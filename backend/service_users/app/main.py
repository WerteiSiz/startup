from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
import sys

from app.models import *

from .database import get_db, create_tables
from . import crud
from .schemas import *
from .security import *


from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")

# ==================== Lifespan ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Начинаем создание таблиц...", file=sys.stderr)
    try:
        await create_tables()
        print("✅ Таблицы созданы/проверены", file=sys.stderr)

        # Подключаем брокера
        print("🔄 Подключение к RabbitMQ...", file=sys.stderr)
        await broker.connect()  # 👈 ВАЖНО: сначала connect()
        print("✅ Брокер подключен", file=sys.stderr)
        
        # Объявляем очередь
        from faststream.rabbit import RabbitQueue
        await broker.declare_queue(RabbitQueue("email_queue"))
        print("✅ Очередь email_queue объявлена", file=sys.stderr)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    yield

    await broker.close()



# ==================== App ====================

app = FastAPI(
    title="StudentPass API",
    description="Платформа студенческих скидок",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Dependencies ====================

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Извлекает текущего пользователя из токена в cookie или Authorization header"""
    
    # Пробуем взять токен из cookie
    token = request.cookies.get("access_token")
    
    # Если нет в cookie, пробуем из Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Не предоставлен токен")
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Невалидный или истёкший токен")
    
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    user = await crud.get_user_by_email(db, user_email)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Пользователь не найден или удалён")
    
    return user


async def get_current_partner(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Partner:
    """Проверяет, что текущий пользователь — партнёр, и возвращает объект Partner"""
    
    if current_user.role != UserRole.PARTNER:
        raise HTTPException(status_code=403, detail="Доступ только для партнёров")
    
    partner = await crud.get_partner_by_user_id(db, current_user.id)
    if not partner or not partner.is_approved:
        raise HTTPException(status_code=403, detail="Партнёр не одобрен администратором")
    
    return partner


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Проверяет, что текущий пользователь — администратор"""
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")
    
    return current_user


# ==================== Health ====================

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "service": "StudentPass API"}


# ==================== Auth Routes ====================

@app.post("/api/v1/auth/register", response_model=MessageResponse)
async def register_user(
    data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли пользователь (включая неактивных)
    existing_user = await crud.get_user_by_email_including_inactive(db, data.email)
    if existing_user:
        if not existing_user.is_active:
            raise HTTPException(status_code=400, detail="Этот email был удалён. Восстановление невозможно, зарегистрируйтесь с другим email")
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    # Хешируем пароль
    hashed_password = get_password_hash(data.password)
    
    # Создаём пользователя
    new_user = await crud.create_user(
        db=db,
        email=data.email,
        password_hash=hashed_password,
        full_name=data.full_name,
        role=UserRole.USER
    )
    
    # Генерируем код подтверждения (6 цифр)
    import random
    code = f"{random.randint(100000, 999999)}"
    
    # Сохраняем код в email_verifications
    await crud.create_email_verification(db, new_user.id, code)
    
    # TODO: Отправить код на email (пока просто логируем)
    print(f"📧 Код подтверждения для {data.email}: {code}")

    email_data = {
        "email": new_user.email,
        "full_name": new_user.full_name,
        "subject": "Добро пожаловать в StudentPass!",
        "message": "Вы успешно зарегистрировались в платформе студенческих скидок StudentPass",
        "code": code
    }
    
    await broker.publish(email_data, queue="email_queue")
    
    return MessageResponse(message="Код подтверждения отправлен на почту")


@app.post("/api/v1/auth/register-partner", response_model=MessageResponse)
async def register_partner(
    data: UserRegisterPartner,
    db: AsyncSession = Depends(get_db)
):
    # Проверяем email
    existing_user = await crud.get_user_by_email_including_inactive(db, data.email)
    if existing_user:
        if not existing_user.is_active:
            raise HTTPException(status_code=400, detail="Этот email был удалён")
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    # Создаём пользователя с ролью PARTNER (но is_active=True, ждёт одобрения админом)
    hashed_password = get_password_hash(data.password)
    new_user = await crud.create_user(
        db=db,
        email=data.email,
        password_hash=hashed_password,
        full_name=data.full_name,
        phone=data.phone,
        role=UserRole.PARTNER
    )
    
    # Создаём заявку на партнёрство
    await crud.create_partner_request(
        db=db,
        user_id=new_user.id,
        company_name=data.company_name,
        contact_person=data.full_name,
        phone=data.phone,
        description=data.description
    )
    
    # Генерируем код подтверждения email
    import random
    code = f"{random.randint(100000, 999999)}"
    await crud.create_email_verification(db, new_user.id, code)
    
    print(f"📧 Код подтверждения для {data.email}: {code}")
    
    return MessageResponse(message="Заявка на партнёрство отправлена. " \
    "После подтверждения email и одобрения администратором вы сможете размещать объявления")


@app.post("/api/v1/auth/verify-email", response_model=TokenResponse)
async def verify_email(
    data: EmailVerify,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Находим верификацию
    verification = await crud.get_email_verification(db, data.email, data.code)
    if not verification:
        raise HTTPException(status_code=400, detail="Неверный или истёкший код")
    
    # Получаем пользователя
    user = await crud.get_user_by_email_including_inactive(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Удаляем код верификации
    await crud.delete_email_verification(db, verification.id)
    
    # Создаём токен
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role,
        "full_name": user.full_name
    }
    access_token = create_access_token(data=token_data)
    
    # Устанавливаем cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * int(os.getenv('ACC_TOKEN_EXP_MIN', 60)),
        path="/"
    )
    
    return TokenResponse(access_token=access_token)


@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role,
        "full_name": user.full_name
    }
    access_token = create_access_token(data=token_data)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * int(os.getenv('ACC_TOKEN_EXP_MIN', 60)),
        path="/"
    )
    
    return TokenResponse(access_token=access_token)


@app.post("/api/v1/auth/logout", response_model=MessageResponse)
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return MessageResponse(message="Выход выполнен")


@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@app.delete("/api/v1/auth/me", response_model=MessageResponse)
async def delete_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await crud.soft_delete_user(db, current_user.id)
    return MessageResponse(message="Аккаунт удалён. Данные будут храниться 3 месяца")


# ==================== Ads Routes ====================

@app.get("/api/v1/ads", response_model=AdListResponse)
async def get_ads(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from .schemas import AdFilterParams
    params = AdFilterParams(
        category=category,
        search=search,
        sort=sort,
        page=page,
        limit=limit
    )
    
    user_id = current_user.id if current_user else None
    ads, total = await crud.get_ads(db, params, user_id)
    
    # Формируем ответ
    items = []
    for ad in ads:
        items.append(AdResponse(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            discount_percent=ad.discount_percent,
            url=ad.url,
            address=ad.address,
            end_date=ad.end_date,
            clicks_count=ad.clicks_count,
            partner_id=ad.partner_id,
            partner_name=ad.partner.company_name,
            categories=[cat.name for cat in ad.categories],
            is_favorite=getattr(ad, 'is_favorite', False),
            emodzi_id=ad.emodzi_id,
            prioritet=ad.prioritet
        ))
    
    pages = (total + limit - 1) // limit
    return AdListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@app.get("/api/v1/ads/{ad_id}", response_model=AdDetailResponse)
async def get_ad_detail(
    ad_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ad = await crud.get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    is_favorite = False
    if current_user:
        is_favorite = await crud.is_favorite(db, current_user.id, ad_id)
    
    return AdDetailResponse(
        id=ad.id,
        title=ad.title,
        description=ad.description,
        discount_percent=ad.discount_percent,
        url=ad.url,
        address=ad.address,
        end_date=ad.end_date,
        clicks_count=ad.clicks_count,
        partner_id=ad.partner_id,
        partner_name=ad.partner.company_name,
        categories=[cat.name for cat in ad.categories],
        is_favorite=is_favorite,
        emodzi_id=ad.emodzi_id,
        prioritet=ad.prioritet,
        created_at=ad.created_at,
        updated_at=ad.updated_at
    )


@app.post("/api/v1/ads/{ad_id}/click")
async def click_ad(
    ad_id: int,
    db: AsyncSession = Depends(get_db)
):
    ad = await crud.increment_ad_clicks(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    # Редирект на url партнёра
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=ad.url)


@app.get("/api/v1/ads/categories", response_model=List[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    categories, _ = await crud.get_categories(db)
    return [CategoryResponse(id=cat.id, name=cat.name, is_custom=cat.is_custom) for cat in categories]


# ==================== Favorites Routes ====================

@app.get("/api/v1/favorites", response_model=FavoriteListResponse)
async def get_favorites(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * limit
    ads, total = await crud.get_favorites(db, current_user.id, skip, limit)
    
    items = []
    for ad in ads:
        items.append(FavoriteResponse(
            ad_id=ad.id,
            title=ad.title,
            discount_percent=ad.discount_percent,
            end_date=ad.end_date,
            partner_name=ad.partner.company_name
        ))
    
    return FavoriteListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit
    )


@app.post("/api/v1/favorites/{ad_id}", response_model=MessageResponse)
async def add_favorite(
    ad_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли объявление
    ad = await crud.get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    # Проверяем, не в избранном ли уже
    if await crud.is_favorite(db, current_user.id, ad_id):
        raise HTTPException(status_code=400, detail="Уже в избранном")
    
    await crud.add_favorite(db, current_user.id, ad_id)
    return MessageResponse(message="Добавлено в избранное")


@app.delete("/api/v1/favorites/{ad_id}", response_model=MessageResponse)
async def remove_favorite(
    ad_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    removed = await crud.remove_favorite(db, current_user.id, ad_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Объявление не найдено в избранном")
    
    return MessageResponse(message="Удалено из избранного")


# ==================== Partners (public) Routes ====================

@app.get("/api/v1/partners", response_model=List[PartnerResponse])
async def get_partners(
    search: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    partners, _ = await crud.get_partners(db, skip=0, limit=limit, search=search)
    
    result = []
    for partner in partners:
        ads_count = await crud.get_partner_ads_count(db, partner.id)
        result.append(PartnerResponse(
            id=partner.id,
            company_name=partner.company_name,
            description=partner.description,
            logo_url=partner.logo_url,
            ads_count=ads_count
        ))
    
    return result


@app.get("/api/v1/partners/{partner_id}/ads", response_model=AdListResponse)
async def get_partner_ads(
    partner_id: int,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли партнёр
    partner = await crud.get_partner_by_id(db, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Партнёр не найден")
    
    skip = (page - 1) * limit
    ads, total = await crud.get_ads_by_partner(db, partner_id, skip, limit, include_inactive=False)
    
    items = []
    for ad in ads:
        items.append(AdResponse(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            discount_percent=ad.discount_percent,
            url=ad.url,
            address=ad.address,
            end_date=ad.end_date,
            clicks_count=ad.clicks_count,
            partner_id=partner_id,
            partner_name=partner.company_name,
            categories=[cat.name for cat in ad.categories],
            is_favorite=False,
            emodzi_id=ad.emodzi_id,
            prioritet=ad.prioritet
        ))
    
    pages = (total + limit - 1) // limit
    return AdListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


# ==================== Partner Cabinet Routes (role=partner) ====================

@app.get("/api/v1/partner/ads", response_model=PartnerAdsResponse)
async def get_my_ads(
    page: int = 1,
    limit: int = 20,
    current_partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * limit
    ads, total = await crud.get_ads_by_partner(db, current_partner.id, skip, limit, include_inactive=True)
    ads_used = await crud.get_partner_ads_count(db, current_partner.id)
    
    items = []
    for ad in ads:
        items.append(AdResponse(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            discount_percent=ad.discount_percent,
            url=ad.url,
            address=ad.address,
            end_date=ad.end_date,
            clicks_count=ad.clicks_count,
            partner_id=current_partner.id,
            partner_name=current_partner.company_name,
            categories=[cat.name for cat in ad.categories],
            is_favorite=False,
            emodzi_id=ad.emodzi_id,
            prioritet=ad.prioritet
        ))
    
    pages = (total + limit - 1) // limit
    return PartnerAdsResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
        ads_used=ads_used,
        ads_limit=current_partner.ads_limit
    )


@app.post("/api/v1/partner/ads", response_model=MessageResponse)
async def create_ad(
    data: AdCreate,
    current_partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем лимит объявлений
    current_count = await crud.get_partner_ads_count(db, current_partner.id)
    if current_count >= current_partner.ads_limit:
        raise HTTPException(status_code=400, detail=f"Превышен лимит объявлений (максимум {current_partner.ads_limit})")
    
    # Проверяем, что категории существуют
    for cat_id in data.category_ids:
        category = await crud.get_category_by_id(db, cat_id)
        if not category:
            raise HTTPException(status_code=400, detail=f"Категория с id {cat_id} не найдена")
    
    await crud.create_ad(
        db=db,
        partner_id=current_partner.id,
        title=data.title,
        description=data.description,
        discount_percent=data.discount_percent,
        url=data.url,
        address=data.address,
        end_date=data.end_date,
        category_ids=data.category_ids,
        emodzi_id=data.emodzi_id,
        prioritet=data.prioritet
    )
    
    return MessageResponse(message="Объявление создано")


@app.put("/api/v1/partner/ads/{ad_id}", response_model=MessageResponse)
async def update_ad(
    ad_id: int,
    data: AdUpdate,
    current_partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, что объявление принадлежит партнёру
    ad = await crud.get_ad_by_id(db, ad_id)
    if not ad or ad.partner_id != current_partner.id:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    # Обновляем только переданные поля
    update_data = data.dict(exclude_unset=True)
    if "category_ids" in update_data:
        # TODO: Обновление категорий (сначала удалить старые, потом добавить новые)
        pass
    
    await crud.update_ad(db, ad_id, **update_data)
    return MessageResponse(message="Объявление обновлено")


@app.delete("/api/v1/partner/ads/{ad_id}", response_model=MessageResponse)
async def delete_ad(
    ad_id: int,
    current_partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, что объявление принадлежит партнёру
    ad = await crud.get_ad_by_id(db, ad_id)
    if not ad or ad.partner_id != current_partner.id:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    await crud.delete_ad(db, ad_id)
    return MessageResponse(message="Объявление удалено")


# ==================== Admin Routes (role=admin) ====================

@app.get("/api/v1/admin/partner-requests", response_model=AdminPartnerRequestListResponse)
async def get_partner_requests(
    status: Optional[PartnerRequestStatus] = None,
    page: int = 1,
    limit: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * limit
    requests, total = await crud.get_partner_requests(db, status, skip, limit)
    
    items = []
    for req in requests:
        items.append(PartnerRequestResponse(
            id=req.id,
            company_name=req.company_name,
            contact_person=req.contact_person,
            phone=req.phone,
            description=req.description,
            status=req.status,
            admin_comment=req.admin_comment,
            created_at=req.created_at
        ))
    
    pages = (total + limit - 1) // limit
    return AdminPartnerRequestListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@app.put("/api/v1/admin/partner-requests/{request_id}", response_model=MessageResponse)
async def update_partner_request(
    request_id: int,
    data: PartnerRequestUpdate,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    partner_request = await crud.update_partner_request_status(
        db, request_id, data.status, data.admin_comment
    )
    
    if not partner_request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    # Если заявка одобрена, создаём запись в partners
    if data.status == PartnerRequestStatus.APPROVED:
        # Находим пользователя
        user = await crud.get_user(db, partner_request.user_id)
        if user:
            # Создаём партнёра
            await crud.create_partner(
                db=db,
                user_id=user.id,
                company_name=partner_request.company_name,
                description=partner_request.description
            )
    
    return MessageResponse(message=f"Заявка {data.status.value}")


@app.get("/api/v1/admin/users", response_model=AdminUserListResponse)
async def get_users(
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * limit
    users, total = await crud.get_users(db, skip, limit, role, search)
    
    items = []
    for user in users:
        items.append(AdminUserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        ))
    
    pages = (total + limit - 1) // limit
    return AdminUserListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@app.put("/api/v1/admin/users/{user_id}/role", response_model=MessageResponse)
async def change_user_role(
    user_id: int,
    data: AdminUserRoleUpdate,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    # TODO: Реализовать смену роли
    # Пока просто заглушка
    return MessageResponse(message=f"Роль пользователя изменена на {data.role.value}")


@app.post("/api/v1/admin/categories", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    existing = await crud.get_category_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Категория уже существует")
    
    category = await crud.create_category(db, data.name, is_custom=False)
    return CategoryResponse(id=category.id, name=category.name, is_custom=category.is_custom)
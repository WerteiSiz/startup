import sys
from sqlalchemy import delete, select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Tuple
from .models import *
from .schemas import AdFilterParams


# ==================== Users ====================

async def create_user(
    db: AsyncSession,
    email: str,
    password_hash: str,
    full_name: str,
    phone: Optional[str] = None,
    role: UserRole = UserRole.USER
) -> User:
    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        phone=phone,
        role=role,
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.email == email, User.is_active == True)
    )
    return result.scalar_one_or_none()


async def get_user_by_email_including_inactive(db: AsyncSession, email: str) -> Optional[User]:
    """Получить пользователя даже если is_active=False (нужно для проверки при регистрации)"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    role: Optional[UserRole] = None,
    search: Optional[str] = None
) -> Tuple[List[User], int]:
    query = select(User).where(User.is_active == True)
    
    if role:
        query = query.where(User.role == role)
    
    if search:
        query = query.where(
            or_(
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
        )
    
    # Подсчёт общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    # Пагинация
    query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users, total


async def soft_delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """Soft delete — помечаем пользователя как удалённого"""
    user = await get_user(db, user_id)
    if user:
        user.is_active = False
        user.deleted_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)
    return user


# ==================== Email Verification ====================

async def create_email_verification(
    db: AsyncSession,
    email: str,
    code: str,
    expires_minutes: int = 15
) -> EmailVerification:
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    verification = EmailVerification(
        user_email=email,
        code=code,
        expires_at=expires_at
    )
    db.add(verification)
    await db.commit()
    await db.refresh(verification)
    return verification


async def get_email_verification(
    db: AsyncSession,
    email: str,
    code: str
) -> Optional[EmailVerification]:
    
    result = await db.execute(
        select(EmailVerification).where(
            EmailVerification.user_email == email,
            EmailVerification.code == code,
            EmailVerification.expires_at > datetime.utcnow()
        )
    )

    return result.scalar_one_or_none()


async def delete_email_verification(db: AsyncSession, email: str):
    await db.execute(
        delete(EmailVerification).where(EmailVerification.user_email == email)
    )
    await db.commit()


# ==================== Partner Requests ====================

async def create_partner_request(
    db: AsyncSession,
    user_id: int,
    company_name: str,
    contact_person: str,
    phone: str,
    description: Optional[str] = None
) -> PartnerRequest:
    request = PartnerRequest(
        user_id=user_id,
        company_name=company_name,
        contact_person=contact_person,
        phone=phone,
        description=description,
        status=PartnerRequestStatus.PENDING
    )
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request


async def get_partner_request_by_user_id(
    db: AsyncSession,
    user_id: int
) -> Optional[PartnerRequest]:
    result = await db.execute(
        select(PartnerRequest).where(PartnerRequest.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_partner_requests(
    db: AsyncSession,
    status: Optional[PartnerRequestStatus] = None,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[PartnerRequest], int]:
    query = select(PartnerRequest)
    
    if status:
        query = query.where(PartnerRequest.status == status)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    query = query.offset(skip).limit(limit).order_by(PartnerRequest.created_at.desc())
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return requests, total


async def update_partner_request_status(
    db: AsyncSession,
    request_id: int,
    status: PartnerRequestStatus,
    admin_comment: Optional[str] = None
) -> Optional[PartnerRequest]:
    result = await db.execute(
        select(PartnerRequest).where(PartnerRequest.id == request_id)
    )
    request = result.scalar_one_or_none()
    
    if request:
        request.status = status
        if admin_comment:
            request.admin_comment = admin_comment
        request.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(request)
    
    return request


# ==================== Partners ====================

async def create_partner(
    db: AsyncSession,
    user_id: int,
    company_name: str,
    description: Optional[str] = None,
    logo_url: Optional[str] = None,
    ads_limit: int = 5
) -> Partner:
    partner = Partner(
        user_id=user_id,
        company_name=company_name,
        description=description,
        logo_url=logo_url,
        is_approved=True,
        ads_limit=ads_limit
    )
    db.add(partner)
    await db.commit()
    await db.refresh(partner)
    return partner


async def get_partner_by_user_id(db: AsyncSession, user_id: int) -> Optional[Partner]:
    result = await db.execute(
        select(Partner).where(Partner.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_partner_by_id(db: AsyncSession, partner_id: int) -> Optional[Partner]:
    result = await db.execute(
        select(Partner).where(Partner.id == partner_id, Partner.is_approved == True)
    )
    return result.scalar_one_or_none()


async def get_partners(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> Tuple[List[Partner], int]:
    query = select(Partner).where(Partner.is_approved == True)
    
    if search:
        query = query.where(Partner.company_name.ilike(f"%{search}%"))
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    query = query.offset(skip).limit(limit).order_by(Partner.created_at.desc())
    result = await db.execute(query)
    partners = result.scalars().all()
    
    return partners, total


async def get_partner_ads_count(db: AsyncSession, partner_id: int) -> int:
    result = await db.execute(
        select(func.count()).where(Ad.partner_id == partner_id, Ad.is_active == True)
    )
    return result.scalar()


# ==================== Categories ====================

async def create_category(db: AsyncSession, name: str, is_custom: bool = False) -> Category:
    category = Category(name=name, is_custom=is_custom)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.name == name))
    return result.scalar_one_or_none()


async def get_category_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Category], int]:
    query = select(Category).order_by(Category.name)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return categories, total


# ==================== Ads ====================

async def create_ad(
    db: AsyncSession,
    partner_id: int,
    title: str,
    discount_percent: int,
    url: str,
    address: str,
    end_date: datetime,
    description: Optional[str] = None,
    category_ids: Optional[List[int]] = None,
    emodzi_id: Optional[int] = None,
    prioritet: int = 0
) -> Ad:
    ad = Ad(
        partner_id=partner_id,
        title=title,
        description=description,
        discount_percent=discount_percent,
        url=url,
        address=address,
        end_date=end_date,
        emodzi_id=emodzi_id,
        prioritet=prioritet,
        is_active=True
    )
    db.add(ad)
    await db.flush()  # Чтобы получить ad.id
    
    # Добавляем категории
    if category_ids:
        for cat_id in category_ids:
            db.add(AdCategory(ad_id=ad.id, category_id=cat_id))
    
    await db.commit()
    await db.refresh(ad)
    return ad


async def get_ad_by_id(db: AsyncSession, ad_id: int) -> Optional[Ad]:
    result = await db.execute(
        select(Ad)
        .options(selectinload(Ad.categories))
        .where(Ad.id == ad_id, Ad.is_active == True, Ad.end_date > datetime.utcnow())
    )
    return result.scalar_one_or_none()


async def get_ads(
    db: AsyncSession,
    params: AdFilterParams,
    user_id: Optional[int] = None
) -> Tuple[List[Ad], int]:
    query = select(Ad).options(selectinload(Ad.categories)).where(
        Ad.is_active == True,
        Ad.end_date > datetime.utcnow()
    )
    
    # Фильтр по категории
    if params.category:
        query = query.join(Ad.categories).where(Category.name == params.category)
    
    # Поиск по названию
    if params.search:
        query = query.where(Ad.title.ilike(f"%{params.search}%"))
    
    # Сортировка
    if params.sort == "newest":
        query = query.order_by(Ad.created_at.desc())
    elif params.sort == "ending_soon":
        query = query.order_by(Ad.end_date.asc())
    elif params.sort == "popular":
        query = query.order_by(Ad.clicks_count.desc())
    else:
        query = query.order_by(Ad.prioritet.desc(), Ad.created_at.desc())
    
    # Подсчёт общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    # Пагинация
    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)
    result = await db.execute(query)
    ads = result.scalars().all()
    
    # Получаем избранное для пользователя
    favorites = set()
    if user_id:
        fav_result = await db.execute(
            select(Favorite.ad_id).where(Favorite.user_id == user_id)
        )
        favorites = {row[0] for row in fav_result.all()}
    
    # Добавляем is_favorite к каждому объявлению
    for ad in ads:
        ad.is_favorite = ad.id in favorites
    
    return ads, total


async def get_ads_by_partner(
    db: AsyncSession,
    partner_id: int,
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False
) -> Tuple[List[Ad], int]:
    query = select(Ad).where(Ad.partner_id == partner_id)
    
    if not include_inactive:
        query = query.where(Ad.is_active == True)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    query = query.offset(skip).limit(limit).order_by(Ad.created_at.desc())
    result = await db.execute(query)
    ads = result.scalars().all()
    
    return ads, total


async def update_ad(
    db: AsyncSession,
    ad_id: int,
    **kwargs
) -> Optional[Ad]:
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    
    if not ad:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(ad, key):
            setattr(ad, key, value)
    
    ad.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(ad)
    return ad


async def increment_ad_clicks(db: AsyncSession, ad_id: int) -> Optional[Ad]:
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    
    if ad:
        ad.clicks_count += 1
        await db.commit()
        await db.refresh(ad)
    
    return ad


async def delete_ad(db: AsyncSession, ad_id: int) -> bool:
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    
    if ad:
        ad.is_active = False
        await db.commit()
        return True
    
    return False


async def get_partner_ads_count(db: AsyncSession, partner_id: int) -> int:
    result = await db.execute(
        select(func.count()).where(Ad.partner_id == partner_id, Ad.is_active == True)
    )
    return result.scalar()


# ==================== Favorites ====================

async def add_favorite(db: AsyncSession, user_id: int, ad_id: int) -> Favorite:
    favorite = Favorite(user_id=user_id, ad_id=ad_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(db: AsyncSession, user_id: int, ad_id: int) -> bool:
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.ad_id == ad_id
        )
    )
    favorite = result.scalar_one_or_none()
    
    if favorite:
        await db.delete(favorite)
        await db.commit()
        return True
    
    return False


async def get_favorites(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Ad], int]:
    query = select(Ad).join(Favorite).where(
        Favorite.user_id == user_id,
        Ad.is_active == True,
        Ad.end_date > datetime.utcnow()
    )
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.execute(count_query)
    total = total.scalar()
    
    query = query.offset(skip).limit(limit).order_by(Favorite.created_at.desc())
    result = await db.execute(query)
    ads = result.scalars().all()
    
    return ads, total


async def is_favorite(db: AsyncSession, user_id: int, ad_id: int) -> bool:
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.ad_id == ad_id
        )
    )
    return result.scalar_one_or_none() is not None
from fastapi import APIRouter, FastAPI, Header, Response, responses, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, create_tables
from . import crud
from .schemas import *
from contextlib import asynccontextmanager
from .security import *
from sqlalchemy import select
from .models import *
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import sys

import logging
logger = logging.getLogger(__name__)

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):

    token = request.cookies.get("access_token")
    
    # 3. Декодируем и проверяем токен (включая черный список)
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # 4. Извлекаем email из payload (в токене хранится {"sub": "user@email.com"})
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # 5. Ищем пользователя в БД по email
    user = await crud.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 6. Возвращаем объект пользователя
    return user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Начинаем создание таблицы users...-----------------------"
    "-------------------------------------------------------------------------------------", file=sys.stderr)
    try:
        await create_tables()
        print("✅ Таблица users созданы/проверены", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}", file=sys.stderr)
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/v1/users")

templates = Jinja2Templates(directory="app/templates")

@router.get("/health")
async def health():
    return {'message': 'service_users successfully working!'}

@router.post("/register")
async def register_user(UserCreate: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, UserCreate.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = get_password_hash(UserCreate.password)
    new_user = await crud.create_user(db, UserCreate.full_name, UserCreate.email, hashed_password, UserCreate.role)

    return {"msg": "Пользователь успешно зарегистрирован", 'user': new_user}


@router.post("/login")
async def login(UserLogin: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, UserLogin.email)

    if not existing_user or not verify_password(UserLogin.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token_data = {
        "sub": UserLogin.email,
        "user_id": str(existing_user.id),
        "role": existing_user.role,
        "full_name": existing_user.full_name
    }    
    access_token = create_access_token(data=token_data)
    
    # 👇 УСТАНАВЛИВАЕМ HTTPONLY COOKIE
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False,  # True in production (HTTPS only)
        samesite="lax", max_age=3600, path="/")       # доступно для всех путей
    
    return {"message": "Login successful", "token_type": "bearer"}  

@router.get("/me", response_model=UserResponse)  # 👈 Добавляем схему ответа
async def get_me(current_user: User = Depends(get_current_user)):
    logger.warning(current_user.__dict__)
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,  # 👈 Исправляем на full_name
        role=current_user.role,            # 👈 Исправляем на role
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

app.include_router(router)


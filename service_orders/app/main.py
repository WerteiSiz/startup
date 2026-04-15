from fastapi import FastAPI, Header, responses, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, create_tables
from . import crud
from .schemas import *
from contextlib import asynccontextmanager
from sqlalchemy import select
from .models import Orders
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import sys

import logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Начинаем создание таблицы orders...-----------------------"
    "-------------------------------------------------------------------------------------", file=sys.stderr)
    try:
        await create_tables()
        print("✅ Таблица orders созданы/проверены", file=sys.stderr)
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}", file=sys.stderr)
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/v1/orders")

templates = Jinja2Templates(directory="app/templates")

@router.get("/health")
async def health():
    return {'message': 'defects_orders successfully working!'}




@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    x_user_id: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить дефекты текущего пользователя"""
    user_id = UUID(x_user_id)
    orders = await crud.get_user_orders(db, user_id, skip=skip, limit=limit)
    return orders

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    x_user_id: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый дефект"""
    user_id = UUID(x_user_id)
    order = await crud.create_order(
        db, 
        user_id=user_id,
        defect_data=order_data.dict()
    )
    return order

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    x_user_id: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить дефект по ID"""
    user_id = UUID(x_user_id)
    order = await crud.get_order(db, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Defect not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: UUID,
    order_update: OrderUpdate,
    x_user_id: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус дефекта"""
    user_id = UUID(x_user_id)
    order = await crud.get_order(db, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Defect not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    updated_order = await crud.update_order_status(db, order_id, order_update.status)
    return updated_order


@router.delete("/{order_id}")
async def delete_order(
    order_id: UUID,
    x_user_id: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Удалить дефект"""
    user_id = UUID(x_user_id)
    order = await crud.get_order(db, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Defect not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    await crud.delete_order(db, order_id)
    return {"message": "Defect deleted"}




app.include_router(router)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *



async def create_user(db: AsyncSession, name: str, email: str, hashed_password: str, role: str):
    user = User(full_name=name, email=email, password_hash=hashed_password, role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, user_email: str):
    result = await db.execute(select(User).where(User.email == user_email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user
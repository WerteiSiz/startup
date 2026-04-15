import sys
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
import logging
logger = logging.getLogger(__name__)

# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    try:
        result = pwd_context.hash(password)
        print("✅ Хеширование успешно")
        return result
    except Exception as e:
        print(f"❌ Ошибка хеширования: {e}")
        raise

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta = int(os.getenv('ACC_TOKEN_EXP_MIN'))):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
#     to_encode.update({"exp": expire})  # Добавляем время истечения
#     encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
#     return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')])
        logger.warning(payload)
        return payload
    except JWTError:
        return None  # Если токен недействителен или истёк
    
    
# Функция для проверки валидности токена (для зависимостей)
def verify_token(token: str):
    return decode_token(token) is not None

from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os

# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password: str) -> str:
    try:
        result = pwd_context.hash(password)
        print("✅ Хеширование успешно")
        return result
    except Exception as e:
        print(f"❌ Ошибка хеширования: {e}")
        raise

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = None) -> str:
    """
    Создание access токена.
    expires_delta — время жизни в минутах. Если не передан, берётся из .env
    """
    to_encode = data.copy()
    
    if expires_delta is None:
        expires_delta = int(os.getenv('ACC_TOKEN_EXP_MIN', 60))
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        os.getenv('JWT_SECRET_KEY'), 
        algorithm=os.getenv('JWT_ALGORITHM', 'HS256')
    )
    return encoded_jwt


def decode_token(token: str):
    """Декодирует токен, возвращает payload или None"""
    try:
        payload = jwt.decode(
            token, 
            os.getenv('JWT_SECRET_KEY'), 
            algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')]
        )
        return payload
    except JWTError:
        return None


def verify_token(token: str) -> bool:
    """Проверяет валидность токена (не истёк и подпись верна)"""
    return decode_token(token) is not None


def get_current_user_id(token: str) -> int:
    """
    Извлекает user_id из токена.
    Если токен невалиден — выбрасывает 401 ошибку.
    """
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или истёкший токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена",
        )
    
    return int(user_id)
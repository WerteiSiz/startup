from fastapi import Request, HTTPException
import time
from typing import Dict, Tuple
import logging
from collections import defaultdict

from fastapi.responses import JSONResponse
import os
import redis
logger = logging.getLogger(__name__)

# In-memory хранилище: { "ip:path": (count, window_start) }
request_counts: Dict[str, Tuple[int, float]] = {}
# Альтернатива с defaultdict для автоматической очистки
# request_counts = defaultdict(lambda: (0, 0))

r = redis.from_url(os.getenv('REDIS_URL'))

class RateLimitExceededException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=429, detail=detail)

def get_client_ip(request: Request) -> str:
    """Получаем реальный IP клиента с учётом прокси"""
    if "x-forwarded-for" in request.headers:
        # Если за nginx/load balancer - берём первый IP из цепочки
        ip = request.headers["x-forwarded-for"].split(",")[0].strip()
    else:
        ip = request.client.host or "unknown"
    return ip

def should_rate_limit(request: Request) -> bool:
    """Определяем, нужно ли применять rate limiting к этому пути"""
    path = request.url.path
    
    # Не ограничиваем статические файлы и health checks
    excluded_paths = [
        '/health',
        '/api/health', 
        '/api/v1/users/health',
        '/api/v1/orders/health',
        '/static/',
        '/favicon.ico'
    ]
    
    return not any(path.startswith(excluded) for excluded in excluded_paths)

async def rate_limit_middleware(request: Request, call_next):
    """Middleware для ограничения запросов по IP"""
    
    # Пропускаем OPTIONS запросы (CORS preflight)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    # Проверяем, нужно ли ограничивать этот путь
    if not should_rate_limit(request):
        return await call_next(request)
    if should_rate_limit(request):
        return await call_next(request)
    
    client_ip = get_client_ip(request)
    path = request.url.path
    current_time = time.time()  # ← ТВОЯ СТРОКА НА МЕСТЕ
    
    # Определяем лимиты в зависимости от пути
    limits_config = {
        "/api/v1/users/login": {"limit": 500, "window": 60},
        "/api/v1/users/register": {"limit": 500, "window": 300},
        "/api/v1/orders": {"limit": 3000, "window": 60},
        "default": {"limit": 1000, "window": 60}  # исправил 100 → 10
    }
    
    # Находим подходящий лимит
    limit_config = limits_config.get(path, limits_config["default"])
    limit = limit_config["limit"]
    window = limit_config["window"]
    
    # Ключи как у тебя
    key_reqs = f"{client_ip}:{path}:requests"
    key_blocking = f'{client_ip}:{path}:blocking'
    
    try:
        # ВСЕ проверки в одном pipeline (атомарно)
        pipe = r.pipeline()
        pipe.exists(key_blocking)      # 1. Проверяем блокировку
        pipe.ttl(key_blocking)         # 2. TTL блокировки
        pipe.get(key_reqs)             # 3. Текущий счетчик
        pipe.ttl(key_reqs)             # 4. TTL счетчика
        
        results = pipe.execute()
        blocking_exists = results[0]   # bool
        ttl_blocking = results[1]      # int (или -2)
        current_count = results[2]     # str или None
        ttl_reqs = results[3]          # int
        
        # Если заблокирован и TTL > 0
        if blocking_exists and ttl_blocking > 0:
            print(f'block for {ttl_blocking} secs')
            return return_exept(ttl_blocking, limit, window)  # обновил функцию
        
        # Создаем новый pipeline для изменений
        pipe = r.pipeline()
        
        if not current_count:  # Первый запрос
            pipe.setex(key_reqs, window, 1)
            pipe.setex(key_blocking, window, '')  # пустой флаг блокировки
            print(f'first request - set counters')
        else:
            current_count = int(current_count)
            
            # Используем limit из конфига, а не хардкод 9
            if current_count >= limit - 1:  # ← ИСПРАВИЛ == 9
                # Превысили лимит - блокируем
                pipe.expire(key_blocking, window)  # включаем блокировку
                pipe.delete(key_reqs)  # сбрасываем счетчик
                print(f'limit exceeded - block for {window} secs')
                pipe.execute()
                return return_exept(window, limit, window)
            else:
                # Увеличиваем счетчик
                pipe.incr(key_reqs)
                # Если окно почти истекло (< половины), обновляем TTL
                if ttl_reqs < window // 2:
                    pipe.expire(key_reqs, window)
                print(f'increment to {current_count + 1}')
        
        pipe.execute()
        
        # Запрос прошел
        response = await call_next(request)
        
        # Добавляем заголовки (опционально)
        remaining = max(0, limit - (int(current_count) if current_count else 0) - 1)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time) + (ttl_reqs if ttl_reqs > 0 else window))
        
        return response
        
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        # При ошибке Redis пропускаем rate limiting
        return await call_next(request)


def return_exept(remaining_time: int, limit: int, window: int):
    """Обновленная функция с параметрами лимита"""
    return JSONResponse(
        status_code=429,
        content={
            "detail": f"Слишком много запросов. Лимит: {limit} в {window} секунд. Попробуйте через {remaining_time} сек."
        },
        headers={
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": "0",
            "Retry-After": str(remaining_time)
        }
    )
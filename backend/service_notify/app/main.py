from contextlib import asynccontextmanager
import asyncio
import sys

from fastapi import FastAPI
from faststream.rabbit import RabbitBroker, RabbitQueue
from .email_send import send_email

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
broker = RabbitBroker(RABBITMQ_URL)

@broker.subscriber("email_queue")
async def handle_email(data: dict):
    """Обработчик сообщений из очереди email_queue"""
    print(f"📧 Получено письмо для: {data.get('email')}", file=sys.stderr)
    result = await send_email(
        mail=data["email"],
        full_name=data.get("full_name", ""),
        message=data["message"],
        subject=data["subject"]
    )
    if result:
        print(f"✅ Письмо отправлено на {data['email']}", file=sys.stderr)
    else:
        print(f"❌ Ошибка отправки на {data['email']}", file=sys.stderr)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Запуск service_notify...", file=sys.stderr)
    
    # Подключение с повторными попытками
    for attempt in range(30):
        try:
            await broker.connect()
            print("✅ Подключено к RabbitMQ", file=sys.stderr)
            break
        except Exception as e:
            print(f"⚠️ Попытка {attempt + 1}/30: {e}", file=sys.stderr)
            if attempt < 29:
                await asyncio.sleep(2)
            else:
                print("❌ Не удалось подключиться", file=sys.stderr)
                raise
    
    # Объявляем очередь
    await broker.declare_queue(RabbitQueue("email_queue"))
    print("✅ Очередь готова", file=sys.stderr)
    
    # Важно: запускаем прослушивание очереди в фоне
    asyncio.create_task(broker.start())
    
    print("✅ Сервис уведомлений запущен", file=sys.stderr)
    yield
    
    await broker.close()
    print("❌ Сервис остановлен", file=sys.stderr)

app = FastAPI(lifespan=lifespan)
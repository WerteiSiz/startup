from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from faststream.rabbit import RabbitBroker, RabbitQueue
from .email_send import send_email

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
broker = RabbitBroker(RABBITMQ_URL)

@broker.subscriber("email_queue")
async def handle_email(data: dict):
    print(f"📧 Получено: {data.get('email')}")
    result = await send_email(
        mail=data["email"],
        full_name=data["full_name"],
        message=data["message"],
        subject=data["subject"]
    )
    print(f"✅ Отправлено" if result else "❌ Ошибка")

@asynccontextmanager
async def lifespan(app):
    print("Starting...")
    for i in range(10):
        try:
            await broker.connect()
            break
        except:
            await asyncio.sleep(2)
    await broker.declare_queue(RabbitQueue("email_queue"))
    await broker.start()
    yield
    await broker.close()

app = FastAPI(lifespan=lifespan)  # Это нужно для запуска lifespan
# app = FastAPI() - без lifespan, если не нужен
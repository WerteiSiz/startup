import asyncio
import os
from smtplib import SMTP
from email.mime.text import MIMEText

async def send_email(mail: str, message: str, full_name: str, subject: str) -> bool:
    SMTP_LOGIN = os.getenv('SMTP_LOGIN')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')




    def sync_send_email():
        message_text = f'Добрый день, {full_name}!\n{message}'
        msg = MIMEText(message_text, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_LOGIN
        msg["To"] = mail
        
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.send_message(msg)
            print('Email отправлен синхронно')
        return True

    try:
        await asyncio.to_thread(sync_send_email)
        print(f"✓ Email успешно отправлен на {mail}")
        return True
        
    except Exception as e:
        print(f"✗ Email error: {e}")
        return False
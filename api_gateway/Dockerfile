FROM python:3.12

WORKDIR /app

COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt

# Копируем всю папку app (включая templates)
COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
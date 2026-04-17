docker-compose up --build



Таблицы юзеров и пользователей можно посмореть через Docker Desktop: 
psql -U admin -d users_db

Другие команды:
\d table_name
\dt
\c orders_db
\l

\x auto
+ select * from users;



Браузер
    ↓
NGINX (порт 80)
    ↓
API Gateway (порт 8000) ← 👈 JWT, безопасность, логи
    ↓
Service Users (порт 8000) ← 👈 Только бизнес-логика
Service Orders (порт 8000) ← 👈 Только бизнес-логика


API Gateway: проверка токенов и прав доступа
Service Users: создание токенов, хеширование паролей
Service Orders: бизнес-логика (получает user_id из заголовков)



-------ENDPOINTS--------
1. api_gateway (HTML-страницы):
    GET /                 → index.html
    GET /login            → login.html
    GET /register         → register.html
    GET /orders           → orders.html (JWT) + данные orders/
    GET /orders/{id}      → order_detail.html (JWT) + данные orders/{id}

    Прокси API (Gateway → сервисы)
    /api/v1/users/*    → service_users:8000/api/v1/users/*
    /api/v1/orders/*   → service_orders:8000/api/v1/orders/*


2. Service Users:
    POST /api/v1/users/register
    Body: {user_model}

    POST /api/v1/users/login  
    Body: {email, password}
    Response: Set-Cookie: access_token=...

    POST /api/v1/users/logout
    Response: Clear cookie

    GET /api/v1/users/me
    Headers: Cookie: access_token=...



3. Service Orders:
    GET    /api/v1/orders
    Headers: X-User-ID: ... (из API Gateway)
    Query: ?status=created&skip=0&limit=50

    POST   /api/v1/orders
    Headers: X-User-ID: ...
    Body: {order model}

    GET    /api/v1/orders/{order_id}
    Headers: X-User-ID: ...

    PUT    /api/v1/orders/{order_id}
    Headers: X-User-ID: ...
    Body: {items, total_amount, status}

    DELETE /api/v1/orders/{order_id}
    Headers: X-User-ID: ...







Тестирование сервисов в Postman:
POST http://localhost:8000/api/v1/users/register
Content-Type: application/json
{
  "email": "test@mail.com",
  "password": "123456", 
  "full_name": "Test User",
  "role": "engineer"
}


POST http://localhost:8000/api/v1/users/login
Content-Type: application/json
{
  "email": "test@mail.com",
  "password": "123456"
}


openapi: 3.0.3
info:
  title: Control System Stroy API
  description: |
    Система управления строительными проектами и заказами.
    
    ## Архитектура
    - **API Gateway** (порт 8000) - единая точка входа, аутентификация, проксирование
    - **Service Users** (порт 8000) - управление пользователями, аутентификация
    - **Service Orders** (порт 8000) - управление заказами
    
    ## Аутентификация
    Используется JWT токен, который автоматически устанавливается в cookie после успешного входа.
    
    ## Базы данных
    - `users_db` - данные пользователей
    - `orders_db` - данные заказов
  version: 2.0.0
  contact:
    name: API Support
    email: support@controlsystem.ru

servers:
  - url: http://localhost:8000
    description: Development server

tags:
  - name: Authentication
    description: Аутентификация и управление сессиями
  - name: Users
    description: Управление пользователями
  - name: Orders
    description: Управление заказами

paths:
  # ==================== AUTHENTICATION ====================
  /api/v1/users/register:
    post:
      tags:
        - Authentication
      summary: Регистрация нового пользователя
      description: Создание нового пользователя в системе
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '200':
          description: Пользователь успешно зарегистрирован
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: "Пользователь успешно зарегистрирован"
                  user:
                    $ref: '#/components/schemas/UserResponse'
        '400':
          description: Ошибка валидации или пользователь уже существует
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /api/v1/users/login:
    post:
      tags:
        - Authentication
      summary: Вход в систему
      description: Аутентификация пользователя и установка JWT токена в cookie
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserLogin'
      responses:
        '200':
          description: Успешный вход
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginResponse'
          headers:
            Set-Cookie:
              schema:
                type: string
                example: "access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...; HttpOnly; Path=/; Max-Age=3600"
        '401':
          description: Неверные учетные данные
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  # ==================== USERS ====================
  /api/v1/users/me:
    get:
      tags:
        - Users
      summary: Получить данные текущего пользователя
      description: Возвращает информацию о текущем аутентифицированном пользователе
      security:
        - cookieAuth: []
      responses:
        '200':
          description: Успешное получение данных пользователя
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'


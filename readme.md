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

  # ==================== ORDERS ====================
  /api/v1/orders:
    get:
      tags:
        - Orders
      summary: Получить список заказов пользователя
      description: Возвращает список всех заказов текущего пользователя
      security:
        - cookieAuth: []
      parameters:
        - name: skip
          in: query
          description: Количество записей для пропуска (пагинация)
          required: false
          schema:
            type: integer
            minimum: 0
            default: 0
        - name: limit
          in: query
          description: Максимальное количество записей для возврата
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 100
      responses:
        '200':
          description: Успешное получение списка заказов
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/OrderResponse'
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    post:
      tags:
        - Orders
      summary: Создать новый заказ
      description: Создание нового заказа для текущего пользователя
      security:
        - cookieAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderCreate'
      responses:
        '200':
          description: Заказ успешно создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '400':
          description: Ошибка валидации данных заказа
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /api/v1/orders/{order_id}:
    get:
      tags:
        - Orders
      summary: Получить заказ по ID
      description: Возвращает детальную информацию о конкретном заказе
      security:
        - cookieAuth: []
      parameters:
        - name: order_id
          in: path
          required: true
          description: UUID заказа
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Успешное получение заказа
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '403':
          description: Заказ не принадлежит пользователю
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '404':
          description: Заказ не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    put:
      tags:
        - Orders
      summary: Обновить заказ
      description: Обновление статуса заказа
      security:
        - cookieAuth: []
      parameters:
        - name: order_id
          in: path
          required: true
          description: UUID заказа
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderUpdate'
      responses:
        '200':
          description: Заказ успешно обновлен
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '400':
          description: Ошибка валидации данных
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '403':
          description: Заказ не принадлежит пользователю
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '404':
          description: Заказ не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    delete:
      tags:
        - Orders
      summary: Удалить заказ
      description: Удаление заказа по ID
      security:
        - cookieAuth: []
      parameters:
        - name: order_id
          in: path
          required: true
          description: UUID заказа
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Заказ успешно удален
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Order deleted"
        '401':
          description: Пользователь не аутентифицирован
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '403':
          description: Заказ не принадлежит пользователю
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '404':
          description: Заказ не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  # ==================== HEALTH CHECKS ====================
  /health:
    get:
      summary: Health check API Gateway
      description: Проверка работоспособности API Gateway
      responses:
        '200':
          description: API Gateway работает
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "API Gateway is healthy"

  /api/health:
    get:
      summary: Health check API
      description: Проверка работоспособности API
      responses:
        '200':
          description: API работает
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "API Gateway API is healthy"

  /api/v1/users/health:
    get:
      summary: Health check Service Users
      description: Проверка работоспособности сервиса пользователей
      responses:
        '200':
          description: Сервис пользователей работает
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "service_users successfully working!"

  /api/v1/orders/health:
    get:
      summary: Health check Service Orders
      description: Проверка работоспособности сервиса заказов
      responses:
        '200':
          description: Сервис заказов работает
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "service_orders successfully working!"

components:
  securitySchemes:
    cookieAuth:
      type: apiKey
      in: cookie
      name: access_token
      description: JWT токен аутентификации

  schemas:
    # ==================== USER SCHEMAS ====================
    UserCreate:
      type: object
      required:
        - email
        - password
        - full_name
        - role
      properties:
        email:
          type: string
          format: email
          description: Email пользователя
          example: "user@example.com"
        password:
          type: string
          minLength: 6
          description: Пароль (минимум 6 символов)
          example: "securepassword123"
        full_name:
          type: string
          description: Полное имя пользователя
          example: "Иван Иванов"
        role:
          type: string
          enum: [engineer, manager, seo]
          description: Роль пользователя в системе
          example: "engineer"

    UserLogin:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
          example: "user@example.com"
        password:
          type: string
          example: "securepassword123"

    UserResponse:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: UUID пользователя
          example: "123e4567-e89b-12d3-a456-426614174000"
        email:
          type: string
          format: email
          example: "user@example.com"
        full_name:
          type: string
          example: "Иван Иванов"
        role:
          type: string
          enum: [engineer, manager, seo]
          example: "engineer"
        created_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"

    LoginResponse:
      type: object
      properties:
        message:
          type: string
          example: "Login successful"
        token_type:
          type: string
          example: "bearer"

    # ==================== ORDER SCHEMAS ====================
    OrderItem:
      type: object
      required:
        - product
        - quantity
        - price
      properties:
        product:
          type: string
          description: Название товара
          example: "Цемент М500"
        quantity:
          type: integer
          minimum: 1
          description: Количество товара
          example: 10
        price:
          type: integer
          minimum: 0
          description: Цена за единицу товара (в рублях)
          example: 450

    OrderCreate:
      type: object
      required:
        - items
        - total_amount
      properties:
        items:
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/OrderItem'
          description: Список товаров в заказе
        total_amount:
          type: integer
          minimum: 0
          description: Общая сумма заказа (в рублях)
          example: 4500

    OrderUpdate:
      type: object
      required:
        - status
      properties:
        status:
          type: string
          enum: [created, in_progress, completed, cancelled]
          description: Новый статус заказа
          example: "in_progress"

    OrderResponse:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: UUID заказа
          example: "123e4567-e89b-12d3-a456-426614174000"
        user_id:
          type: string
          format: uuid
          description: UUID пользователя-владельца
          example: "123e4567-e89b-12d3-a456-426614174000"
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
        status:
          type: string
          enum: [created, in_progress, completed, cancelled]
          example: "created"
        total_amount:
          type: integer
          example: 4500
        created_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"

    # ==================== ERROR SCHEMA ====================
    Error:
      type: object
      properties:
        detail:
          type: string
          description: Описание ошибки
          example: "User already exists"
      required:
        - detail
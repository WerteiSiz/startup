# StudentPass — Backend Architecture (MVP v1)

## Проект: Платформа студенческих скидок на досуг (кафе, кино, музеи, доставка)

**Команда:** 4

---
**Описание проекта:**

StudentPass — единая платформа для студентов Москвы, которая собирает проверенные скидки на досуг (кафе, кино, музеи, доставка) в одном месте. Пользователь получает доступ к актуальным предложениям, фильтрации по метро и категориям, а также может сохранять скидки в избранное и активировать их с помощью промокода или QR-кода.

**Цель MVP:**

Создать работающий backend для веб-приложения и мобильных клиентов, обеспечивающий:

- регистрацию и аутентификацию пользователей
- верификацию студенческого статуса
- управление каталогом скидок и партнеров
- поиск и фильтрацию предложений
- функционал избранного и активации скидок
- базовую админку для управления контентом

**Технические ограничения MVP:**

- Фокус на стабильность и простоту
- Реляционная база данных (PostgreSQL)
- REST API
- Без сложных микросервисов

## 3. Схема базы данных

### 3.1. PostgreSQL (реляционная модель)

```sql
-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(50), -- 'email', 'photo', 'gosuslugi'
    role VARCHAR(50) DEFAULT 'user', -- 'user', 'admin', 'partner_admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Партнеры (кафе, кино, музеи)
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL, -- 'cinema', 'cafe', 'museum', 'food_delivery', etc.
    address TEXT,
    metro_station VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    logo_url TEXT,
    contact_person VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Скидки
CREATE TABLE discounts (
    id SERIAL PRIMARY KEY,
    partner_id INTEGER REFERENCES partners(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    discount_type VARCHAR(50) NOT NULL, -- 'percentage', 'fixed_amount', 'promo_code'
    discount_value INTEGER NOT NULL, -- процент (20) или сумма (500)
    promo_code VARCHAR(100), -- если тип promo_code
    qr_code_url TEXT, -- если генерируем QR
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    usage_limit INTEGER, -- общий лимит активаций (NULL = без лимита)
    per_user_limit INTEGER DEFAULT 1, -- сколько раз может активировать один пользователь
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    terms TEXT, -- условия применения
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Избранное
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    discount_id INTEGER REFERENCES discounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, discount_id)
);

-- Активации скидок (история использования)
CREATE TABLE discount_uses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    discount_id INTEGER REFERENCES discounts(id) ON DELETE CASCADE,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, discount_id) -- защита от дублей (можно снять, если per_user_limit > 1)
);

-- Отзывы
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    discount_id INTEGER REFERENCES discounts(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Сессии (для JWT refresh токенов)
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(512) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


```

================================================================================
                              КЛАССЫ МОДЕЛЕЙ
================================================================================

┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│        User         │       │      Partner        │       │      Discount       │
├─────────────────────┤       ├─────────────────────┤       ├─────────────────────┤
│ id: int             │       │ id: int             │       │ id: int             │
│ email: str          │       │ name: str           │◄──────│ partner_id: int     │
│ password_hash: str  │       │ description: str    │       │ title: str          │
│ full_name: str      │       │ category: str       │       │ description: str    │
│ phone: str          │       │ address: str        │       │ discount_type: str  │
│ is_verified: bool   │       │ metro_station: str  │       │ discount_value: int │
│ role: str           │       │ logo_url: str       │       │ promo_code: str     │
│ created_at: datetime│       │ is_active: bool     │       │ qr_code_url: str    │
│ updated_at: datetime│       │ created_at: datetime│       │ valid_from: date    │
└─────────────────────┘       │ updated_at: datetime│       │ valid_to: date      │
         │                    └─────────────────────┘       │ usage_limit: int    │
         │                                                   │ per_user_limit: int │
         ├───────────────────────────────────────────────────│ used_count: int     │
         │                                                   │ is_active: bool     │
         │                                                   │ terms: str          │
┌────────┴───────────────┐       ┌─────────────────────┐       │ created_at: datetime│
│        Favorite        │       │     DiscountUse     │       │ updated_at: datetime│
├────────────────────────┤       ├─────────────────────┤       └─────────────────────┘
│ id: int                │       │ id: int             │                  │
│ user_id: int           │       │ user_id: int        │                  │
│ discount_id: int       │       │ discount_id: int    │◄─────────────────┘
│ created_at: datetime   │       │ used_at: datetime   │
└────────────────────────┘       └─────────────────────┘


┌─────────────────────┐
│       Review        │
├─────────────────────┤
│ id: int             │
│ user_id: int        │
│ discount_id: int    │
│ rating: int         │
│ comment: str        │
│ created_at: datetime│
│ updated_at: datetime│
└─────────────────────┘


================================================================================
                              СЕРВИСЫ (Services)
================================================================================

┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│      AuthService        │  │    DiscountService      │  │     PartnerService      │
├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────────┤
│ + register()            │  │ + get_list()            │  │ + get_list()            │
│ + login()               │  │ + get_by_id()           │  │ + get_by_id()           │
│ + logout()              │  │ + create()              │  │ + create()              │
│ + refresh_token()       │  │ + update()              │  │ + update()              │
│ + verify_student()      │  │ + delete()              │  │ + delete()              │
│ + get_profile()         │  │ + activate()            │  │ + get_discounts()       │
│ + update_profile()      │  │ + add_to_favorites()    │  │                         │
│                         │  │ + remove_from_favorites()│  └─────────────────────────┘
│                         │  │ + get_favorites()       │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│    AnalyticsService     │  │      AdminService       │
├─────────────────────────┤  ├─────────────────────────┤
│ + get_stats()           │  │ + moderate_user()       │
│ + get_partner_report()  │  │ + moderate_discount()   │
│ + get_user_activity()   │  │ + get_all_users()       │
└─────────────────────────┘  │ + get_all_partners()    │
                             └─────────────────────────┘


## 5. API Endpoints (MVP)

### 5.1. Auth (аутентификация)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Регистрация | No |
| POST | `/api/v1/auth/login` | Вход (email + password) | No |
| POST | `/api/v1/auth/logout` | Выход | Yes |
| POST | `/api/v1/auth/refresh` | Обновление токена | Yes (refresh) |
| GET | `/api/v1/auth/me` | Получить профиль | Yes |
| PUT | `/api/v1/auth/me` | Обновить профиль | Yes |
| POST | `/api/v1/auth/verify` | Запросить верификацию студента | Yes |

---

### 5.2. Discounts (скидки)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/discounts` | Список скидок (с фильтрами) | No/Optional |
| GET | `/api/v1/discounts/{id}` | Детали скидки | No/Optional |
| POST | `/api/v1/discounts/{id}/activate` | Активировать скидку (получить код/QR) | Yes |
| GET | `/api/v1/discounts/categories` | Список категорий | No |
| GET | `/api/v1/discounts/nearby` | Скидки рядом (геолокация) | No |

**Параметры фильтрации для GET /discounts:**

| Параметр | Описание |
|----------|---------|
| `category` | фильтр по категории |
| `metro` | фильтр по метро |
| `sort` | сортировка (`newest`, `popular`, `ending_soon`) |
| `page` | пагинация |
| `limit` | количество на странице |

---

### 5.3. Favorites (избранное)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/favorites` | Список избранных скидок | Yes |
| POST | `/api/v1/favorites/{discount_id}` | Добавить в избранное | Yes |
| DELETE | `/api/v1/favorites/{discount_id}` | Удалить из избранного | Yes |

---

### 5.4. Partners (партнеры)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/partners` | Список партнеров | No |
| GET | `/api/v1/partners/{id}` | Детали партнера | No |
| GET | `/api/v1/partners/{id}/discounts` | Скидки партнера | No |

---

### 5.5. Reviews (отзывы)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/discounts/{discount_id}/reviews` | Отзывы к скидке | No |
| POST | `/api/v1/discounts/{discount_id}/reviews` | Оставить отзыв | Yes |
| DELETE | `/api/v1/reviews/{id}` | Удалить отзыв | Yes (owner/admin) |

---

### 5.6. Admin (администрирование)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/admin/users` | Список пользователей | Admin |
| PUT | `/api/v1/admin/users/{id}/verify` | Верифицировать студента | Admin |
| POST | `/api/v1/admin/partners` | Создать партнера | Admin |
| POST | `/api/v1/admin/discounts` | Создать скидку | Admin |
| PUT | `/api/v1/admin/discounts/{id}` | Редактировать скидку | Admin |
| DELETE | `/api/v1/admin/discounts/{id}` | Удалить скидку | Admin |
| GET | `/api/v1/admin/analytics` | Статистика платформы | Admin |

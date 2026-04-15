-- postgres/init.sql
-- Создаем отдельные БД для каждого сервиса
CREATE DATABASE users_db;
CREATE DATABASE orders_db;

-- Включаем расширение для UUID в каждой БД
\c users_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

\c orders_db;  
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
<script setup>
import SitePublicHeader from '../components/SitePublicHeader.vue'
import { useAuthModal } from '../composables/useAuthModal'

const { openRegister } = useAuthModal()

const problemCards = [
  {
    title: 'Студенты переплачивают',
    text: 'Кафе, кино, такси, подписки - все дорого. Стипендия в РФ 3 801 ₽, а расходы студента - 15-20 тыс/мес.',
  },
  {
    title: 'Скидки сложно получить',
    text: 'Многие сервисы требуют зарубежные email или верификацию, которую не пройти из России.',
  },
  {
    title: 'Информация разрознена',
    text: 'Часы поиска скидок по сайтам, Telegram-чатам и форумам. Единого места для всех предложений нет.',
  },
]

const popular = [
  { title: 'Adobe Creative Cloud', tag: 'Хит', price: '8 000 ₽/год', old: '20 000 ₽/год' },
  { title: 'Figma Education', tag: 'Бесплатно', price: 'Бесплатно', old: '18 000 ₽/год' },
  { title: 'JetBrains All Products', tag: 'Бесплатно', price: 'Бесплатно', old: '30 000 ₽/год' },
  { title: 'ChatGPT Plus', tag: 'Хит', price: '1 000 ₽/мес', old: '2 000 ₽/мес' },
  { title: 'Microsoft 365 Education', tag: 'Бесплатно', price: 'Бесплатно', old: '5 000 ₽/год' },
  { title: 'Cursor Pro', tag: 'Бесплатно', price: 'Бесплатно', old: '20 $/мес' },
]

const benefits = [
  { title: 'Единый каталог', text: 'Все студенческие скидки в одном месте. Фильтрация по категориям и типу ПО.' },
  { title: 'Только легальные скидки', text: 'Мы работаем только с официальными партнерскими программами.' },
  { title: 'Быстрая верификация', text: 'Помогаем пройти верификацию для зарубежных сервисов с учетом российских реалий.' },
  { title: 'Безопасно и надежно', text: 'Только проверенные источники и официальные каналы получения лицензий.' },
]
</script>

<template>
  <div class="sp-page">
    <section class="sp-shell">
      <SitePublicHeader />

      <section class="sp-hero sp-container">
        <div>
          <span class="sp-badge">Новый сезон скидок 2025-2026</span>
          <h1>Профессиональный софт и AI<br />по студенческой цене</h1>
          <p class="sp-muted">
            StudentPass — единая платформа, где студенты IT и дизайна находят
            легальные скидки до 100% на Adobe, Figma, JetBrains, ChatGPT и десятки
            других сервисов.
          </p>
          <div class="sp-actions">
            <button type="button" class="sp-btn" @click="openRegister">Регистрация</button>
            <a class="sp-btn sp-btn--ghost" href="#">Как это работает</a>
          </div>
          <p class="sp-students">450 000+ студентов могут воспользоваться</p>
        </div>
        <div class="sp-hero-visual">
          <span>Студенты за ноутбуками</span>
        </div>
      </section>

      <section class="sp-stats sp-container">
        <article><strong>450K+</strong><span>Студентов в сегменте</span></article>
        <article><strong>16+</strong><span>Партнерских сервисов</span></article>
        <article><strong>до 100%</strong><span>Размер скидки</span></article>
        <article><strong>₽0</strong><span>Стоимость доступа</span></article>
      </section>
    </section>

    <section class="sp-section sp-container">
      <p class="sp-section-tag">Проблема</p>
      <h2>Студенческая жизнь стоит дорого</h2>
      <p class="sp-muted sp-center">
        От кафе до подписок, от такси до учебных материалов — все требует денег.
        StudentPass помогает экономить.
      </p>
      <div class="sp-problems">
        <article v-for="card in problemCards" :key="card.title" class="sp-problem-card">
          <h3>{{ card.title }}</h3>
          <p>{{ card.text }}</p>
        </article>
      </div>
    </section>

    <section class="sp-section sp-container">
      <div class="sp-catalog-head">
        <div>
          <p class="sp-section-tag">Каталог</p>
          <h2>Популярные скидки</h2>
        </div>
        <a href="#">Смотреть все</a>
      </div>
      <div class="sp-catalog-grid">
        <article v-for="item in popular" :key="item.title" class="sp-product-card">
          <div class="sp-product-top">
            <h3>{{ item.title }}</h3>
            <span>{{ item.tag }}</span>
          </div>
          <p class="sp-product-desc">Короткое описание предложения и преимуществ для студента.</p>
          <div class="sp-product-bottom">
            <div>
              <small>{{ item.old }}</small>
              <strong>{{ item.price }}</strong>
            </div>
            <a href="#">Получить</a>
          </div>
        </article>
      </div>
    </section>

    <section class="sp-section sp-container sp-why">
      <div class="sp-why-image">Студенты сотрудничают</div>
      <div>
        <p class="sp-section-tag">Почему мы</p>
        <h2>Решение всех проблем в одном месте</h2>
        <div class="sp-benefits">
          <article v-for="item in benefits" :key="item.title" class="sp-benefit-card">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="sp-section sp-container">
      <div class="sp-cta">
        <h2>Начни экономить прямо сейчас</h2>
        <p>Воспользуйся скидками на профессиональный ПО и AI-инструменты, пока ты студент.</p>
        <RouterLink class="sp-btn" :to="{ name: 'catalog' }">Открыть каталог скидок</RouterLink>
      </div>
    </section>

    <footer class="sp-footer">
      <div class="sp-container sp-footer-grid">
        <div>
          <div class="sp-logo">StudentPass</div>
          <p class="sp-muted">
            Единая платформа студенческих скидок на профессиональный софт и AI-сервисы.
          </p>
        </div>
        <div>
          <h4>Навигация</h4>
          <RouterLink :to="{ name: 'home' }">Главная</RouterLink>
          <RouterLink :to="{ name: 'catalog' }">Каталог скидок</RouterLink>
          <RouterLink :to="{ name: 'how' }">Как это работает</RouterLink>
        </div>
        <div>
          <h4>Категории</h4>
          <a href="#">AI-инструменты</a>
          <a href="#">Дизайн</a>
          <a href="#">Разработка</a>
          <a href="#">Продуктивность</a>
        </div>
      </div>
    </footer>
  </div>
</template>

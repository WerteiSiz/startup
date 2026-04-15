<script setup>
import { RouterLink } from 'vue-router'
import SitePublicHeader from '../components/SitePublicHeader.vue'

const timelineSteps = [
  {
    side: 'left',
    label: 'Шаг 01',
    tone: 'purple',
    title: 'Выбери нужный сервис',
    text: 'Открой каталог и найди нужный софт или AI-сервис. Используй поиск, категории и фильтр «только бесплатные».',
    icon: 'search',
  },
  {
    side: 'right',
    label: 'Шаг 02',
    tone: 'blue',
    title: 'Подтверди статус студента',
    text: 'Большинство партнёров принимают edu-почту, SheerID или GitHub Student Pack. Мы подскажем, какой способ подходит именно тебе.',
    icon: 'cap',
  },
  {
    side: 'left',
    label: 'Шаг 03',
    tone: 'green',
    title: 'Получи скидку легально',
    text: 'После верификации получаешь бесплатную или сильно сниженную лицензию прямо от компании. Никаких посредников и пиратства.',
    icon: 'check',
  },
  {
    side: 'right',
    label: 'Шаг 04',
    tone: 'orange',
    title: 'Пользуйся и учись',
    text: 'Используй профессиональные инструменты для учёбы, фриланса и проектов. Продляй лицензию каждый год, пока ты студент.',
    icon: 'download',
  },
]

const whyCards = [
  {
    title: 'Экономия 50 000+ ₽/год',
    text: 'Среднегодовая экономия студента на лицензиях при использовании всех доступных скидок.',
    icon: 'bolt',
  },
  {
    title: 'Конкурентное преимущество',
    text: 'Профессиональный стек инструментов выделяет тебя среди других кандидатов при поиске работы.',
    icon: 'trophy',
  },
  {
    title: 'Поддержка и инструкции',
    text: 'Подробные гайды по верификации для каждого сервиса с учётом российских реалий 2025.',
    icon: 'bubble',
  },
]

const faqTwo = [
  {
    q: 'Для кого работает StudentPass?',
    a: 'Для студентов IT, дизайнерских и инженерных специальностей вузов и колледжей России. Нужна действующая студенческая карта или edu-почта.',
  },
  {
    q: 'Это законно?',
    a: 'Абсолютно. Мы работаем только с официальными студенческими программами компаний. Adobe, JetBrains, Microsoft и другие имеют специальные условия для образовательных учреждений.',
  },
]

const faqGrid = [
  {
    q: 'Что делать, если у меня нет edu-почты?',
    a: 'Многие сервисы принимают студенческий билет через SheerID. Мы помогаем разобраться с альтернативными способами верификации для каждого конкретного сервиса.',
  },
  {
    q: 'Как долго действуют скидки?',
    a: 'Обычно один год с ежегодным продлением. Пока ты студент — скидки действуют. Некоторые сервисы дают лицензию на весь период обучения.',
  },
  {
    q: 'Что делать с зарубежными сервисами в условиях санкций?',
    a: 'Это наша специализация. Мы даём конкретные инструкции по оплате и верификации для российских студентов, включая альтернативные способы оплаты.',
  },
  {
    q: 'Сколько стоит StudentPass?',
    a: 'Использование платформы абсолютно бесплатно для студентов. Мы зарабатываем на партнёрских комиссиях от компаний, не с пользователей.',
  },
]

const tamSamSom = [
  {
    label: 'TAM',
    value: '45 млрд ₽',
    sub: 'Весь рынок образовательного ПО в РФ — 1,5 млн студентов',
  },
  {
    label: 'SAM',
    value: '13,5 млрд ₽',
    sub: 'IT и дизайн — 450 000 студентов × 30 000 ₽ / год',
  },
  {
    label: 'SOM',
    value: '540 млн ₽',
    sub: 'Цель на 3-й год — 4% SAM — 90 000 пользователей',
  },
]
</script>

<template>
  <div class="how-page">
    <SitePublicHeader />

    <main class="how-main cat-container">
      <section class="how-hero">
        <p class="how-eyebrow">Инструкция</p>
        <h1 class="how-title">Как это работает</h1>
        <p class="how-lead">
          Получить студенческую скидку легально — проще, чем кажется. Вот 4 простых шага.
        </p>
      </section>

      <div class="how-timeline">
        <div class="how-timeline__line" aria-hidden="true" />
        <div
          v-for="step in timelineSteps"
          :key="step.label"
          class="how-step"
          :class="[`how-step--${step.side}`, `how-step--tone-${step.tone}`]"
        >
          <div class="how-step__icon" :class="`how-step__icon--${step.tone}`">
            <svg v-if="step.icon === 'search'" class="how-step__svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" />
              <path d="M16 16l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
            <svg v-else-if="step.icon === 'cap'" class="how-step__svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path
                d="M12 4L4 8l8 4 8-4-8-4zM4 13v4l8 4 8-4v-4"
                stroke="currentColor"
                stroke-width="2"
                stroke-linejoin="round"
              />
            </svg>
            <svg v-else-if="step.icon === 'check'" class="how-step__svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M6 12l4 4 8-8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <svg v-else-if="step.icon === 'download'" class="how-step__svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M12 4v11m0 0l4-4m-4 4L8 11M4 19h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </div>
          <div class="how-step__card">
            <span class="how-step__badge">{{ step.label }}</span>
            <h2 class="how-step__title">{{ step.title }}</h2>
            <p class="how-step__text">{{ step.text }}</p>
          </div>
        </div>
      </div>

      <h2 class="how-section-title how-section-title--center">Зачем это нужно?</h2>

      <section class="how-why-grid">
        <article v-for="card in whyCards" :key="card.title" class="how-why-card">
          <div class="how-why-card__icon" aria-hidden="true">
            <svg v-if="card.icon === 'bolt'" viewBox="0 0 24 24" fill="none">
              <path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
            </svg>
            <svg v-else-if="card.icon === 'trophy'" viewBox="0 0 24 24" fill="none">
              <path d="M6 4h12v3a4 4 0 01-4 4H10a4 4 0 01-4-4V4zM9 22h6M12 11v11" stroke="currentColor" stroke-width="2" />
              <path d="M4 4H2v2a4 4 0 004 4M20 4h2v2a4 4 0 01-4 4" stroke="currentColor" stroke-width="2" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none">
              <path d="M6 8h12v10H6V8zM9 8V6a3 3 0 013-3 3 3 0 013 3v2" stroke="currentColor" stroke-width="2" />
            </svg>
          </div>
          <h3>{{ card.title }}</h3>
          <p>{{ card.text }}</p>
        </article>
      </section>

      <h2 class="how-section-title how-section-title--center how-faq-title">Часто задаваемые вопросы</h2>

      <section class="how-faq-row">
        <article v-for="item in faqTwo" :key="item.q" class="how-faq-card">
          <h3>{{ item.q }}</h3>
          <p>{{ item.a }}</p>
        </article>
      </section>

      <section class="how-faq-grid">
        <article v-for="item in faqGrid" :key="item.q" class="how-faq-card">
          <h3>{{ item.q }}</h3>
          <p>{{ item.a }}</p>
        </article>
      </section>

      <section class="how-market">
        <h2 class="how-market__title">Рынок StudentPass: TAM / SAM / SOM</h2>
        <div class="how-market__row">
          <article v-for="cell in tamSamSom" :key="cell.label" class="how-market__cell">
            <span class="how-market__label">{{ cell.label }}</span>
            <strong>{{ cell.value }}</strong>
            <p>{{ cell.sub }}</p>
          </article>
        </div>
      </section>

      <section class="how-cta-wrap">
        <p class="how-cta-text">
          Готов сэкономить? Открой каталог и найди нужную скидку прямо сейчас.
        </p>
        <RouterLink class="how-cta-btn" :to="{ name: 'catalog' }">Открыть каталог →</RouterLink>
      </section>
    </main>

    <button type="button" class="how-fab" aria-label="Помощь">?</button>
  </div>
</template>

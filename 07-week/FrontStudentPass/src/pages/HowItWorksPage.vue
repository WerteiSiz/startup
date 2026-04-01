<script setup>
const steps = [
  {
    id: 1,
    side: "left",
    title: "Выбери нужный сервис",
    description:
      "Открой каталог StudentPass и найди нужный инструмент - Adobe, JetBrains, ChatGPT или любой другой. Фильтруй по категориям или используй поиск.",
    icon: "⌕",
    badge: "ШАГ 01",
    color: "from-violet-500 to-fuchsia-500",
    badgeColor: "bg-violet-500/20 text-violet-200",
  },
  {
    id: 2,
    side: "right",
    title: "Подтверди статус студента",
    description:
      "Большинство сервисов требуют подтверждение через edu-почту или платформы SheerID / GitHub Student Pack. Мы даем инструкцию для каждого сервиса.",
    icon: "◉",
    badge: "ШАГ 02",
    color: "from-cyan-500 to-sky-500",
    badgeColor: "bg-cyan-500/20 text-cyan-200",
  },
  {
    id: 3,
    side: "left",
    title: "Получи скидку легально",
    description:
      "После верификации получаешь бесплатную или сильно сниженную лицензию прямо от компании. Никаких посредников и пиратства.",
    icon: "◎",
    badge: "ШАГ 03",
    color: "from-emerald-500 to-teal-500",
    badgeColor: "bg-emerald-500/20 text-emerald-200",
  },
  {
    id: 4,
    side: "right",
    title: "Пользуйся и учись",
    description:
      "Используй профессиональные инструменты для учебы, фриланса и проектов. Продляй лицензию, пока ты студент.",
    icon: "↓",
    badge: "ШАГ 04",
    color: "from-amber-500 to-orange-500",
    badgeColor: "bg-amber-500/20 text-amber-200",
  },
];

const benefits = [
  {
    id: 1,
    icon: "⚡",
    title: "Экономия 50 000+ ₽/год",
    description: "Среднегодовая экономия студента на лицензиях при использовании доступных скидок.",
  },
  {
    id: 2,
    icon: "⌛",
    title: "Конкурентное преимущество",
    description: "Профессиональный стек инструментов выделяет тебя среди других кандидатов при поиске работы.",
  },
  {
    id: 3,
    icon: "◌",
    title: "Поддержка и инструкции",
    description: "Подробные гайды по верификации для каждого сервиса с учетом российских реалий.",
  },
];

const faqs = [
  {
    id: 1,
    q: "Для кого работает StudentPass?",
    a: "Для студентов IT, дизайнерских и инженерных специальностей вузов и колледжей России. Нужна действующая студенческая карта или edu-почта.",
  },
  {
    id: 2,
    q: "Это законно?",
    a: "Абсолютно. Мы работаем только с официальными студенческими программами компаний. Adobe, JetBrains, Microsoft и другие имеют специальные условия для образовательных учреждений.",
  },
  {
    id: 3,
    q: "Что делать, если у меня нет edu-почты?",
    a: "Многие сервисы принимают студенческий билет через SheerID. Мы поможем разобраться с альтернативными способами верификации для каждого конкретного сервиса.",
  },
  {
    id: 4,
    q: "Как долго действуют скидки?",
    a: "Обычно один год с ежегодным продлением. Пока ты студент - скидки действуют. Некоторые сервисы дают лицензию на весь период обучения.",
  },
  {
    id: 5,
    q: "Что делать с зарубежными сервисами в условиях санкций?",
    a: "Это наша специализация. Мы даем конкретные инструкции по оплате и верификации для российских студентов, включая альтернативные способы оплаты.",
  },
  {
    id: 6,
    q: "Сколько стоит StudentPass?",
    a: "Использование платформы абсолютно бесплатно для студентов. Мы зарабатываем на партнерских комиссиях от компаний, не с пользователей.",
  },
];

const market = [
  { id: 1, label: "TAM", value: "45 млрд ₽", note: "Весь рынок образовательного ПО в РФ - 1,5 млн студентов" },
  { id: 2, label: "SAM", value: "13,5 млрд ₽", note: "IT и дизайн - 450 000 студентов × 30 000 ₽/год" },
  { id: 3, label: "SOM", value: "540 млн ₽", note: "Цель на 3-й год - 4% SAM - 90 000 пользователей" },
];
</script>

<template>
  <main class="mx-auto flex w-full max-w-7xl flex-col gap-14 px-4 py-10 md:px-8 md:py-14">
    <section class="pt-4 text-center">
      <p class="text-sm font-semibold uppercase tracking-[0.2em] text-violet-300">Инструкция</p>
      <h1 class="mt-3 text-5xl font-extrabold text-white md:text-7xl">Как это работает</h1>
      <p class="mx-auto mt-5 max-w-3xl text-2xl leading-snug text-slate-400 md:text-3xl">
        Получить студенческую скидку легально проще, чем кажется. Вот 4 простых шага.
      </p>
    </section>

    <section class="relative mx-auto w-full max-w-5xl py-2">
      <div class="pointer-events-none absolute left-1/2 top-0 hidden h-full w-px -translate-x-1/2 bg-white/10 md:block" />
      <article
        v-for="step in steps"
        :key="step.id"
        class="relative mb-8 grid gap-4 md:mb-12 md:grid-cols-2 md:items-center"
      >
        <div
          :class="[
            step.side === 'left' ? 'md:pr-16 md:text-right' : 'md:col-start-2 md:pl-16',
            'space-y-3',
          ]"
        >
          <p :class="[step.badgeColor, 'inline-flex rounded-full px-3 py-1 text-xs font-semibold']">
            {{ step.badge }}
          </p>
          <h2 class="text-3xl font-bold text-white">{{ step.title }}</h2>
          <p class="text-xl leading-relaxed text-slate-400">{{ step.description }}</p>
        </div>
        <div
          :class="[
            step.color,
            'mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br text-xl font-semibold text-white shadow-lg',
            'md:absolute md:left-1/2 md:top-1/2 md:-translate-x-1/2 md:-translate-y-1/2',
          ]"
        >
          {{ step.icon }}
        </div>
      </article>
    </section>

    <section class="space-y-6 pt-2">
      <h2 class="text-center text-5xl font-bold text-white">Зачем это нужно?</h2>
      <div class="grid gap-5 md:grid-cols-3">
        <article
          v-for="item in benefits"
          :key="item.id"
          class="rounded-2xl border border-white/10 bg-[#0b1121]/85 p-6 text-center shadow-lg shadow-black/20"
        >
          <div class="mx-auto mb-5 flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-300">
            {{ item.icon }}
          </div>
          <h3 class="text-4xl font-bold text-white">{{ item.title }}</h3>
          <p class="mt-3 text-xl leading-relaxed text-slate-400">{{ item.description }}</p>
        </article>
      </div>
    </section>

    <section class="space-y-6">
      <h2 class="text-center text-5xl font-bold text-white">Часто задаваемые вопросы</h2>
      <div class="grid gap-5 md:grid-cols-2">
        <article
          v-for="item in faqs"
          :key="item.id"
          class="rounded-2xl border border-white/10 bg-[#0b1121]/85 p-6 shadow-lg shadow-black/20"
        >
          <h3 class="text-2xl font-bold text-white">{{ item.q }}</h3>
          <p class="mt-3 text-xl leading-relaxed text-slate-400">{{ item.a }}</p>
        </article>
      </div>
    </section>

    <section class="rounded-3xl border border-white/10 bg-[#0b1121]/90 p-6 shadow-xl shadow-black/25 md:p-10">
      <h2 class="text-center text-5xl font-bold text-white">Рынок StudentPass: TAM / SAM / SOM</h2>
      <div class="mt-8 grid gap-5 md:grid-cols-3">
        <article
          v-for="item in market"
          :key="item.id"
          class="rounded-2xl border border-white/10 bg-[#121931]/80 p-6 text-center"
        >
          <p class="text-sm font-semibold uppercase tracking-[0.2em] text-violet-300">{{ item.label }}</p>
          <p class="mt-3 text-4xl font-extrabold text-white">{{ item.value }}</p>
          <p class="mt-2 text-lg text-slate-400">{{ item.note }}</p>
        </article>
      </div>
    </section>

    <section class="pb-2 text-center">
      <p class="text-xl text-slate-400">Готов сэкономить? Открой каталог и найди нужную скидку прямо сейчас.</p>
      <RouterLink
        to="/catalog"
        class="mt-6 inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 px-10 py-4 text-2xl font-semibold text-white shadow-lg shadow-fuchsia-500/30 transition hover:scale-105"
      >
        Открыть каталог
        <span aria-hidden="true">→</span>
      </RouterLink>
    </section>
  </main>
</template>

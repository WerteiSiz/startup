<script setup>
const problems = [
  {
    id: 1,
    title: "Студенты переплачивают",
    description:
      "Кафе, кино, такси, подписки - все дорого. Стипендия не покрывает регулярные траты.",
    icon: "⚠",
    bg: "from-rose-600/20 to-fuchsia-600/10",
  },
  {
    id: 2,
    title: "Скидки сложно получить",
    description:
      "Многие сервисы требуют зарубежные email.edu или верификацию, которую сложно пройти.",
    icon: "🛡",
    bg: "from-orange-500/20 to-amber-500/10",
  },
  {
    id: 3,
    title: "Информация разрознена",
    description:
      "Скидки разбросаны по сайтам и чатам. Нет единой платформы для быстрого поиска.",
    icon: "◷",
    bg: "from-yellow-500/20 to-slate-600/10",
  },
];
</script>

<template>
  <section class="space-y-8">
    <div class="text-center">
      <p class="text-sm font-semibold uppercase tracking-[0.2em] text-violet-300">Проблема</p>
      <h2 class="mt-3 text-3xl font-bold text-white md:text-5xl">Студенческая жизнь стоит дорого</h2>
    </div>

    <div class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <article
        v-for="problem in problems"
        :key="problem.id"
        :class="problem.bg"
        class="rounded-2xl border border-white/10 bg-gradient-to-br p-6 shadow-lg transition duration-300 hover:scale-[1.03] hover:border-violet-400/40 hover:shadow-xl hover:shadow-violet-500/20"
      >
        <div class="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 text-xl text-white">
          {{ problem.icon }}
        </div>
        <h3 class="text-xl font-semibold text-white">{{ problem.title }}</h3>
        <p class="mt-3 leading-relaxed text-slate-300">{{ problem.description }}</p>
      </article>
    </div>
  </section>
</template>

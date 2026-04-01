<script setup>
const advantages = [
  {
    id: 1,
    icon: "⌕",
    title: "Единый каталог",
    description: "Все студенческие скидки в одном месте. Фильтрация по категориям и типу ПО.",
  },
  {
    id: 2,
    icon: "◉",
    title: "Только легальные скидки",
    description: "Работаем с официальными партнерами. Никакого пиратства и сомнительных схем.",
  },
  {
    id: 3,
    icon: "⚡",
    title: "Быстрая верификация",
    description: "Помогаем пройти проверку для зарубежных сервисов с учетом локальных реалий.",
  },
  {
    id: 4,
    icon: "🛡",
    title: "Безопасно и надежно",
    description: "Только проверенные источники и официальные каналы получения студенческих лицензий.",
  },
];
</script>

<template>
  <section class="grid items-stretch gap-6 lg:grid-cols-2">
    <div
      class="relative min-h-[320px] overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#0b1022] via-[#161233] to-[#2a1e59]/80 p-4 shadow-xl"
    >
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,rgba(168,85,247,0.22),transparent_45%)]" />
      <p class="relative z-10 text-slate-300">Студенты сотрудничают</p>
    </div>

    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.2em] text-violet-300">Почему мы</p>
      <h2 class="mt-2 max-w-xl text-3xl font-bold text-white md:text-5xl">
        Решение всех проблем в одном месте
      </h2>

      <div class="mt-6 grid gap-4 sm:grid-cols-2">
        <article
          v-for="item in advantages"
          :key="item.id"
          class="rounded-2xl border border-white/10 bg-[#0f1424]/80 p-5 shadow-lg transition duration-300 hover:scale-[1.03] hover:border-violet-400/40 hover:shadow-xl hover:shadow-violet-500/20"
        >
          <div class="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/15 text-violet-300">
            {{ item.icon }}
          </div>
          <h3 class="text-xl font-semibold text-white">{{ item.title }}</h3>
          <p class="mt-2 text-slate-300">{{ item.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

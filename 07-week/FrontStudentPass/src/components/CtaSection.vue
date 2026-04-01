<template>
  <section class="rounded-2xl border border-white/10 bg-[#0b1020]/80 p-6 shadow-xl md:p-10">
    <div
      class="rounded-2xl border border-white/10 bg-gradient-to-r from-[#2b1d55]/55 via-[#1a1744]/45 to-[#0c2840]/40 px-6 py-10 text-center"
    >
      <h2 class="text-3xl font-bold text-white md:text-5xl">Начни экономить прямо сейчас</h2>
      <p class="mx-auto mt-4 max-w-2xl text-lg text-slate-300">
        Воспользуйся скидками на профессиональный ПО и AI-инструменты, пока ты студент.
      </p>

      <RouterLink
        to="/catalog"
        class="mt-8 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 px-8 py-3 text-lg font-semibold text-white shadow-lg shadow-fuchsia-500/35 transition duration-300 hover:scale-105 hover:shadow-xl hover:shadow-fuchsia-500/45"
      >
        Открыть каталог скидок
      </RouterLink>
    </div>
  </section>
</template>

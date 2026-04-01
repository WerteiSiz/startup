<template>
  <section class="relative overflow-hidden rounded-2xl border border-white/10 bg-[#0a0e1b]/70 p-8 shadow-xl md:p-12">
    <div
      class="pointer-events-none absolute -left-24 -top-24 h-72 w-72 rounded-full bg-purple-600/20 blur-3xl"
    />
    <div
      class="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-cyan-500/10 blur-3xl"
    />

    <div class="relative z-10 grid items-center gap-8 lg:grid-cols-2">
      <div class="space-y-6">
        <span class="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-1 text-sm text-slate-300">
          Новый сезон скидок 2025-2026
        </span>

        <h1 class="text-4xl font-extrabold leading-tight text-white md:text-6xl">
          Профессиональный
          <span class="bg-gradient-to-r from-fuchsia-400 to-blue-400 bg-clip-text text-transparent">
            софт
          </span>
          и
          <span class="bg-gradient-to-r from-fuchsia-400 to-cyan-400 bg-clip-text text-transparent">
            AI
          </span>
          по студенческой цене
        </h1>

        <p class="max-w-xl text-lg text-slate-300">
          Единая платформа, где студенты находят скидки до 100%
        </p>

        <div class="flex flex-wrap gap-4">
          <RouterLink
            to="/catalog"
            class="rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 px-6 py-3 font-semibold text-white shadow-lg shadow-fuchsia-500/30 transition duration-300 hover:scale-105 hover:shadow-xl hover:shadow-fuchsia-500/40"
          >
            Найти скидку
          </RouterLink>
          <RouterLink
            to="/how-it-works"
            class="rounded-2xl border border-white/20 bg-transparent px-6 py-3 font-semibold text-slate-100 transition duration-300 hover:scale-105 hover:border-violet-400 hover:shadow-lg hover:shadow-violet-500/20"
          >
            Как это работает
          </RouterLink>
        </div>
      </div>

      <div
        class="relative h-[320px] rounded-2xl border border-white/10 bg-gradient-to-br from-violet-700/30 via-indigo-700/20 to-cyan-500/20 shadow-xl"
      >
        <div class="absolute right-4 top-5 rounded-xl border border-cyan-300/30 bg-[#0f1426]/80 px-4 py-3 shadow-lg">
          <p class="text-sm font-semibold text-white">JetBrains All</p>
          <p class="text-sm text-emerald-400">-100% · Бесплатно</p>
        </div>
        <div class="absolute bottom-5 left-5 rounded-xl border border-fuchsia-300/30 bg-[#0f1426]/80 px-4 py-3 shadow-lg">
          <p class="text-sm font-semibold text-white">Figma Pro</p>
          <p class="text-sm text-emerald-400">Бесплатно для студентов</p>
        </div>
      </div>
    </div>
  </section>
</template>

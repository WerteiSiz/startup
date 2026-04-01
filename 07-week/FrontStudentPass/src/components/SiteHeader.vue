<template>
  <header class="sticky top-0 z-40 border-b border-white/10 bg-[#070b18]/95 backdrop-blur">
    <div class="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-4 py-4 md:px-8">
      <RouterLink to="/" class="flex items-center gap-3">
        <div class="rounded-xl bg-gradient-to-br from-violet-600 to-fuchsia-500 px-2 py-1 text-white shadow-lg shadow-violet-500/30">
          ✦
        </div>
        <p class="text-xl font-semibold text-white">StudentPass</p>
      </RouterLink>

      <nav class="flex items-center gap-2 text-sm md:text-base">
        <RouterLink
          to="/"
          class="rounded-xl px-4 py-2 text-slate-300 transition hover:bg-white/5 hover:text-white"
          active-class="bg-white/10 text-white"
          exact-active-class="bg-white/10 text-white"
        >
          Главная
        </RouterLink>
        <RouterLink
          to="/catalog"
          class="rounded-xl px-4 py-2 text-slate-300 transition hover:bg-white/5 hover:text-white"
          active-class="bg-white/10 text-white"
        >
          Каталог скидок
        </RouterLink>
        <RouterLink
          to="/how-it-works"
          class="rounded-xl px-4 py-2 text-slate-300 transition hover:bg-white/5 hover:text-white"
          active-class="bg-white/10 text-white"
        >
          Как это работает
        </RouterLink>
      </nav>

      <RouterLink
        to="/catalog"
        class="rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 px-4 py-2 font-semibold text-white shadow-lg shadow-fuchsia-500/30 transition hover:scale-105"
      >
        Найти скидку
      </RouterLink>
    </div>
  </header>
</template>

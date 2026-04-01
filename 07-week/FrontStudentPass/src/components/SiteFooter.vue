<template>
  <footer class="rounded-2xl border border-white/10 bg-[#090d1b]/90 p-6 shadow-lg md:p-8">
    <div class="grid gap-8 md:grid-cols-3">
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="rounded-xl bg-gradient-to-br from-violet-600 to-fuchsia-500 p-2 text-white shadow-lg shadow-violet-500/30">
            ✦
          </div>
          <p class="text-2xl font-semibold text-white">StudentPass</p>
        </div>
        <p class="max-w-sm text-slate-300">
          Единая платформа студенческих скидок на профессиональный софт и AI-сервисы.
        </p>
        <div class="flex gap-2 text-slate-300">
          <button class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 transition hover:border-violet-400/50 hover:text-white">
            ↗
          </button>
          <button class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 transition hover:border-violet-400/50 hover:text-white">
            ✈
          </button>
        </div>
      </div>

      <div>
        <h3 class="text-xl font-semibold text-white">Навигация</h3>
        <ul class="mt-4 space-y-2 text-slate-300">
          <li><RouterLink class="transition hover:text-cyan-300" to="/">Главная</RouterLink></li>
          <li><RouterLink class="transition hover:text-cyan-300" to="/catalog">Каталог скидок</RouterLink></li>
          <li><RouterLink class="transition hover:text-cyan-300" to="/how-it-works">Как это работает</RouterLink></li>
        </ul>
      </div>

      <div>
        <h3 class="text-xl font-semibold text-white">Категории</h3>
        <ul class="mt-4 space-y-2 text-slate-300">
          <li>AI-инструменты</li>
          <li>Дизайн</li>
          <li>Разработка</li>
          <li>Продуктивность</li>
          <li>Офис</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 border-t border-white/10 pt-4 text-sm text-slate-400 md:flex md:items-center md:justify-between">
      <p>© 2025 StudentPass. Команда №4 - Стартап в ИТ.</p>
      <p>Сделано с ♡ для студентов РФ</p>
    </div>
  </footer>
</template>

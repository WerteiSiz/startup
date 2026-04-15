<script setup>
import { RouterLink } from 'vue-router'
import AuthHeaderActions from './AuthHeaderActions.vue'
</script>

<template>
  <header class="site-header">
    <div class="site-header__inner">
      <RouterLink :to="{ name: 'home' }" class="site-header__logo">
        <span class="site-header__logo-mark" aria-hidden="true">⚡</span>
        <span>StudentPass</span>
      </RouterLink>
      <nav class="site-header__nav" aria-label="Основное меню">
        <RouterLink :to="{ name: 'home' }" active-class="is-active">Главная</RouterLink>
        <RouterLink :to="{ name: 'catalog' }" active-class="is-active">Каталог скидок</RouterLink>
        <RouterLink :to="{ name: 'how' }" active-class="is-active">Как это работает</RouterLink>
      </nav>
      <AuthHeaderActions />
    </div>
  </header>
</template>

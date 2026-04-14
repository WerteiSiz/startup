<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
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
</template>

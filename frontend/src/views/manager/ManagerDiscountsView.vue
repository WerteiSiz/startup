<script setup>
import { RouterLink } from 'vue-router'
import { useManagerDiscounts } from '../../composables/useManagerDiscounts'

const { items: managerDiscounts, deleteDiscount } = useManagerDiscounts()

function handleDelete(id) {
  deleteDiscount(id)
}
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head admin-page-head--row">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--blue mgr-title-cube" aria-hidden="true" />
        <div>
          <h1>Мои скидки</h1>
          <p>Управление предложениями вашей компании</p>
        </div>
      </div>
      <RouterLink :to="{ name: 'manager-discount-create' }" class="admin-btn admin-btn--primary">
        + Создать скидку
      </RouterLink>
    </header>

    <section class="mgr-discount-grid">
      <article v-for="card in managerDiscounts" :key="card.id" class="mgr-discount-card">
        <div class="mgr-discount-card__top">
          <span class="mgr-discount-emoji" aria-hidden="true">{{ card.emoji }}</span>
          <div class="mgr-discount-tools">
            <RouterLink
              :to="{ name: 'manager-discount-edit', params: { id: card.id } }"
              class="admin-icon-btn"
              aria-label="Редактировать"
            >
              ✎
            </RouterLink>
            <button
              type="button"
              class="admin-icon-btn admin-icon-btn--danger"
              aria-label="Удалить"
              @click="handleDelete(card.id)"
            >
              🗑
            </button>
          </div>
        </div>
        <h2>{{ card.title }}</h2>
        <p class="mgr-discount-desc">{{ card.description }}</p>
        <div class="mgr-discount-tags">
          <span class="mgr-tag mgr-tag--percent">{{ card.percent }}</span>
          <span class="mgr-tag mgr-tag--cat">{{ card.category }}</span>
        </div>
        <div class="mgr-discount-stats">
          <span>👁 Просмотры: {{ card.views }}</span>
          <span>📈 Клики: {{ card.clicks }}</span>
        </div>
      </article>
    </section>
  </div>
</template>

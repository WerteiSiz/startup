<script setup>
import { computed, ref } from 'vue'
import { applications } from '../../data/adminMock'

const filter = ref('all')

const filterOptions = [
  { key: 'all', label: 'Все' },
  { key: 'pending', label: 'На рассмотрении' },
  { key: 'approved', label: 'Одобренные' },
  { key: 'rejected', label: 'Отклоненные' },
]

const visible = computed(() => {
  if (filter.value === 'all') return applications
  return applications.filter((a) => a.status === filter.value)
})

const statusLabel = (s) => {
  if (s === 'pending') return 'На рассмотрении'
  if (s === 'approved') return 'Одобрена'
  return 'Отклонена'
}

const statusClass = (s) => {
  if (s === 'pending') return 'admin-badge--warn'
  if (s === 'approved') return 'admin-badge--ok'
  return 'admin-badge--bad'
}
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--doc" aria-hidden="true" />
        <div>
          <h1>Заявки компаний</h1>
          <p>Управление заявками на партнерство</p>
        </div>
      </div>
    </header>

    <div class="admin-filter-bar">
      <span class="admin-filter-label">Фильтр:</span>
      <div class="admin-filter-chips">
        <button
          v-for="opt in filterOptions"
          :key="opt.key"
          type="button"
          class="admin-chip"
          :class="{ 'is-active': filter === opt.key }"
          @click="filter = opt.key"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="admin-app-list">
      <article v-for="app in visible" :key="app.id" class="admin-app-card">
        <div class="admin-app-card__head">
          <div>
            <h2>{{ app.company }}</h2>
            <span class="admin-badge" :class="statusClass(app.status)">{{ statusLabel(app.status) }}</span>
          </div>
          <div v-if="app.status === 'pending'" class="admin-app-actions">
            <button type="button" class="admin-btn admin-btn--ok">✓ Одобрить</button>
            <button type="button" class="admin-btn admin-btn--bad">✕ Отклонить</button>
          </div>
        </div>

        <div class="admin-app-grid">
          <div>
            <span class="admin-k">Контактное лицо</span>
            <p>{{ app.contact }}</p>
          </div>
          <div>
            <span class="admin-k">Должность</span>
            <p>{{ app.position }}</p>
          </div>
          <div>
            <span class="admin-k">Email</span>
            <p>✉ {{ app.email }}</p>
          </div>
          <div>
            <span class="admin-k">Телефон</span>
            <p>☎ {{ app.phone }}</p>
          </div>
        </div>

        <div class="admin-app-offer">
          <span class="admin-k">Предложение:</span>
          <p>{{ app.offer }}</p>
        </div>

        <footer class="admin-app-meta">
          <span>Подана: {{ app.submitted }}</span>
          <span v-if="app.status === 'approved'" class="meta-ok">Одобрена: {{ app.resolved }}</span>
          <span v-if="app.status === 'rejected'" class="meta-bad">
            Отклонена: {{ app.resolved }} ({{ app.reason }})
          </span>
        </footer>
      </article>
    </div>
  </div>
</template>

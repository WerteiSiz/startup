<script setup>
import { RouterLink } from 'vue-router'
import {
  dashboardStats,
  pendingSidebar,
  quickNav,
  recentActivity,
  topCompanies,
} from '../../data/adminMock'
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--orange" aria-hidden="true" />
        <div>
          <h1>Панель администратора</h1>
          <p>Управление платформой StudentPass</p>
        </div>
      </div>
    </header>

    <section class="admin-stat-grid">
      <article v-for="s in dashboardStats" :key="s.label" class="admin-stat-card" :class="`tone-${s.tone}`">
        <span class="admin-stat-icon" :class="`ic-${s.icon}`" aria-hidden="true" />
        <div>
          <strong>{{ s.value }}</strong>
          <span>{{ s.label }}</span>
        </div>
      </article>
    </section>

    <div class="admin-two-col">
      <section class="admin-panel">
        <h2>Последняя активность</h2>
        <ul class="admin-activity">
          <li v-for="(a, i) in recentActivity" :key="i" class="admin-activity__item">
            <span class="admin-activity__dot" :class="`dot-${a.tone}`" />
            <div>
              <p>{{ a.text }}</p>
              <time>{{ a.time }}</time>
            </div>
          </li>
        </ul>
      </section>

      <section class="admin-panel">
        <div class="admin-panel-head">
          <h2>Заявки на рассмотрении</h2>
          <RouterLink :to="{ name: 'admin-applications' }" class="admin-link-all">Все →</RouterLink>
        </div>
        <div class="admin-pending-list">
          <article v-for="p in pendingSidebar" :key="p.company" class="admin-pending-card">
            <div class="admin-pending-head">
              <strong>{{ p.company }}</strong>
              <span class="admin-badge admin-badge--pending">⏱ На рассмотрении</span>
            </div>
            <p class="admin-pending-contact">{{ p.contact }}</p>
            <p class="admin-pending-offer">{{ p.offer }}</p>
            <time>{{ p.date }}</time>
          </article>
        </div>
      </section>
    </div>

    <section class="admin-panel">
      <div class="admin-panel-head">
        <h2>Топ компаний по кликам</h2>
        <RouterLink :to="{ name: 'admin-statistics' }" class="admin-link-all">Подробная статистика →</RouterLink>
      </div>
      <div class="admin-table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Компания</th>
              <th>Клики</th>
              <th>Уникальные</th>
              <th>CTR</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in topCompanies" :key="row.company">
              <td>{{ row.company }}</td>
              <td>{{ row.clicks }}</td>
              <td>{{ row.unique }}</td>
              <td class="admin-ctr">{{ row.ctr }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="admin-quick-grid">
      <RouterLink v-for="q in quickNav" :key="q.title" :to="q.to" class="admin-quick-card" :class="`tone-${q.tone}`">
        <strong>{{ q.title }}</strong>
        <span>{{ q.desc }}</span>
      </RouterLink>
    </section>
  </div>
</template>

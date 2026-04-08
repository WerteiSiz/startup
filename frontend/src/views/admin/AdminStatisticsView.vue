<script setup>
import { statisticsSummary, statisticsTable } from '../../data/adminMock'
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head admin-page-head--row">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--green" aria-hidden="true" />
        <div>
          <h1>Статистика</h1>
          <p>Аналитика кликов и активности пользователей</p>
        </div>
      </div>
      <button type="button" class="admin-btn admin-btn--primary">⬇ Скачать отчет</button>
    </header>

    <section class="admin-summary-row">
      <article v-for="s in statisticsSummary" :key="s.label" class="admin-summary-card" :class="`tone-${s.tone}`">
        <span class="admin-summary-icon" :class="`ic-${s.icon}`" aria-hidden="true" />
        <div>
          <strong>{{ s.value }}</strong>
          <span>{{ s.label }}</span>
        </div>
      </article>
    </section>

    <section class="admin-panel">
      <div class="admin-table-wrap">
        <table class="admin-table admin-table--wide">
          <thead>
            <tr>
              <th>Компания</th>
              <th>Клики</th>
              <th>Уникальные</th>
              <th>CTR</th>
              <th>Период</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in statisticsTable" :key="row.company + row.period">
              <td>{{ row.company }}</td>
              <td>{{ row.clicks }}</td>
              <td>{{ row.unique }}</td>
              <td class="admin-ctr">{{ row.ctr }}</td>
              <td>{{ row.period }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

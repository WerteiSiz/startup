<script setup>
import { managerStatsSummary, managerStatsTable } from '../../data/managerMock'
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head admin-page-head--row">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--green" aria-hidden="true" />
        <div>
          <h1>Статистика</h1>
          <p>Аналитика эффективности ваших предложений</p>
        </div>
      </div>
      <button type="button" class="admin-btn admin-btn--primary">⬇ Скачать отчет</button>
    </header>

    <section class="mgr-stat-summary">
      <article
        v-for="s in managerStatsSummary"
        :key="s.label"
        class="mgr-stat-summary__card"
        :class="`tone-${s.tone}`"
      >
        <span class="mgr-stat-summary__ic" :class="`ic-${s.icon}`" aria-hidden="true" />
        <div>
          <strong>{{ s.value }}</strong>
          <span>{{ s.label }}</span>
        </div>
      </article>
    </section>

    <section class="admin-panel">
      <h2>Статистика по скидкам</h2>
      <div class="admin-table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Предложение</th>
              <th>Просмотры</th>
              <th>Клики</th>
              <th>CTR</th>
              <th>Период</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in managerStatsTable" :key="row.offer">
              <td>{{ row.offer }}</td>
              <td>{{ row.views }}</td>
              <td>{{ row.clicks }}</td>
              <td class="admin-ctr">{{ row.ctr }}</td>
              <td>{{ row.period }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="admin-panel mgr-export">
      <h2>Экспорт отчетов</h2>
      <div class="mgr-export-btns">
        <button type="button" class="mgr-export-btn">📊 Excel отчет</button>
        <button type="button" class="mgr-export-btn">📕 PDF отчет</button>
        <button type="button" class="mgr-export-btn">📄 CSV данные</button>
      </div>
    </section>
  </div>
</template>

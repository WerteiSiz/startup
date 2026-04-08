<script setup>
import { managers, partnerCompaniesTable } from '../../data/adminMock'
import { useAdminPartnerModals } from '../../composables/useAdminPartnerModals'

const { openAddManager, openCreateCompany } = useAdminPartnerModals()
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head admin-page-head--row">
      <div class="admin-page-title">
        <span class="admin-page-icon admin-page-icon--blue" aria-hidden="true" />
        <div>
          <h1>Менеджеры</h1>
          <p>Управление менеджерами и их компаниями</p>
        </div>
      </div>
      <div class="admin-page-actions">
        <button type="button" class="admin-btn admin-btn--outline" @click="openCreateCompany">
          Создать компанию
        </button>
        <button type="button" class="admin-btn admin-btn--primary" @click="openAddManager">
          + Добавить менеджера
        </button>
      </div>
    </header>

    <section class="admin-managers-list">
      <article v-for="m in managers" :key="m.id" class="admin-manager-card">
        <div class="admin-manager-card__top">
          <h2>{{ m.name }}</h2>
          <div class="admin-manager-tools">
            <button type="button" class="admin-icon-btn" aria-label="Редактировать">✎</button>
            <button type="button" class="admin-icon-btn admin-icon-btn--danger" aria-label="Удалить">🗑</button>
          </div>
        </div>
        <p class="admin-manager-meta">{{ m.email }} · {{ m.phone }}</p>
        <p class="admin-manager-meta">Назначен: {{ m.assigned }}</p>
        <h3 class="admin-manager-sub">Закрепленные компании ({{ m.companies.length }}):</h3>
        <div class="admin-mini-cols">
          <div v-for="c in m.companies" :key="c.name" class="admin-mini-card">
            <span class="admin-mini-clicks">{{ c.clicks }}</span>
            <strong>{{ c.name }}</strong>
            <span>Скидок: {{ c.discounts }}</span>
          </div>
        </div>
      </article>
    </section>

    <section class="admin-panel">
      <div class="admin-panel-head">
        <h2>Партнерские компании</h2>
        <button type="button" class="admin-link-all admin-link-all--btn" @click="openCreateCompany">
          + Создать компанию
        </button>
      </div>
      <div class="admin-table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Компания</th>
              <th>Email</th>
              <th>Менеджер</th>
              <th>Скидки</th>
              <th>Клики</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in partnerCompaniesTable" :key="row.company">
              <td>{{ row.company }}</td>
              <td>{{ row.email }}</td>
              <td>{{ row.manager }}</td>
              <td>{{ row.discounts }}</td>
              <td>{{ row.clicks }}</td>
              <td><span class="admin-badge admin-badge--ok">Активна</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

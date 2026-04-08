<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { computed } from 'vue'
import { useSession } from '../composables/useSession'

const router = useRouter()
const { user, logout } = useSession()

const displayRole = computed(() =>
  user.value?.role === 'admin' ? 'Администратор' : user.value?.displayName || 'Пользователь',
)

function handleLogout() {
  logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="admin-layout">
    <header class="admin-top">
      <RouterLink :to="{ name: 'home' }" class="admin-brand">StudentPass</RouterLink>
      <nav class="admin-nav">
        <RouterLink :to="{ name: 'admin-dashboard' }" active-class="is-active">Панель управления</RouterLink>
        <RouterLink :to="{ name: 'admin-applications' }" active-class="is-active">Заявки компаний</RouterLink>
        <RouterLink :to="{ name: 'admin-managers' }" active-class="is-active">Менеджеры</RouterLink>
        <RouterLink :to="{ name: 'admin-statistics' }" active-class="is-active">Статистика</RouterLink>
      </nav>
      <div class="admin-profile">
        <span class="admin-profile-dot" aria-hidden="true" />
        <span class="admin-profile-name">{{ displayRole }}</span>
        <button type="button" class="admin-logout" @click="handleLogout">Выйти</button>
      </div>
    </header>
    <main class="admin-body">
      <RouterView />
    </main>
  </div>
</template>

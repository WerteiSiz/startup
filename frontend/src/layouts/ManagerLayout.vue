<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { computed } from 'vue'
import { useSession } from '../composables/useSession'

const router = useRouter()
const { user, logout } = useSession()

const profileLabel = computed(() => user.value?.displayName || 'Компания')

async function handleLogout() {
  await logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="admin-layout mgr-layout">
    <header class="admin-top">
      <RouterLink :to="{ name: 'home' }" class="admin-brand">StudentPass</RouterLink>
      <nav class="admin-nav mgr-nav">
        <RouterLink :to="{ name: 'manager-discounts' }" active-class="is-active">Мои скидки</RouterLink>
        <RouterLink :to="{ name: 'manager-statistics' }" active-class="is-active">Статистика</RouterLink>
        <RouterLink :to="{ name: 'manager-discount-create' }" active-class="is-active">Создать скидку</RouterLink>
      </nav>
      <div class="admin-profile">
        <span class="admin-profile-dot admin-profile-dot--blue" aria-hidden="true" />
        <span class="admin-profile-name">{{ profileLabel }}</span>
        <button type="button" class="admin-logout" @click="handleLogout">Выйти</button>
      </div>
    </header>
    <main class="admin-body">
      <RouterView />
    </main>
  </div>
</template>

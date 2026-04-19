<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthModal } from '../composables/useAuthModal'
import { useSession } from '../composables/useSession'

const router = useRouter()
const { openRegister, openLogin } = useAuthModal()
const { user, isLoggedIn, isAdmin, isManager, logout } = useSession()

async function handleLogout() {
  const path = router.currentRoute.value.path
  const leaveCabinet = path.startsWith('/admin') || path.startsWith('/manager')
  await logout()
  if (leaveCabinet) router.push({ name: 'home' })
}
</script>

<template>
  <div v-if="!isLoggedIn" class="auth-header-actions">
    <button type="button" class="auth-header-btn auth-header-btn--ghost" @click="openLogin">
      Войти
    </button>
    <button type="button" class="auth-header-btn auth-header-btn--primary" @click="openRegister">
      Регистрация
    </button>
  </div>
  <div v-else class="auth-header-actions auth-header-actions--logged">
    <RouterLink
      v-if="isAdmin"
      class="auth-header-btn auth-header-btn--ghost"
      :to="{ name: 'admin-dashboard' }"
    >
      Админ-панель
    </RouterLink>
    <RouterLink
      v-if="isManager"
      class="auth-header-btn auth-header-btn--ghost"
      :to="{ name: 'manager-discounts' }"
    >
      Кабинет компании
    </RouterLink>
    <span class="auth-header-email" :title="user.email">{{ user.displayName }}</span>
    <button type="button" class="auth-header-btn auth-header-btn--ghost" @click="handleLogout">
      Выйти
    </button>
  </div>
</template>

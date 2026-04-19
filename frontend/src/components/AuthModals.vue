<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthModal } from '../composables/useAuthModal'
import { useSession } from '../composables/useSession'

const router = useRouter()
const { openMode, close, openLogin, openRegister } = useAuthModal()
const { login, register } = useSession()
const authError = ref('')

const regName = ref('')
const regEmail = ref('')
const regUni = ref('')
const regPass = ref('')

const loginEmail = ref('')
const loginPass = ref('')

const onKeydown = (e) => {
  if (e.key === 'Escape') close()
}

watch(openMode, (mode) => {
  document.body.style.overflow = mode ? 'hidden' : ''
})

async function submitRegister() {
  authError.value = ''
  try {
    await register({
      email: regEmail.value,
      name: regName.value,
      password: regPass.value,
    })
    close()
    openLogin()
  } catch (error) {
    authError.value = error instanceof Error ? error.message : 'Не удалось зарегистрироваться'
  }
}

async function submitLogin() {
  authError.value = ''
  try {
    const currentUser = await login({ email: loginEmail.value, password: loginPass.value })
    close()
    const role = currentUser?.role
    if (role === 'admin') router.push({ name: 'admin-dashboard' })
    else if (role === 'partner' || role === 'manager') router.push({ name: 'manager-discounts' })
  } catch (error) {
    authError.value = error instanceof Error ? error.message : 'Не удалось выполнить вход'
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <div
      v-if="openMode"
      class="auth-overlay"
      role="presentation"
      @click.self="close"
    >
      <div
        class="auth-modal"
        :class="{ 'auth-modal--login': openMode === 'login' }"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="openMode === 'login' ? 'auth-login-title' : 'auth-register-title'"
      >
        <button type="button" class="auth-close" aria-label="Закрыть" @click="close">
          ×
        </button>

        <template v-if="openMode === 'register'">
          <h2 id="auth-register-title" class="auth-title">Регистрация</h2>

          <form class="auth-form" @submit.prevent="submitRegister">
            <div class="auth-field">
              <label class="auth-label" for="reg-name">Имя</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M12 12a4 4 0 100-8 4 4 0 000 8zM4 20a8 8 0 1116 0H4z" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="reg-name" v-model="regName" type="text" class="auth-input" placeholder="Иван Иванов" autocomplete="name" />
              </div>
            </div>

            <div class="auth-field">
              <label class="auth-label" for="reg-email">Студенческая почта <span class="auth-label-hint">(.edu, @student, @ac)</span></label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M4 6h16v12H4V6zm0 0l8 6 8-6" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="reg-email" v-model="regEmail" type="email" class="auth-input" placeholder="student@university.edu" autocomplete="email" />
              </div>
              <p class="auth-hint">Используйте почту, выданную вашим учебным заведением</p>
            </div>

            <div class="auth-field">
              <label class="auth-label" for="reg-uni">Университет</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M12 3L3 8v2h18V8L12 3zm-7 6l7 4 7-4" stroke="currentColor" stroke-width="2"/><path d="M5 14v6M19 14v6" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="reg-uni" v-model="regUni" type="text" class="auth-input" placeholder="МИРЭА, МГУ, СПбГУ, НИУ ВШЭ..." autocomplete="organization" />
              </div>
            </div>

            <div class="auth-field">
              <label class="auth-label" for="reg-pass">Пароль</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 11V7a4 4 0 018 0v4" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="reg-pass" v-model="regPass" type="password" class="auth-input" placeholder="••••••••" autocomplete="new-password" />
              </div>
            </div>

            <button type="submit" class="auth-submit">Продолжить</button>
            <p v-if="authError" class="auth-hint">{{ authError }}</p>
          </form>

          <p class="auth-switch">
            Уже есть аккаунт?
            <button type="button" class="auth-link" @click="openLogin">Войти</button>
          </p>
        </template>

        <template v-else>
          <h2 id="auth-login-title" class="auth-title">Вход в StudentPass</h2>

          <form class="auth-form" @submit.prevent="submitLogin">
            <div class="auth-field">
              <label class="auth-label" for="login-email">Логин или почта</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M4 6h16v12H4V6zm0 0l8 6 8-6" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="login-email" v-model="loginEmail" type="text" class="auth-input" placeholder="admin, manager или email" autocomplete="username" />
              </div>
              <p class="auth-hint">
                Демо-вход: <strong>admin / admin</strong> — админ-панель, <strong>manager / manager</strong> — кабинет компании.
              </p>
            </div>

            <div class="auth-field">
              <label class="auth-label" for="login-pass">Пароль</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 11V7a4 4 0 018 0v4" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input id="login-pass" v-model="loginPass" type="password" class="auth-input" placeholder="••••••••" autocomplete="current-password" />
              </div>
            </div>

            <button type="submit" class="auth-submit">Войти</button>
            <p v-if="authError" class="auth-hint">{{ authError }}</p>
          </form>

          <p class="auth-switch">
            Нет аккаунта?
            <button type="button" class="auth-link" @click="openRegister">Зарегистрироваться</button>
          </p>
        </template>
      </div>
    </div>
  </Teleport>
</template>

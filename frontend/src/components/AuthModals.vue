<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthModal } from '../composables/useAuthModal'
import { useSession } from '../composables/useSession'

const router = useRouter()
const { openMode, close, openLogin, openRegister } = useAuthModal()
const { login, register, requestRegistrationCode } = useSession()
const authError = ref('')

const regName = ref('')
const regEmail = ref('')
const regUni = ref('')
const regPass = ref('')
const regCode = ref('')
const codeSent = ref(false)
const sendingCode = ref(false)

const loginEmail = ref('')
const loginPass = ref('')

const onKeydown = (e) => {
  if (e.key === 'Escape') close()
}

watch(openMode, (mode) => {
  document.body.style.overflow = mode ? 'hidden' : ''
  if (mode === 'register') {
    regCode.value = ''
    codeSent.value = false
    authError.value = ''
  }
})

async function onSendCode() {
  authError.value = ''
  if (!String(regEmail.value || '').trim()) {
    authError.value = 'Укажите email, на который отправить код'
    return
  }
  sendingCode.value = true
  try {
    await requestRegistrationCode({ email: regEmail.value })
    codeSent.value = true
  } catch (error) {
    authError.value = error instanceof Error ? error.message : 'Не удалось отправить код'
  } finally {
    sendingCode.value = false
  }
}

async function submitRegister() {
  authError.value = ''
  try {
    await register({
      email: regEmail.value,
      name: regName.value,
      password: regPass.value,
      code: regCode.value,
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
              <button
                type="button"
                class="auth-submit auth-submit--secondary"
                :disabled="sendingCode"
                @click="onSendCode"
              >
                {{ sendingCode ? 'Отправка…' : 'Получить код на почту' }}
              </button>
              <p v-if="codeSent" class="auth-hint auth-hint--ok">Код отправлен. Проверьте почту и введите его ниже.</p>
            </div>

            <div class="auth-field">
              <label class="auth-label" for="reg-code">Код из письма</label>
              <div class="auth-input-row">
                <span class="auth-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M12 15a3 3 0 100-6 3 3 0 000 6z" stroke="currentColor" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" stroke="currentColor" stroke-width="2"/></svg>
                </span>
                <input
                  id="reg-code"
                  v-model="regCode"
                  type="text"
                  inputmode="numeric"
                  maxlength="6"
                  autocomplete="one-time-code"
                  class="auth-input"
                  placeholder="000000"
                />
              </div>
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

            <button type="submit" class="auth-submit">Зарегистрироваться</button>
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

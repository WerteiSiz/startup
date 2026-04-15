<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { managers } from '../data/adminMock'
import { useAdminPartnerModals } from '../composables/useAdminPartnerModals'

const { openMode, close } = useAdminPartnerModals()

const managerName = ref('')
const managerEmail = ref('')
const managerPhone = ref('')

const companyName = ref('')
const companyEmail = ref('')
const companyPassword = ref('')
const companyManagerId = ref('')

const onKeydown = (e) => {
  if (e.key === 'Escape') close()
}

watch(openMode, (mode) => {
  document.body.style.overflow = mode ? 'hidden' : ''
  if (!mode) return
  if (mode === 'manager') {
    managerName.value = ''
    managerEmail.value = ''
    managerPhone.value = ''
  } else {
    companyName.value = ''
    companyEmail.value = ''
    companyPassword.value = ''
    companyManagerId.value = ''
  }
})

function submitManager() {
  close()
}

function submitCompany() {
  close()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <div v-if="openMode" class="auth-overlay" role="presentation" @click.self="close">
      <!-- Добавить менеджера -->
      <div
        v-if="openMode === 'manager'"
        class="auth-modal admin-partner-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="admin-add-manager-title"
      >
        <button type="button" class="auth-close" aria-label="Закрыть" @click="close">×</button>
        <h2 id="admin-add-manager-title" class="auth-title">Добавить менеджера</h2>

        <form class="auth-form" @submit.prevent="submitManager">
          <div class="auth-field">
            <label class="auth-label" for="adm-mgr-name">ФИО</label>
            <input
              id="adm-mgr-name"
              v-model="managerName"
              type="text"
              class="admin-modal-input"
              placeholder="Иванов Иван Иванович"
              autocomplete="name"
            />
          </div>
          <div class="auth-field">
            <label class="auth-label" for="adm-mgr-email">Email</label>
            <input
              id="adm-mgr-email"
              v-model="managerEmail"
              type="email"
              class="admin-modal-input"
              placeholder="manager@studentpass.ru"
              autocomplete="email"
            />
          </div>
          <div class="auth-field">
            <label class="auth-label" for="adm-mgr-phone">Телефон</label>
            <input
              id="adm-mgr-phone"
              v-model="managerPhone"
              type="tel"
              class="admin-modal-input"
              placeholder="+7 (495) 123-45-67"
              autocomplete="tel"
            />
          </div>
          <button type="submit" class="auth-submit">Добавить</button>
        </form>
      </div>

      <!-- Создать компанию-партнера -->
      <div
        v-else
        class="auth-modal admin-partner-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="admin-create-company-title"
      >
        <button type="button" class="auth-close" aria-label="Закрыть" @click="close">×</button>
        <h2 id="admin-create-company-title" class="auth-title">Создать компанию-партнера</h2>

        <form class="auth-form" @submit.prevent="submitCompany">
          <div class="auth-field">
            <label class="auth-label" for="adm-co-name">Название компании</label>
            <input
              id="adm-co-name"
              v-model="companyName"
              type="text"
              class="admin-modal-input admin-modal-input--focus-ring"
              placeholder="Burger King"
              autocomplete="organization"
            />
          </div>
          <div class="auth-field">
            <label class="auth-label" for="adm-co-email">Email компании</label>
            <input
              id="adm-co-email"
              v-model="companyEmail"
              type="email"
              class="admin-modal-input admin-modal-input--light"
              placeholder="manager@gmail.com"
              autocomplete="email"
            />
          </div>
          <div class="auth-field">
            <label class="auth-label" for="adm-co-pass">Пароль</label>
            <input
              id="adm-co-pass"
              v-model="companyPassword"
              type="password"
              class="admin-modal-input admin-modal-input--light"
              placeholder="••••••••"
              autocomplete="new-password"
            />
          </div>
          <div class="auth-field">
            <label class="auth-label" for="adm-co-mgr">Назначить менеджера</label>
            <div class="admin-modal-select-wrap">
              <select id="adm-co-mgr" v-model="companyManagerId" class="admin-modal-select" required>
                <option disabled value="">Выберите менеджера</option>
                <option v-for="m in managers" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
            </div>
          </div>
          <button type="submit" class="auth-submit">Создать компанию</button>
        </form>
      </div>
    </div>
  </Teleport>
</template>

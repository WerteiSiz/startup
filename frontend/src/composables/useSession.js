import { computed, ref } from 'vue'
import { applyDevAuthSession } from '../config/devAuth'
import {
  getCurrentUser,
  loginUser,
  logoutUser,
  registerPartner,
  registerUser,
  sendRegistrationCode,
} from '../services/authService'

const user = ref(null)
let storageLoaded = false

function toUiUser(apiUser) {
  return {
    id: apiUser.id,
    email: apiUser.email,
    displayName: apiUser.full_name || apiUser.email,
    role: apiUser.role,
    isActive: apiUser.is_active,
  }
}

async function readStorage() {
  if (storageLoaded) return
  storageLoaded = true

  applyDevAuthSession(user)
  if (user.value) return

  try {
    const apiUser = await getCurrentUser()
    user.value = toUiUser(apiUser)
  } catch {
    user.value = null
  }
}

function mapLoginValue(value) {
  const v = String(value || '').trim().toLowerCase()
  if (v === 'admin') return 'admin@studentpass.local'
  if (v === 'manager' || v === 'partner') return 'partner@studentpass.local'
  return String(value || '').trim()
}

function isPartnerRole(role) {
  return role === 'partner' || role === 'manager'
}

export function useSession() {
  void readStorage()

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => isPartnerRole(user.value?.role))

  async function login({ email, password = '' }) {
    await loginUser({ email: mapLoginValue(email), password })
    const apiUser = await getCurrentUser()
    user.value = toUiUser(apiUser)
    return user.value
  }

  async function requestRegistrationCode({ email }) {
    await sendRegistrationCode({ email: String(email || '').trim() })
  }

  async function register({
    email,
    name,
    password = 'studentpass',
    code,
    companyName = '',
    phone = '',
    partner = false,
  }) {
    if (partner) {
      await registerPartner({
        email: String(email || '').trim(),
        password,
        full_name: String(name || '').trim(),
        company_name: String(companyName || '').trim() || 'Компания',
        phone: String(phone || '').trim() || '+7 (000) 000-00-00',
      })
      return
    }
    const raw = String(code ?? '').replace(/\D/g, '')
    const codeNum = Number.parseInt(raw, 10)
    if (!Number.isFinite(codeNum) || raw.length !== 6) {
      throw new Error('Введите 6-значный код из письма')
    }
    await registerUser({
      email: String(email || '').trim(),
      password,
      full_name: String(name || '').trim(),
      code: codeNum,
    })
  }

  async function logout() {
    try {
      await logoutUser()
    } catch {
      /* noop */
    }
    user.value = null
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    isManager,
    login,
    register,
    requestRegistrationCode,
    logout,
    readStorage,
  }
}

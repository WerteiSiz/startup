import { computed, ref } from 'vue'
import { applyDevAuthSession } from '../config/devAuth'

const STORAGE_KEY = 'studentpass_session'

const user = ref(null)
let storageLoaded = false

function readStorage() {
  if (storageLoaded || typeof localStorage === 'undefined') return
  storageLoaded = true
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) user.value = JSON.parse(raw)
  } catch {
    /* ignore */
  }
  applyDevAuthSession(user)
}

function writeStorage() {
  if (typeof localStorage === 'undefined') return
  if (user.value) localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value))
  else localStorage.removeItem(STORAGE_KEY)
}

export function roleFromEmail(email) {
  const e = String(email).trim().toLowerCase()
  if (e.startsWith('admin@')) return 'admin'
  if (e.startsWith('manager@')) return 'manager'
  return 'user'
}

function roleFromCredentials(login, password) {
  const l = String(login).trim().toLowerCase()
  const p = String(password).trim().toLowerCase()
  if (l === 'admin' && p === 'admin') return 'admin'
  if (l === 'manager' && p === 'manager') return 'manager'
  return null
}

export function useSession() {
  readStorage()

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => user.value?.role === 'manager')

  function login({ email, password = '', displayName }) {
    const loginValue = String(email).trim()
    const roleByCredentials = roleFromCredentials(loginValue, password)
    const role = roleByCredentials || roleFromEmail(loginValue)
    const profileNameByRole = role === 'admin' ? 'Администратор' : role === 'manager' ? 'Компания Manager' : null
    const fallbackDisplayName = loginValue.includes('@') ? loginValue.split('@')[0] : loginValue

    user.value = {
      email: loginValue.includes('@') ? loginValue : `${loginValue || role}@studentpass.local`,
      displayName: displayName?.trim() || profileNameByRole || fallbackDisplayName || 'Пользователь',
      role,
    }
    writeStorage()
    return user.value
  }

  function register({ email, name }) {
    const e = email.trim()
    user.value = {
      email: e,
      displayName: name?.trim() || e.split('@')[0],
      role: roleFromEmail(e),
    }
    writeStorage()
  }

  function logout() {
    user.value = null
    writeStorage()
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    isManager,
    login,
    register,
    logout,
    readStorage,
  }
}

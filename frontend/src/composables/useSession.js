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

/**
 * Демо-роли по почте:
 * admin@* — администратор
 * manager@* — менеджер компании
 */
export function roleFromEmail(email) {
  const e = String(email).trim().toLowerCase()
  if (e.startsWith('admin@')) return 'admin'
  if (e.startsWith('manager@')) return 'manager'
  return 'user'
}

export function useSession() {
  readStorage()

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => user.value?.role === 'manager')

  function login({ email, displayName }) {
    const e = email.trim()
    user.value = {
      email: e,
      displayName: displayName?.trim() || e.split('@')[0],
      role: roleFromEmail(e),
    }
    writeStorage()
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

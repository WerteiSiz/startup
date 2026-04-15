/**
 * Тестовая авторизация (только import.meta.env.DEV === true).
 *
 * 1) Задайте роль здесь — перекрывает .env, если не пусто.
 * 2) Или в `.env.development`: VITE_DEV_AUTH_ROLE=admin|manager|user|off
 *
 * Значение '' или 'off' — обычное поведение (только localStorage / вход в модалке).
 */
export const HARDCODE_DEV_AUTH_ROLE = ''

const PROFILES = {
  admin: { email: 'admin@test.dev', displayName: 'Администратор', role: 'admin' },
  manager: { email: 'manager@test.dev', displayName: 'Компания Manager', role: 'manager' },
  user: { email: 'student@test.dev', displayName: 'Студент', role: 'user' },
}

export function getDevAuthRole() {
  const hard = String(HARDCODE_DEV_AUTH_ROLE || '').trim().toLowerCase()
  const env = String(import.meta.env.VITE_DEV_AUTH_ROLE || '').trim().toLowerCase()
  const role = hard || env
  if (!role || role === 'off' || role === 'none') return null
  return role in PROFILES ? role : null
}

/**
 * @param {import('vue').Ref<{ email: string, displayName: string, role: string } | null>} userRef
 */
export function applyDevAuthSession(userRef) {
  if (!import.meta.env.DEV) return
  const key = getDevAuthRole()
  if (!key) return
  userRef.value = { ...PROFILES[key] }
}

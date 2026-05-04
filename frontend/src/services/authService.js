import { apiRequest } from './apiClient'

export async function loginUser(payload) {
  return apiRequest('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

/** Запрос кода подтверждения на email перед регистрацией (обычный пользователь). */
export async function sendRegistrationCode({ email }) {
  return apiRequest('/api/v1/auth/send_code', {
    method: 'POST',
    body: JSON.stringify({ email }),
  })
}

export async function registerUser(payload) {
  const { email, password, full_name, code } = payload
  const codeNum = typeof code === 'number' ? code : Number.parseInt(String(code).replace(/\D/g, ''), 10)
  const data = await apiRequest('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
      full_name,
      code: codeNum,
    }),
  })
  // API может вернуть 200 с текстом об ошибке кода
  if (data?.message && /код не подходит/i.test(data.message)) {
    throw new Error(data.message)
  }
  return data
}

export async function registerPartner(payload) {
  return apiRequest('/api/v1/auth/register-partner', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getCurrentUser() {
  return apiRequest('/api/v1/auth/me')
}

export async function logoutUser() {
  return apiRequest('/api/v1/auth/logout', { method: 'POST' })
}

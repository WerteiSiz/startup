import { apiRequest } from './apiClient'

export async function loginUser(payload) {
  return apiRequest('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function registerUser(payload) {
  return apiRequest('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function registerPartner(payload) {
  return apiRequest('/api/v1/auth/register-partner', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function verifyEmailCode(payload) {
  return apiRequest('/api/v1/auth/verify-email', {
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

import { apiRequest } from './apiClient'

export function getPartnerRequests(params = {}) {
  return apiRequest('/api/v1/admin/partner-requests', { query: params })
}

export function updatePartnerRequest(requestId, payload) {
  return apiRequest(`/api/v1/admin/partner-requests/${requestId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function getAdminUsers(params = {}) {
  return apiRequest('/api/v1/admin/users', { query: params })
}

export function updateUserRole(userId, payload) {
  return apiRequest(`/api/v1/admin/users/${userId}/role`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

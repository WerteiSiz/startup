import { apiRequest } from './apiClient'

export function getPartnerRequests(params = {}) {
  return apiRequest('/api/v1/admin/partner-requests', { query: params })
}

export function approvePartnerRequest(userEmail) {
  return apiRequest(`/api/v1/admin/partner-requests/${encodeURIComponent(userEmail)}`, {
    method: 'POST',
  })
}

export function getAdminUsers(params = {}) {
  return apiRequest('/api/v1/admin/users', { query: params })
}

export function deleteAdminUser(userId) {
  return apiRequest(`/api/v1/admin/users/${userId}`, { method: 'DELETE' })
}

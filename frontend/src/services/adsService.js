import { apiRequest } from './apiClient'

export function getAds(params = {}) {
  return apiRequest('/api/v1/ads', { query: params })
}

export function getAdById(adId) {
  return apiRequest(`/api/v1/ads/${adId}`)
}

export function getAdCategories() {
  return apiRequest('/api/v1/ads/categories')
}

export function clickAd(adId) {
  return apiRequest(`/api/v1/ads/${adId}/click`, { method: 'POST' })
}

export function getPartnerAds(params = {}) {
  return apiRequest('/api/v1/partner/ads', { query: params })
}

export function createPartnerAd(payload) {
  return apiRequest('/api/v1/partner/ads', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updatePartnerAd(adId, payload) {
  return apiRequest(`/api/v1/partner/ads/${adId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deletePartnerAd(adId) {
  return apiRequest(`/api/v1/partner/ads/${adId}`, { method: 'DELETE' })
}

import { computed, ref } from 'vue'
import {
  createPartnerAd,
  deletePartnerAd,
  getAdCategories,
  getPartnerAds,
  updatePartnerAd,
} from '../services/adsService'

const discounts = ref([])
const categories = ref([])
const stateLoaded = ref(false)

function normalizeDiscount(payload) {
  const percentNumber = Number(payload.discount_percent ?? payload.percentNumber ?? payload.percent ?? 0)
  const safePercent = Number.isFinite(percentNumber) ? Math.max(0, Math.min(100, percentNumber)) : 0
  const cat = payload.categories?.[0] || payload.category || 'Прочее'

  return {
    id: String(payload.id),
    emoji: '🏷',
    title: String(payload.title || '').trim(),
    description: String(payload.description || '').trim(),
    percent: `-${safePercent}%`,
    percentNumber: safePercent,
    category: String(cat).trim() || 'Прочее',
    categoryIds: payload.category_ids || [],
    linkUrl: String(payload.url || payload.linkUrl || '').trim(),
    views: Number(payload.views ?? 0) || 0,
    clicks: Number(payload.clicks_count ?? payload.clicks ?? 0) || 0,
    address: String(payload.address || '').trim(),
    endDate: payload.end_date,
    raw: payload,
  }
}

function mapPayloadToApi(payload, categoryRef) {
  const categoryIdByName =
    categories.value.find((item) => item.name === String(categoryRef || payload.category || '').trim())?.id || null
  return {
    title: String(payload.title || '').trim(),
    description: String(payload.description || '').trim(),
    discount_percent: Number(payload.percentNumber ?? 0),
    url: String(payload.linkUrl || '').trim(),
    address: String(payload.address || 'Онлайн').trim(),
    end_date: payload.endDate || new Date(Date.now() + 1000 * 60 * 60 * 24 * 30).toISOString(),
    category_ids: Array.isArray(payload.categoryIds) && payload.categoryIds.length
      ? payload.categoryIds
      : [categoryIdByName || 1],
    emodzi_id: null,
    prioritet: 0,
  }
}

export function useManagerDiscounts() {
  async function load() {
    if (stateLoaded.value) return
    stateLoaded.value = true
    const [adsResponse, categoriesResponse] = await Promise.all([getPartnerAds(), getAdCategories()])
    const items = Array.isArray(adsResponse?.items) ? adsResponse.items : []
    discounts.value = items.map(normalizeDiscount)
    categories.value = Array.isArray(categoriesResponse) ? categoriesResponse : []
  }

  const items = computed(() => discounts.value)
  const categoryNames = computed(() => categories.value.map((item) => item.name))

  function getById(id) {
    return discounts.value.find((item) => item.id === String(id)) || null
  }

  async function createDiscount(payload) {
    await createPartnerAd(mapPayloadToApi(payload, payload.category))
    const adsResponse = await getPartnerAds()
    discounts.value = (adsResponse?.items || []).map(normalizeDiscount)
    const item = discounts.value[0] || null
    return item
  }

  async function updateDiscount(id, payload) {
    const idx = discounts.value.findIndex((item) => item.id === String(id))
    if (idx < 0) return null
    const base = discounts.value[idx]
    await updatePartnerAd(String(id), mapPayloadToApi({ ...base, ...payload }, payload.category))
    const adsResponse = await getPartnerAds()
    discounts.value = (adsResponse?.items || []).map(normalizeDiscount)
    const next = discounts.value.find((item) => item.id === String(id)) || null
    return next
  }

  async function deleteDiscount(id) {
    await deletePartnerAd(String(id))
    discounts.value = discounts.value.filter((item) => item.id !== String(id))
  }

  return {
    items,
    categoryNames,
    load,
    getById,
    createDiscount,
    updateDiscount,
    deleteDiscount,
  }
}

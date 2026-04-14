import { computed, ref } from 'vue'
import { managerDiscounts as seedDiscounts } from '../data/managerMock'

const STORAGE_KEY = 'studentpass_manager_discounts'
const discounts = ref([])
let loaded = false

function normalizeDiscount(payload) {
  const percentNumber = Number(payload.percentNumber ?? payload.percent ?? 0)
  const safePercent = Number.isFinite(percentNumber) ? Math.max(0, Math.min(100, percentNumber)) : 0

  return {
    id: String(payload.id),
    emoji: String(payload.emoji || '🏷').trim() || '🏷',
    title: String(payload.title || '').trim(),
    description: String(payload.description || '').trim(),
    percent: `-${safePercent}%`,
    percentNumber: safePercent,
    category: String(payload.category || 'Прочее').trim() || 'Прочее',
    linkUrl: String(payload.linkUrl || '').trim(),
    views: Number(payload.views ?? 0) || 0,
    clicks: Number(payload.clicks ?? 0) || 0,
  }
}

function save() {
  if (typeof localStorage === 'undefined') return
  localStorage.setItem(STORAGE_KEY, JSON.stringify(discounts.value))
}

function hydrate() {
  if (loaded) return
  loaded = true

  if (typeof localStorage === 'undefined') {
    discounts.value = seedDiscounts.map(normalizeDiscount)
    return
  }

  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed)) {
        discounts.value = parsed.map(normalizeDiscount)
        return
      }
    }
  } catch {
    /* ignore broken storage */
  }

  discounts.value = seedDiscounts.map(normalizeDiscount)
  save()
}

function makeId() {
  return `mg_${Date.now()}_${Math.floor(Math.random() * 10000)}`
}

export function useManagerDiscounts() {
  hydrate()

  const items = computed(() => discounts.value)

  function getById(id) {
    return discounts.value.find((item) => item.id === String(id)) || null
  }

  function createDiscount(payload) {
    const item = normalizeDiscount({ ...payload, id: makeId() })
    discounts.value = [item, ...discounts.value]
    save()
    return item
  }

  function updateDiscount(id, payload) {
    const idx = discounts.value.findIndex((item) => item.id === String(id))
    if (idx < 0) return null
    const next = normalizeDiscount({ ...discounts.value[idx], ...payload, id: String(id) })
    discounts.value.splice(idx, 1, next)
    save()
    return next
  }

  function deleteDiscount(id) {
    const before = discounts.value.length
    discounts.value = discounts.value.filter((item) => item.id !== String(id))
    if (discounts.value.length !== before) save()
  }

  return {
    items,
    getById,
    createDiscount,
    updateDiscount,
    deleteDiscount,
  }
}

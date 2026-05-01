import { getAds, getAdCategories } from './adsService'

const ACCENTS = ['orange', 'magenta', 'blue', 'violet', 'teal', 'slate', 'purple', 'azure']

function mapAdToCatalogItem(item, idx) {
  const discount = Number(item.discount_percent) || 0
  const isFree = discount >= 100

  return {
    id: String(item.id),
    title: item.title || 'Скидка',
    category: item.categories?.[0] || 'Прочее',
    description: item.description || 'Предложение от партнера StudentPass.',
    badges: item.categories?.length ? item.categories : ['Партнер'],
    tag: isFree ? 'Бесплатно' : 'Скидка',
    oldPrice: 'По прайсу партнера',
    price: isFree ? 'Бесплатно' : 'Скидка у партнера',
    discount: `-${discount}%`,
    isFree,
    accent: ACCENTS[idx % ACCENTS.length],
    partnerName: item.partner_name,
    clicksCount: item.clicks_count,
    raw: item,
  }
}

export async function getCatalogItems(params = {}) {
  const response = await getAds(params)
  const items = Array.isArray(response?.items) ? response.items : []
  return items.map(mapAdToCatalogItem)
}

export async function getCatalogCategories() {
  const categories = await getAdCategories()
  if (!Array.isArray(categories)) return []
  return categories.map((item) => item.name).filter(Boolean)
}

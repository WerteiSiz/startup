<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import SitePublicHeader from '../components/SitePublicHeader.vue'
import { getCatalogCategories, getCatalogItems } from '../services/catalogService'

const categories = ref(['Все'])

const search = ref('')
const sortBy = ref('По умолчанию')
const onlyFree = ref(false)
const activeCategory = ref('Все')
const items = ref([])

const visibleItems = computed(() => {
  const q = search.value.trim().toLowerCase()

  let data = items.value.filter((item) => {
    const byCategory = activeCategory.value === 'Все' || item.category === activeCategory.value
    const byFree = !onlyFree.value || item.isFree
    const bySearch =
      q.length === 0 ||
      item.title.toLowerCase().includes(q) ||
      item.category.toLowerCase().includes(q) ||
      item.badges.some((tag) => tag.toLowerCase().includes(q))

    return byCategory && byFree && bySearch
  })

  if (sortBy.value === 'Сначала бесплатные') {
    data = [...data].sort((a, b) => Number(b.isFree) - Number(a.isFree))
  }

  if (sortBy.value === 'По алфавиту') {
    data = [...data].sort((a, b) => a.title.localeCompare(b.title, 'ru'))
  }

  return data
})

const freeCount = computed(() => items.value.filter((item) => item.isFree).length)

onMounted(async () => {
  const [catalogItems, apiCategories] = await Promise.all([getCatalogItems(), getCatalogCategories()])
  items.value = catalogItems
  categories.value = ['Все', ...apiCategories]
})
</script>

<template>
  <div class="cat-page">
    <SitePublicHeader />

    <main class="cat-container cat-main">
      <span class="cat-counter">{{ items.length }} скидок в каталоге</span>
      <h1>Каталог скидок</h1>
      <p class="cat-subtitle">Легальные студенческие скидки на профессиональный софт и AI-сервисы</p>

      <section class="cat-filters">
        <input
          v-model="search"
          class="cat-input"
          type="text"
          placeholder="Поиск по названию, категории..."
        />

        <select v-model="sortBy" class="cat-select">
          <option>По умолчанию</option>
          <option>Сначала бесплатные</option>
          <option>По алфавиту</option>
        </select>

        <button class="cat-toggle" :class="{ 'is-active': onlyFree }" @click="onlyFree = !onlyFree">
          Только бесплатные
        </button>
      </section>

      <div class="cat-chip-row">
        <button
          v-for="category in categories"
          :key="category"
          class="cat-chip"
          :class="{ 'is-active': activeCategory === category }"
          @click="activeCategory = category"
        >
          {{ category }}
        </button>
      </div>

      <p class="cat-found">Найдено: {{ visibleItems.length }} скидок · <span>{{ freeCount }} бесплатных</span></p>

      <section class="cat-grid">
        <article
          v-for="item in visibleItems"
          :key="item.id"
          class="cat-card"
          :class="`cat-card--${item.accent}`"
        >
          <div class="cat-card-top">
            <div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.category }}</p>
            </div>
            <span>{{ item.tag }}</span>
          </div>

          <p class="cat-card-desc">{{ item.description }}</p>

          <div class="cat-tags">
            <span v-for="tag in item.badges" :key="tag">{{ tag }}</span>
          </div>

          <div class="cat-price-row">
            <div>
              <small>{{ item.oldPrice }}</small>
              <strong>{{ item.price }}</strong>
            </div>
            <div class="cat-actions">
              <em v-if="item.discount">{{ item.discount }}</em>
              <RouterLink :to="`/product/${item.id}`">Получить</RouterLink>
            </div>
          </div>
        </article>
      </section>
    </main>

  </div>
</template>

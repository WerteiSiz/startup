<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getAdById } from '../services/adsService'

const route = useRoute()
const productId = computed(() => route.params.id)
const item = ref(null)
const loadError = ref('')

onMounted(async () => {
  loadError.value = ''
  try {
    item.value = await getAdById(productId.value)
  } catch (error) {
    loadError.value = error instanceof Error ? error.message : 'Не удалось загрузить продукт'
  }
})
</script>

<template>
  <section class="page">
    <p class="eyebrow">Product</p>
    <h1>{{ item?.title || 'Карточка скидки' }}</h1>
    <p class="muted" v-if="item">{{ item.description }}</p>
    <p class="muted" v-else-if="loadError">{{ loadError }}</p>
    <p class="muted" v-else>Загрузка...</p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const productId = computed(() => route.params.id)
</script>

<template>
  <section class="page">
    <p class="eyebrow">Product</p>
    <h1>Product page</h1>
    <p class="muted">Dynamic route param: {{ productId }}</p>
  </section>
</template>

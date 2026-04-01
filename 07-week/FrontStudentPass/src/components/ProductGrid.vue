<script setup>
import ProductCard from "./ProductCard.vue";

defineProps({
  products: {
    type: Array,
    required: true,
  },
});
</script>

<template>
  <section class="space-y-6">
    <div class="flex items-end justify-between gap-3">
      <div>
        <p class="text-sm font-semibold uppercase tracking-[0.2em] text-violet-300">Каталог</p>
        <h2 class="mt-2 text-3xl font-bold text-white md:text-4xl">Популярные скидки</h2>
      </div>
      <RouterLink
        to="/catalog"
        class="text-sm font-semibold text-violet-300 transition hover:text-cyan-300"
      >
        Смотреть все
      </RouterLink>
    </div>

    <div class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
  </section>
</template>

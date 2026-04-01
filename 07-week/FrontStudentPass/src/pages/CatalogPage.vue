<script setup>
import ProductGrid from "../components/ProductGrid.vue";
import { products } from "../data/products";
</script>

<template>
  <main class="mx-auto flex w-full max-w-7xl flex-col gap-10 px-4 py-10 md:px-8 md:py-14">
    <section class="rounded-2xl border border-white/10 bg-[#0a0e1b]/70 p-6 shadow-xl md:p-8">
      <p class="inline-flex rounded-full border border-violet-400/20 bg-violet-500/10 px-4 py-1 text-sm text-violet-200">
        {{ products.length }} скидок в каталоге
      </p>
      <h1 class="mt-4 text-4xl font-extrabold text-white md:text-6xl">Каталог скидок</h1>
      <p class="mt-4 max-w-3xl text-lg text-slate-300">
        Легальные студенческие скидки на профессиональный софт и AI-сервисы.
      </p>
    </section>

    <ProductGrid :products="products" />
  </main>
</template>

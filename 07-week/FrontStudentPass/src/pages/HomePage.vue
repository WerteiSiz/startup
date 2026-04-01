<script setup>
import HeroSection from "../components/HeroSection.vue";
import ProblemSection from "../components/ProblemSection.vue";
import ProductGrid from "../components/ProductGrid.vue";
import WhySection from "../components/WhySection.vue";
import CtaSection from "../components/CtaSection.vue";
import { products } from "../data/products";
</script>

<template>
  <main class="mx-auto flex w-full max-w-7xl flex-col gap-20 px-4 py-10 md:px-8 md:py-14">
    <HeroSection />
    <ProblemSection />
    <ProductGrid :products="products" />
    <WhySection id="how-it-works" />
    <CtaSection />
  </main>
</template>

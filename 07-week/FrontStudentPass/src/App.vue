<script setup>
import SiteHeader from "./components/SiteHeader.vue";
import SiteFooter from "./components/SiteFooter.vue";
</script>

<template>
  <div
    class="min-h-screen bg-gradient-to-b from-[#0b0f1a] to-[#0a0d18] font-sans text-slate-100"
    style="font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
  >
    <SiteHeader />
    <RouterView />
    <main class="mx-auto w-full max-w-7xl px-4 pb-10 md:px-8 md:pb-14">
      <SiteFooter />
    </main>
  </div>
</template>

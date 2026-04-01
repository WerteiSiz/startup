<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <article
    class="group rounded-2xl border border-white/10 bg-[#0f1424]/90 p-5 shadow-lg transition duration-300 hover:scale-[1.03] hover:border-violet-400/50 hover:shadow-xl hover:shadow-violet-500/25"
  >
    <div class="mb-4 flex items-start justify-between gap-3">
      <div>
        <h3 class="text-xl font-semibold text-white">{{ props.product.title }}</h3>
        <p class="mt-1 text-sm text-slate-400">{{ props.product.category }}</p>
      </div>
      <span
        :class="
          props.product.badge === 'Хит'
            ? 'bg-gradient-to-r from-orange-500/90 to-rose-500/90'
            : 'bg-gradient-to-r from-fuchsia-500/90 to-cyan-500/90'
        "
        class="rounded-full px-3 py-1 text-xs font-semibold text-white"
      >
        {{ props.product.badge }}
      </span>
    </div>

    <p class="mb-4 min-h-[72px] text-slate-300">{{ props.product.description }}</p>

    <div class="mb-5 flex flex-wrap gap-2">
      <span
        v-for="tag in props.product.tags"
        :key="tag"
        class="rounded-full border border-white/15 bg-white/5 px-3 py-1 text-xs text-slate-200"
      >
        {{ tag }}
      </span>
    </div>

    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-sm text-slate-500 line-through">{{ props.product.oldPrice }}</p>
        <p class="text-3xl font-bold text-emerald-400">{{ props.product.price }}</p>
      </div>
      <button
        class="rounded-2xl border border-white/20 bg-white/5 px-5 py-2 font-semibold text-white transition duration-300 hover:border-cyan-400 hover:bg-cyan-500/10 hover:shadow-lg hover:shadow-cyan-500/20"
      >
        Получить
      </button>
    </div>
  </article>
</template>

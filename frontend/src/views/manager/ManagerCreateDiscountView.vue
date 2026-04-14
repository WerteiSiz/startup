<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { managerCategories } from '../../data/managerMock'
import { useManagerDiscounts } from '../../composables/useManagerDiscounts'

const route = useRoute()
const router = useRouter()
const { getById, createDiscount, updateDiscount } = useManagerDiscounts()

const discountId = computed(() => String(route.params.id || ''))
const editingDiscount = computed(() => (discountId.value ? getById(discountId.value) : null))
const isEditMode = computed(() => !!editingDiscount.value)

const title = ref(editingDiscount.value?.title || '15% скидка на все меню')
const description = ref(
  editingDiscount.value?.description || 'Подробное описание скидки и условий получения...',
)
const percent = ref(editingDiscount.value?.percentNumber ?? 15)
const category = ref(editingDiscount.value?.category || managerCategories[0])
const linkUrl = ref(editingDiscount.value?.linkUrl || '')
const emoji = ref(editingDiscount.value?.emoji || '🍔')

const previewTitle = computed(() => title.value.trim() || 'Название скидки')
const previewDesc = computed(() => description.value.trim() || 'Описание скидки...')
const previewEmoji = computed(() => emoji.value.trim() || '📋')

function submitForm() {
  const payload = {
    title: title.value,
    description: description.value,
    percentNumber: percent.value,
    category: category.value,
    linkUrl: linkUrl.value,
    emoji: emoji.value,
  }

  if (isEditMode.value) updateDiscount(discountId.value, payload)
  else createDiscount(payload)

  router.push({ name: 'manager-discounts' })
}
</script>

<template>
  <div class="admin-page admin-container">
    <header class="admin-page-head">
      <div class="admin-page-title">
        <span class="mgr-create-icon" aria-hidden="true">+</span>
        <div>
          <h1>{{ isEditMode ? 'Редактировать скидку' : 'Создать скидку' }}</h1>
          <p>
            {{
              isEditMode
                ? 'Обновите условия предложения и сохраните изменения'
                : 'Добавьте новое предложение для студентов'
            }}
          </p>
        </div>
      </div>
    </header>

    <div class="mgr-form-card">
      <form class="mgr-form" @submit.prevent="submitForm">
        <div class="mgr-form__row">
          <label class="mgr-form-label" for="offer-title">📄 Название предложения</label>
          <input
            id="offer-title"
            v-model="title"
            type="text"
            class="mgr-form-input"
            placeholder="15% скидка на все меню"
          />
        </div>

        <div class="mgr-form__row">
          <label class="mgr-form-label" for="offer-desc">Описание</label>
          <textarea
            id="offer-desc"
            v-model="description"
            class="mgr-form-textarea"
            rows="4"
            placeholder="Подробное описание скидки и условий получения..."
          />
        </div>

        <div class="mgr-form__grid2">
          <div class="mgr-form__row">
            <label class="mgr-form-label" for="offer-pct">Размер скидки (%)</label>
            <input id="offer-pct" v-model.number="percent" type="number" min="0" max="100" class="mgr-form-input" />
          </div>
          <div class="mgr-form__row">
            <label class="mgr-form-label" for="offer-cat">🏷 Категория</label>
            <div class="mgr-form-select-wrap">
              <select id="offer-cat" v-model="category" class="mgr-form-select">
                <option v-for="c in managerCategories" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="mgr-form__row">
          <label class="mgr-form-label" for="offer-link">🔗 Ссылка для получения скидки</label>
          <input
            id="offer-link"
            v-model="linkUrl"
            type="url"
            class="mgr-form-input"
            placeholder="https://yourwebsite.com/student-discount"
          />
          <p class="mgr-form-hint">
            Студенты будут переходить по этой ссылке при нажатии «Получить»
          </p>
        </div>

        <div class="mgr-form__row mgr-form__row--emoji">
          <label class="mgr-form-label" for="offer-emoji">🖼 Эмодзи (иконка)</label>
          <input id="offer-emoji" v-model="emoji" type="text" class="mgr-form-input mgr-form-input--emoji" maxlength="4" />
        </div>

        <button type="submit" class="admin-btn admin-btn--primary mgr-form-submit">
          {{ isEditMode ? 'Сохранить изменения' : 'Опубликовать скидку' }}
        </button>
      </form>

      <div class="mgr-preview-block">
        <h3>Предпросмотр:</h3>
        <div class="mgr-preview-card">
          <span class="mgr-preview-emoji">{{ previewEmoji }}</span>
          <strong>{{ previewTitle }}</strong>
          <p>{{ previewDesc }}</p>
          <span class="mgr-preview-cat">{{ category }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

import { ref } from 'vue'

const openMode = ref(null)

export function useAdminPartnerModals() {
  const openAddManager = () => {
    openMode.value = 'manager'
  }
  const openCreateCompany = () => {
    openMode.value = 'company'
  }
  const close = () => {
    openMode.value = null
  }

  return {
    openMode,
    openAddManager,
    openCreateCompany,
    close,
  }
}

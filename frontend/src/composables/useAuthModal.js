import { ref } from 'vue'

const openMode = ref(null)

export function useAuthModal() {
  const openRegister = () => {
    openMode.value = 'register'
  }
  const openLogin = () => {
    openMode.value = 'login'
  }
  const close = () => {
    openMode.value = null
  }

  return {
    openMode,
    openRegister,
    openLogin,
    close,
  }
}

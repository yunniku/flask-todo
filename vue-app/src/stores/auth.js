import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)

  async function fetchUser() {
    try {
      const res = await axios.get('/api/me')
      user.value = res.data.user
      isAuthenticated.value = true
    } catch {
      user.value = null
      isAuthenticated.value = false
    }
  }

  async function logout() {
    await axios.post('/api/logout')
    user.value = null
    isAuthenticated.value = false
  }

  return { user, isAuthenticated, fetchUser, logout }
})

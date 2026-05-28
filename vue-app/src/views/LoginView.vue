<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title text-center mb-4">
              <i class="bi bi-check2-square"></i> Flask Todo
            </h4>
            <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
            <div class="mb-3">
              <input
                type="email"
                class="form-control"
                placeholder="이메일"
                v-model="form.email"
              >
            </div>
            <div class="mb-3">
              <input
                type="password"
                class="form-control"
                placeholder="비밀번호"
                v-model="form.password"
                @keyup.enter="handleLogin"
              >
            </div>
            <button class="btn btn-dark w-100" @click="handleLogin" :disabled="loading">
              {{ loading ? '로그인 중...' : '로그인' }}
            </button>
            <div class="text-center mt-3">
              <small>계정이 없으신가요? <RouterLink to="/register">회원가입</RouterLink></small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ email: '', password: '' })
const errorMsg = ref('')
const loading = ref(false)

async function handleLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    const res = await axios.post('/api/login', form.value)
    if (res.data.success) {
      await auth.fetchUser()
      router.push('/dashboard')
    }
  } catch (err) {
    errorMsg.value = err.response?.data?.message || '로그인 실패!'
  } finally {
    loading.value = false
  }
}
</script>

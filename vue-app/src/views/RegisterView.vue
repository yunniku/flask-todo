<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title text-center mb-4">
              <i class="bi bi-check2-square"></i> 회원가입
            </h4>
            <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
            <div v-if="successMsg" class="alert alert-success">{{ successMsg }}</div>
            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                placeholder="아이디"
                v-model="form.username"
              >
            </div>
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
                @keyup.enter="handleRegister"
              >
            </div>
            <button class="btn btn-dark w-100" @click="handleRegister" :disabled="loading">
              {{ loading ? '처리 중...' : '회원가입' }}
            </button>
            <div class="text-center mt-3">
              <small>이미 계정이 있으신가요? <RouterLink to="/login">로그인</RouterLink></small>
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
import axios from 'axios'

const router = useRouter()

const form = ref({ username: '', email: '', password: '' })
const errorMsg = ref('')
const successMsg = ref('')
const loading = ref(false)

async function handleRegister() {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    const res = await axios.post('/api/register', form.value)
    if (res.data.success) {
      successMsg.value = res.data.message
      setTimeout(() => router.push('/login'), 1500)
    }
  } catch (err) {
    errorMsg.value = err.response?.data?.message || '회원가입 실패!'
  } finally {
    loading.value = false
  }
}
</script>

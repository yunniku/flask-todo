<template>
  <div class="mt-4">
    <div class="row g-4">

      <!-- 왼쪽: 기념일 추가 폼 -->
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h5 class="card-title mb-3">
              <i class="bi bi-plus-circle"></i> 기념일 추가
            </h5>
            <div class="mb-3">
              <input type="text" class="form-control" placeholder="기념일 이름 *" v-model="form.title">
            </div>
            <div class="mb-3">
              <input type="text" class="form-control" placeholder="이모지 (예: 🎂)" v-model="form.emoji">
            </div>
            <div class="mb-3">
              <label class="form-label text-muted small">날짜 *</label>
              <input type="date" class="form-control" v-model="form.date">
            </div>
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="repeat" v-model="form.repeat_yearly">
              <label class="form-check-label" for="repeat">매년 반복</label>
            </div>
            <button class="btn btn-dark w-100" @click="addAnniversary">
              <i class="bi bi-plus"></i> 추가하기
            </button>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 기념일 목록 -->
      <div class="col-md-8">
        <h5 class="mb-4 mt-2">
          <i class="bi bi-balloon-heart"></i> 기념일 목록
          <span class="badge bg-secondary">{{ anniversaries.length }}</span>
        </h5>

        <div v-if="anniversaries.length === 0" class="text-center py-5 text-muted">
          <i class="bi bi-calendar-heart" style="font-size: 3rem;"></i>
          <p class="mt-2">기념일을 추가해보세요! 🎂</p>
        </div>

        <div v-for="ann in anniversaries" :key="ann.id" class="card shadow-sm mb-2">
          <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">{{ ann.emoji }} {{ ann.title }}</h6>
                <div class="d-flex gap-2">
                  <span class="badge bg-secondary">{{ ann.date }}</span>
                  <span v-if="ann.repeat_yearly" class="badge bg-info text-dark">매년 반복</span>
                </div>
              </div>
              <div class="d-flex align-items-center gap-2">
                <span class="badge fs-6"
                  :class="ann.dday === 0 ? 'bg-danger' : ann.dday <= 7 ? 'bg-warning text-dark' : 'bg-secondary'">
                  {{ ann.dday_str }}
                </span>
                <button class="btn btn-sm btn-outline-danger" @click="deleteAnniversary(ann.id)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const anniversaries = ref([])
const form = ref({ title: '', emoji: '🎉', date: '', repeat_yearly: false })

async function fetchAnniversaries() {
  try {
    const res = await axios.get('/api/anniversary')
    if (res.data.success) anniversaries.value = res.data.anniversaries
  } catch (err) {
    console.error('기념일 로딩 실패:', err)
  }
}

async function addAnniversary() {
  if (!form.value.title.trim() || !form.value.date) return alert('이름과 날짜를 입력해주세요!')
  try {
    const res = await axios.post('/api/anniversary', form.value)
    if (res.data.success) {
      await fetchAnniversaries()
      form.value = { title: '', emoji: '🎉', date: '', repeat_yearly: false }
    }
  } catch (err) {
    console.error('추가 실패:', err)
  }
}

async function deleteAnniversary(id) {
  if (!confirm('정말 삭제할까요?')) return
  try {
    const res = await axios.delete(`/api/anniversary/${id}`)
    if (res.data.success) await fetchAnniversaries()
  } catch (err) {
    console.error('삭제 실패:', err)
  }
}

onMounted(fetchAnniversaries)
</script>

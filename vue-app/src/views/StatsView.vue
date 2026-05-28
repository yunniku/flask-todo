<template>
  <div class="mt-4">

    <!-- 전체 요약 -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card shadow-sm text-center p-3">
          <div style="font-size:2rem;font-weight:700;color:#6c63ff">{{ stats.total_todos }}</div>
          <div class="text-muted small">전체 할 일</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm text-center p-3">
          <div style="font-size:2rem;font-weight:700;color:#1db97a">{{ stats.done_todos }}</div>
          <div class="text-muted small">완료한 일</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm text-center p-3">
          <div style="font-size:2rem;font-weight:700;color:#f0a500">{{ stats.total_todos - stats.done_todos }}</div>
          <div class="text-muted small">진행 중</div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm text-center p-3">
          <div style="font-size:2rem;font-weight:700;color:#D4537E">{{ totalRate }}%</div>
          <div class="text-muted small">전체 달성률</div>
        </div>
      </div>
    </div>

    <div class="row g-4">

      <!-- 월별 통계 -->
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h6 class="card-title mb-3"><i class="bi bi-bar-chart"></i> 월별 완료 통계</h6>
            <div v-for="m in stats.monthly_stats" :key="m.month" class="mb-3">
              <div class="d-flex justify-content-between small mb-1">
                <span>{{ m.month }}</span>
                <span>{{ m.done }} / {{ m.total }} ({{ m.rate }}%)</span>
              </div>
              <div class="home-goal-bar">
                <div class="home-goal-fill" :style="{ width: m.rate + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 카테고리별 통계 -->
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h6 class="card-title mb-3"><i class="bi bi-tag"></i> 카테고리별 통계</h6>
            <div v-if="stats.cat_stats.length === 0" class="text-muted small">카테고리 데이터가 없어요!</div>
            <div v-for="cat in stats.cat_stats" :key="cat.category" class="mb-3">
              <div class="d-flex justify-content-between small mb-1">
                <span>{{ cat.category }}</span>
                <span>{{ cat.done }} / {{ cat.total }} ({{ cat.rate }}%)</span>
              </div>
              <div class="home-goal-bar">
                <div class="home-goal-fill" :style="{ width: cat.rate + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({
  total_todos: 0,
  done_todos: 0,
  monthly_stats: [],
  cat_stats: []
})

const totalRate = computed(() => {
  if (!stats.value.total_todos) return 0
  return Math.round(stats.value.done_todos / stats.value.total_todos * 100)
})

async function fetchStats() {
  try {
    const res = await axios.get('/api/stats')
    if (res.data.success) stats.value = res.data
  } catch (err) {
    console.error('통계 로딩 실패:', err)
  }
}

onMounted(fetchStats)
</script>

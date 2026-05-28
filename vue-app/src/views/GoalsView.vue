<template>
  <div class="mt-4">

    <div class="row g-4">
      <!-- 왼쪽: 목표 추가 폼 -->
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h5 class="card-title mb-3">
              <i class="bi bi-plus-circle"></i> 목표 추가
            </h5>
            <div class="mb-3">
              <input type="text" class="form-control" placeholder="목표 제목 *" v-model="form.title">
            </div>
            <div class="mb-3">
              <textarea class="form-control" placeholder="설명 (선택)" rows="2" v-model="form.description"></textarea>
            </div>
            <div class="mb-3">
              <select class="form-select" v-model="form.goal_type">
                <option value="daily">오늘 목표</option>
                <option value="weekly">이번 주 목표</option>
                <option value="monthly">이번 달 목표</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label text-muted small">목표일</label>
              <input type="date" class="form-control" v-model="form.target_date">
            </div>
            <button class="btn btn-dark w-100" @click="addGoal">
              <i class="bi bi-plus"></i> 추가하기
            </button>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 목표 목록 -->
      <div class="col-md-8">

        <!-- 달성률 -->
        <div class="card shadow-sm mb-4">
          <div class="card-body p-3">
            <div class="home-goal-row">
              <div class="home-goal-label"><span>오늘</span><span style="color:#6c63ff">{{ rates.daily }}%</span></div>
              <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: rates.daily + '%' }"></div></div>
            </div>
            <div class="home-goal-row">
              <div class="home-goal-label"><span>이번 주</span><span style="color:#6c63ff">{{ rates.weekly }}%</span></div>
              <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: rates.weekly + '%' }"></div></div>
            </div>
            <div class="home-goal-row">
              <div class="home-goal-label"><span>이번 달</span><span style="color:#6c63ff">{{ rates.monthly }}%</span></div>
              <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: rates.monthly + '%' }"></div></div>
            </div>
          </div>
        </div>

        <!-- 오늘 목표 -->
        <h6 class="mb-2"><i class="bi bi-sun"></i> 오늘 목표</h6>
        <div v-if="goals.daily.length === 0" class="text-muted small mb-3">오늘 목표가 없어요!</div>
        <div v-for="goal in goals.daily" :key="goal.id" class="card shadow-sm mb-2" :class="{ 'done-card': goal.achieved }">
          <div class="card-body p-3 d-flex justify-content-between align-items-center">
            <span :class="{ 'done-text': goal.achieved }">{{ goal.title }}</span>
            <div class="d-flex gap-1">
              <button class="btn btn-sm" :class="goal.achieved ? 'btn-success' : 'btn-outline-success'" @click="toggleGoal(goal)">
                <i class="bi bi-check"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteGoal(goal.id)">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 이번 주 목표 -->
        <h6 class="mb-2 mt-3"><i class="bi bi-calendar-week"></i> 이번 주 목표</h6>
        <div v-if="goals.weekly.length === 0" class="text-muted small mb-3">이번 주 목표가 없어요!</div>
        <div v-for="goal in goals.weekly" :key="goal.id" class="card shadow-sm mb-2" :class="{ 'done-card': goal.achieved }">
          <div class="card-body p-3 d-flex justify-content-between align-items-center">
            <span :class="{ 'done-text': goal.achieved }">{{ goal.title }}</span>
            <div class="d-flex gap-1">
              <button class="btn btn-sm" :class="goal.achieved ? 'btn-success' : 'btn-outline-success'" @click="toggleGoal(goal)">
                <i class="bi bi-check"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteGoal(goal.id)">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 이번 달 목표 -->
        <h6 class="mb-2 mt-3"><i class="bi bi-calendar-month"></i> 이번 달 목표</h6>
        <div v-if="goals.monthly.length === 0" class="text-muted small mb-3">이번 달 목표가 없어요!</div>
        <div v-for="goal in goals.monthly" :key="goal.id" class="card shadow-sm mb-2" :class="{ 'done-card': goal.achieved }">
          <div class="card-body p-3 d-flex justify-content-between align-items-center">
            <span :class="{ 'done-text': goal.achieved }">{{ goal.title }}</span>
            <div class="d-flex gap-1">
              <button class="btn btn-sm" :class="goal.achieved ? 'btn-success' : 'btn-outline-success'" @click="toggleGoal(goal)">
                <i class="bi bi-check"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteGoal(goal.id)">
                <i class="bi bi-trash"></i>
              </button>
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

const goals = ref({ daily: [], weekly: [], monthly: [] })
const rates = ref({ daily: 0, weekly: 0, monthly: 0 })
const form = ref({ title: '', description: '', goal_type: 'daily', target_date: '' })

async function fetchGoals() {
  try {
    const res = await axios.get('/api/goals')
    goals.value = { daily: res.data.daily, weekly: res.data.weekly, monthly: res.data.monthly }
    rates.value = { daily: res.data.daily_rate, weekly: res.data.weekly_rate, monthly: res.data.monthly_rate }
  } catch (err) {
    console.error('목표 로딩 실패:', err)
  }
}

async function addGoal() {
  if (!form.value.title.trim()) return alert('목표 제목을 입력해주세요!')
  try {
    const res = await axios.post('/api/goals', form.value)
    if (res.data.success) {
      await fetchGoals()
      form.value = { title: '', description: '', goal_type: 'daily', target_date: '' }
    }
  } catch (err) {
    console.error('추가 실패:', err)
  }
}

async function toggleGoal(goal) {
  try {
    const res = await axios.put(`/api/goals/${goal.id}/toggle`)
    if (res.data.success) {
      goal.achieved = res.data.achieved
      await fetchGoals()
    }
  } catch (err) {
    console.error('토글 실패:', err)
  }
}

async function deleteGoal(id) {
  if (!confirm('정말 삭제할까요?')) return
  try {
    const res = await axios.delete(`/api/goals/${id}`)
    if (res.data.success) await fetchGoals()
  } catch (err) {
    console.error('삭제 실패:', err)
  }
}

onMounted(fetchGoals)
</script>

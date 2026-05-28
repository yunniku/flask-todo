<template>
  <div class="home-wrap">

    <!-- 인사말 배너 -->
    <div class="greeting-banner">
      <div class="greeting-left">
        <div class="greeting-date">{{ nowDate }}</div>
        <div class="greeting-text">안녕하세요, {{ auth.user?.username }}님! 👋</div>
        <div class="greeting-sub">오늘도 하루 잘 보내세요 🌟</div>
      </div>
      <div class="greeting-mood">{{ todayMood }}</div>
    </div>

    <!-- 핵심 숫자 4개 -->
    <div class="quick-grid">
      <RouterLink to="/todos" class="quick-card">
        <div class="quick-icon">📝</div>
        <div class="quick-num" style="color:#6c63ff">{{ stats.ongoing }}</div>
        <div class="quick-label">오늘 할 일</div>
      </RouterLink>
      <RouterLink to="/goals" class="quick-card">
        <div class="quick-icon">🎯</div>
        <div class="quick-num" style="color:#1db97a">{{ stats.dailyRate }}%</div>
        <div class="quick-label">목표 달성</div>
      </RouterLink>
      <RouterLink to="/anniversary" class="quick-card">
        <div class="quick-icon">🎂</div>
        <div class="quick-num" style="color:#D4537E">{{ nextDday }}</div>
        <div class="quick-label">다음 기념일</div>
      </RouterLink>
      <RouterLink to="/diary" class="quick-card">
        <div class="quick-icon">📔</div>
        <div class="quick-num" style="color:#f0a500">{{ stats.done }}</div>
        <div class="quick-label">완료한 일</div>
      </RouterLink>
    </div>

    <!-- 하단 4개 카드 -->
    <div class="home-grid">

      <!-- 오늘 할 일 -->
      <div class="home-card">
        <div class="home-card-header">
          <div class="home-card-title">📝 오늘 할 일</div>
          <RouterLink to="/todos" class="home-card-more">전체보기 →</RouterLink>
        </div>
        <template v-if="todayTodos.length > 0">
          <div v-for="todo in todayTodos.slice(0, 4)" :key="todo.id" class="home-todo-item">
            <a href="#" class="home-check" :class="{ done: todo.done }"
               @click.prevent="toggleTodo(todo)">
              <i v-if="todo.done" class="bi bi-check"></i>
            </a>
            <span class="home-todo-text" :class="{ 'done-text': todo.done }">{{ todo.title }}</span>
          </div>
          <div v-if="todayTodos.length > 4" class="home-more-text">
            + {{ todayTodos.length - 4 }}개 더 있어요
          </div>
        </template>
        <div v-else class="home-empty">오늘 할 일이 없어요 😊</div>
      </div>

      <!-- D-day -->
      <div class="home-card">
        <div class="home-card-header">
          <div class="home-card-title">🎂 D-day</div>
          <RouterLink to="/anniversary" class="home-card-more">전체보기 →</RouterLink>
        </div>
        <template v-if="ddays.length > 0">
          <div v-for="d in ddays.slice(0, 4)" :key="d.title" class="home-dday-item">
            <span class="home-dday-name">{{ d.emoji }} {{ d.title }}</span>
            <span class="home-dday-badge" :class="{ today: d.dday === 0, soon: d.dday <= 7 && d.dday > 0 }">
              {{ d.dday_str }}
            </span>
          </div>
        </template>
        <div v-else class="home-empty">
          기념일을 추가해보세요!
          <RouterLink to="/anniversary" class="home-add-link">추가하기 →</RouterLink>
        </div>
      </div>

      <!-- 목표 달성률 -->
      <div class="home-card">
        <div class="home-card-header">
          <div class="home-card-title">🎯 목표 달성률</div>
          <RouterLink to="/goals" class="home-card-more">전체보기 →</RouterLink>
        </div>
        <div class="home-goal-row">
          <div class="home-goal-label"><span>오늘</span><span style="color:#6c63ff">{{ stats.dailyRate }}%</span></div>
          <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: stats.dailyRate + '%' }"></div></div>
        </div>
        <div class="home-goal-row">
          <div class="home-goal-label"><span>이번 주</span><span style="color:#6c63ff">{{ stats.weeklyRate }}%</span></div>
          <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: stats.weeklyRate + '%' }"></div></div>
        </div>
        <div class="home-goal-row">
          <div class="home-goal-label"><span>이번 달</span><span style="color:#6c63ff">{{ stats.monthlyRate }}%</span></div>
          <div class="home-goal-bar"><div class="home-goal-fill" :style="{ width: stats.monthlyRate + '%' }"></div></div>
        </div>
      </div>

      <!-- 오늘 한 줄 다이어리 -->
      <div class="home-card">
        <div class="home-card-header">
          <div class="home-card-title">📔 오늘 한 줄</div>
          <RouterLink to="/diary" class="home-card-more">다이어리 →</RouterLink>
        </div>
        <template v-if="todayDiary">
          <div class="home-diary-box">{{ todayDiary.content?.slice(0, 100) }}{{ todayDiary.content?.length > 100 ? '...' : '' }}</div>
        </template>
        <div v-else class="home-empty">
          오늘 하루를 기록해보세요!
          <RouterLink to="/diary" class="home-add-link">기록하기 →</RouterLink>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const auth = useAuthStore()

const todayTodos = ref([])
const ddays = ref([])
const todayDiary = ref(null)
const stats = ref({ ongoing: 0, done: 0, dailyRate: 0, weeklyRate: 0, monthlyRate: 0 })

const nowDate = new Date().toISOString().slice(0, 10)
const todayMood = computed(() => todayDiary.value?.mood || '😊')
const nextDday = computed(() => ddays.value[0]?.dday_str || '-')

async function fetchDashboard() {
  try {
    const res = await axios.get('/api/dashboard')
    const d = res.data
    todayTodos.value = d.today_todos
    ddays.value = d.dday_list
    todayDiary.value = d.today_diary
    stats.value = {
      ongoing: d.ongoing_todos,
      done: d.done_todos,
      dailyRate: d.daily_rate,
      weeklyRate: d.weekly_rate,
      monthlyRate: d.monthly_rate
    }
  } catch (err) {
    console.error('대시보드 로딩 실패:', err)
  }
}

async function toggleTodo(todo) {
  try {
    const res = await axios.put(`/api/todos/${todo.id}`, { done: !todo.done })
    if (res.data.success) todo.done = !todo.done
  } catch (err) {
    console.error('토글 실패:', err)
  }
}

onMounted(fetchDashboard)
</script>

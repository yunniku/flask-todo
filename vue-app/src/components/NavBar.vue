<template>
  <!-- 데스크탑 네비게이션 -->
  <nav class="navbar navbar-expand-lg d-none d-lg-flex">
    <div class="container-fluid px-4">
      <a class="navbar-brand" href="/dashboard">
        <i class="bi bi-check2-square"></i> Flask Todo
      </a>
      <div class="navbar-nav mx-auto">
        <RouterLink class="nav-link" :class="{ active: route.path === '/dashboard' }" to="/dashboard">
          <i class="bi bi-grid"></i> 대시보드
        </RouterLink>
        <RouterLink class="nav-link" :class="{ active: route.path === '/todos' }" to="/todos">
          <i class="bi bi-list-check"></i> 할 일
        </RouterLink>
        <RouterLink class="nav-link" :class="{ active: route.path === '/goals' }" to="/goals">
          <i class="bi bi-trophy"></i> 목표
        </RouterLink>
        <RouterLink class="nav-link" :class="{ active: route.path === '/anniversary' }" to="/anniversary">
          <i class="bi bi-balloon-heart"></i> 기념일
        </RouterLink>
        <RouterLink class="nav-link" :class="{ active: route.path === '/diary' }" to="/diary">
          <i class="bi bi-journal-richtext"></i> 다이어리
        </RouterLink>
        <RouterLink class="nav-link" :class="{ active: route.path === '/stats' }" to="/stats">
          <i class="bi bi-bar-chart"></i> 통계
        </RouterLink>
      </div>
      <div class="navbar-nav ms-auto">
        <span class="navbar-text me-3">👋 {{ auth.user?.username }}님</span>
        <a class="nav-link" href="#" @click.prevent="handleLogout">로그아웃</a>
      </div>
    </div>
  </nav>

  <!-- 모바일 상단 헤더 -->
  <div class="mobile-header d-lg-none">
    <div class="mobile-header-brand">
      <i class="bi bi-check2-square"></i> Flask Todo
    </div>
    <div class="mobile-header-user">
      👋 {{ auth.user?.username }}님
      <a href="#" class="mobile-logout" @click.prevent="handleLogout">로그아웃</a>
    </div>
  </div>

  <!-- 모바일 하단 네비게이션 -->
  <nav class="mobile-bottom-nav d-lg-none">
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/dashboard' }" to="/dashboard">
      <i class="bi bi-grid"></i>
      <span>홈</span>
    </RouterLink>
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/todos' }" to="/todos">
      <i class="bi bi-list-check"></i>
      <span>할 일</span>
    </RouterLink>
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/goals' }" to="/goals">
      <i class="bi bi-trophy"></i>
      <span>목표</span>
    </RouterLink>
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/anniversary' }" to="/anniversary">
      <i class="bi bi-balloon-heart"></i>
      <span>기념일</span>
    </RouterLink>
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/diary' }" to="/diary">
      <i class="bi bi-journal-richtext"></i>
      <span>다이어리</span>
    </RouterLink>
    <RouterLink class="mobile-nav-item" :class="{ active: route.path === '/stats' }" to="/stats">
      <i class="bi bi-bar-chart"></i>
      <span>통계</span>
    </RouterLink>
  </nav>
</template>

<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

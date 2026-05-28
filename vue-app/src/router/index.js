import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/todos', component: () => import('../views/TodosView.vue'), meta: { requiresAuth: true } },
  { path: '/goals', component: () => import('../views/GoalsView.vue'), meta: { requiresAuth: true } },
  { path: '/diary', component: () => import('../views/DiaryView.vue'), meta: { requiresAuth: true } },
  { path: '/anniversary', component: () => import('../views/AnniversaryView.vue'), meta: { requiresAuth: true } },
  { path: '/stats', component: () => import('../views/StatsView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('../stores/auth')
  const auth = useAuthStore()

  if (!auth.user) await auth.fetchUser()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && auth.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router

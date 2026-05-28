<template>
  <div>
    <template v-if="auth.isAuthenticated">
      <NavBar />
      <div class="main-content">
        <div class="container-fluid px-3 px-lg-4">
          <RouterView />
        </div>
      </div>
    </template>
    <template v-else>
      <RouterView />
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import NavBar from './components/NavBar.vue'

const auth = useAuthStore()

onMounted(async () => {
  await auth.fetchUser()
})
</script>

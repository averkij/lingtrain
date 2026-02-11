import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/pages/Landing.vue'),
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('@/pages/Main.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/pages/Admin.vue'),
      meta: { requiresAuth: true, requiresRole: 'admin' },
    },
  ],
})

let initialized = false

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!initialized && authStore.token) {
    initialized = true
    await authStore.fetchUser()
  }

  if (to.name === 'landing' && authStore.isAuthenticated) {
    return { name: 'main' }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'landing' }
  }

  if (to.meta.requiresRole && authStore.user?.role !== to.meta.requiresRole) {
    return { name: 'main' }
  }
})

export default router

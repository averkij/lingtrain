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
      path: '/',
      component: () => import('@/pages/Main.vue'),
      children: [
        {
          path: 'aligner',
          component: () => import('@/pages/Aligner.vue'),
          redirect: { name: 'aligner-documents' },
          children: [
            {
              path: 'documents',
              name: 'aligner-documents',
              component: () => import('@/pages/aligner/Documents.vue'),
            },
            {
              path: 'alignments',
              name: 'aligner-alignments',
              component: () => import('@/pages/aligner/Alignments.vue'),
            },
            {
              path: 'alignments/:guid',
              name: 'aligner-alignment-detail',
              component: () => import('@/components/aligner/AlignmentDetail.vue'),
            },
            {
              path: 'create',
              name: 'aligner-create',
              component: () => import('@/pages/aligner/Create.vue'),
            },
          ],
        },
      ],
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
    return { name: 'aligner-documents' }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'landing' }
  }

  if (to.meta.requiresRole && authStore.user?.role !== to.meta.requiresRole) {
    return { name: 'aligner-documents' }
  }
})

export default router

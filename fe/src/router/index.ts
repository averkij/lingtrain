import { createRouter, createWebHistory } from 'vue-router'

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
  ],
})

export default router

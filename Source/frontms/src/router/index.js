import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';  // 登录页面组件
import StudentDashboard from '@/components/StudentDashboard.vue';  // 学生仪表板页面组件

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true }  // 添加 meta 字段，用于验证登录
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated'); // 检查登录状态
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果需要登录并且用户未登录，则重定向到登录页面
    next({ name: 'Login' });
  } else {
    next(); // 否则允许访问
  }
});

export default router;


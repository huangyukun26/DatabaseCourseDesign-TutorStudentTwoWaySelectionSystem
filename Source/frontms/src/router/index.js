import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';  // 登录页面组件
import StudentDashboard from '@/components/StudentDashboard.vue';  // 学生仪表板页面组件
import BasicInfo from '@/components/BasicInfo.vue';  // 导入基本信息组件
import StudentVolunteerSelection from "@/components/StudentVolunteerSelection.vue";

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
    meta: { requiresAuth: true },// 添加 meta 字段，用于验证登录
    children: [
    {
      path: 'basic-info',
      name: 'basic-info',
      component: BasicInfo
    },
    {
    path: '/student-volunteer-selection',
    name: 'student-volunteer-selection',
    component: StudentVolunteerSelection
  }
  ]
  },
  {
    path: '/basic-info',  // 添加基本信息的路由
    name: 'BasicInfo',
    component: BasicInfo,
    meta: { requiresAuth: true }
  }

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


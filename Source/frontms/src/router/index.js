import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';  //登录页面组件
import StudentDashboard from '@/components/StudentDashboard.vue';  //学生仪表板页面组件
import BasicInfo from '@/components/BasicInfo.vue';
import StudentVolunteerSelection from "@/components/StudentVolunteerSelection.vue";
import StudentScoreQuery from "@/components/StudentScoreQuery.vue";
import StudentAdmissionStatus from "@/components/StudentAdmissionStatus.vue";
import AdmissionPlan from "@/components/AdmissionPlan.vue";
import MentorStudentList from "@/components/MentorStudentList.vue";
import MentorAcceptedStudents from '@/components/MentorAcceptedStudents.vue'
import MentorAllApplications from '@/components/MentorAllApplications.vue'
import MentorBasicInfo from '@/components/MentorBasicInfo.vue'
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
    meta: { requiresAuth: true },//添加 meta 字段，用于验证登录
    children: [
    {
      path: 'basic-info',
      name: 'basic-info',
      component: BasicInfo,
      meta: { requiresAuth: true }
    },
    {
    path: 'volunteer',
    name: 'student-volunteer-selection',
    component: StudentVolunteerSelection,
    meta: { requiresAuth: true }
    },
    {
    path: 'scores',
    name: 'student-scores',
    component: StudentScoreQuery,
    meta: { requiresAuth: true }
    },
    {
      path: 'admission-status',
      name: 'student-admission-status',
      component: StudentAdmissionStatus,
      meta: { requiresAuth: true }
    },
    {
      path: 'admission-plan',
      name: 'student-admission-plan',
      component: AdmissionPlan,
      meta: { requiresAuth: true }
    },

  ]
  },

  {
    path: '/mentor/dashboard',
    name: 'MentorDashboard',
    component: () => import('@/components/MentorDashboard.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'sutdent-list',
        name: 'mentor-student-list',
        component: MentorStudentList,
        meta: { requiresAuth: true }
      },
      {
      path: 'admission-plan',
      name: 'mentor-admission-plan',
      component: AdmissionPlan,
      meta: { requiresAuth: true }
      },
      {
        path: 'accepted-students',
        name: 'mentor-accepted-students',
        component: MentorAcceptedStudents
      },
      {
        path: 'all-applications',
        name: 'mentor-all-applications',
        component: MentorAllApplications
      },
      {
        path: 'basic-info',
        name: 'mentor-basic-info',
        component: MentorBasicInfo,
        meta: { requiresAuth: true }
      }

      ]
  },

  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated'); // 检查登录状态
  if (to.meta.requiresAuth && !isAuthenticated) {
    //如果需要登录并且用户未登录，则重定向到登录页面
    next({ name: 'Login' });
  } else {
    next(); //否则允许访问
  }
});

export default router;


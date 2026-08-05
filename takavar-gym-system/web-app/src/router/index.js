import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import Members from '@/views/Members/MemberList.vue'
import MemberDetail from '@/views/Members/MemberDetail.vue'
import Subscriptions from '@/views/Subscriptions/SubscriptionList.vue'
import Payments from '@/views/Payments/PaymentList.vue'
import Attendance from '@/views/Attendance/AttendanceTracker.vue'
import Workouts from '@/views/Workouts/WorkoutPlan.vue'
import Schedule from '@/views/Schedule/ScheduleView.vue'
import Trainers from '@/views/Trainers/TrainerList.vue'
import Equipment from '@/views/Equipment/EquipmentList.vue'
import Nutrition from '@/views/Nutrition/MealPlan.vue'
import Products from '@/views/Products/ProductList.vue'
import Reports from '@/views/Reports/ReportGenerator.vue'
import Settings from '@/views/Settings.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/members',
    name: 'Members',
    component: Members,
    meta: { requiresAuth: true },
  },
  {
    path: '/members/:id',
    name: 'MemberDetail',
    component: MemberDetail,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/subscriptions',
    name: 'Subscriptions',
    component: Subscriptions,
    meta: { requiresAuth: true },
  },
  {
    path: '/payments',
    name: 'Payments',
    component: Payments,
    meta: { requiresAuth: true },
  },
  {
    path: '/attendance',
    name: 'Attendance',
    component: Attendance,
    meta: { requiresAuth: true },
  },
  {
    path: '/workouts',
    name: 'Workouts',
    component: Workouts,
    meta: { requiresAuth: true },
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule,
    meta: { requiresAuth: true },
  },
  {
    path: '/trainers',
    name: 'Trainers',
    component: Trainers,
    meta: { requiresAuth: true },
  },
  {
    path: '/equipment',
    name: 'Equipment',
    component: Equipment,
    meta: { requiresAuth: true },
  },
  {
    path: '/nutrition',
    name: 'Nutrition',
    component: Nutrition,
    meta: { requiresAuth: true },
  },
  {
    path: '/products',
    name: 'Products',
    component: Products,
    meta: { requiresAuth: true },
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('takavar_token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default routes

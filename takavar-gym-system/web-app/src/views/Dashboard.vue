<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="dashboard-header mb-6">
      <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
        🏋️ پنجره اصلی سیستم مدیریت باشگاه بدنسازی تکاور
      </h1>
      <p class="text-body-2 text-grey mt-1">
        خوش آمدید، {{ currentUser?.first_name || 'کاربر' }}! امروز {{ currentDate }} می‌باشد.
      </p>
    </div>

    <!-- Stats cards -->
    <div class="d-flex flex-wrap gap-4 mb-6">
      <v-card
        v-for="stat in stats"
        :key="stat.title"
        class="stat-card pa-4"
        :class="{ 'stat-highlight': stat.highlight }"
        max-width="200"
        flex-grow="1"
      >
        <div class="d-flex align-center gap-3">
          <v-avatar
            :color="stat.color"
            size="48"
            class="white--text"
          >
            <v-icon size="24">{{ stat.icon }}</v-icon>
          </v-avatar>
          <div class="flex-grow-1">
            <div class="text-h4 font-weight-bold" :style="{ color: stat.color }">
              {{ stat.value }}
            </div>
            <div class="text-caption text-grey">{{ stat.title }}</div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Content grid -->
    <div class="d-flex flex-wrap gap-4">
      <!-- Recent members -->
      <v-card class="flex-grow-1" min-width="350" max-width="600">
        <v-card-item>
          <template #prepend>
            <v-avatar color="primary" size="40">
              <v-icon>mdi-account-group</v-icon>
            </v-avatar>
          </template>
          <v-card-title>اخیرین اعضا</v-card-title>
          <v-card-subtitle>لیست اعضای Recently ثبت‌نام کرده‌اند</v-card-subtitle>
        </v-card-item>

        <v-divider></v-divider>

        <v-list dense class="rounded-b-xl">
          <v-list-item
            v-for="member in recentMembers"
            :key="member.id"
            :to="`/members/${member.id}`"
            class="pa-2"
            link
          >
            <template #prepend>
              <v-avatar
                :color="member.status === 'active' ? 'green' : 'grey'"
                size="36"
              >
                <v-icon size="18">{{ member.gender === 'male' ? 'mdi-account-male' : 'mdi-account-female' }}</v-icon>
              </v-avatar>
            </template>
            <v-list-item-title class="text-body-2 font-weight-medium">
              {{ member.first_name }} {{ member.last_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-caption">
              {{ member.phone || 'بدون تلفن' }} | {{ member.membership_type }}
            </v-list-item-subtitle>
            <template #append>
              <v-chip
                :color="member.status === 'active' ? 'green' : member.status === 'suspended' ? 'red' : 'yellow'"
                size="x-small"
                variant="tonal"
              >
                {{ member.status }}
              </v-chip>
            </template>
          </v-list-item>

          <v-list-item v-if="recentMembers.length === 0">
            <v-list-item-title class="text-grey text-body-2 text-center pa-4">
              هنوز عضوی ثبت نشده است
            </v-list-item-title>
          </v-list-item>
        </v-list>

        <template #append>
          <v-btn
            to="/members"
            variant="text"
            size="small"
            color="primary"
            class="mt-2"
          >
            مشاهده همه اعضا
            <v-icon right size="small">mdi-arrow-right</v-icon>
          </v-btn>
        </template>
      </v-card>

      <!-- Quick actions -->
      <v-card class="flex-grow-1" min-width="300">
        <v-card-item>
          <v-avatar color="secondary" size="40">
            <v-icon>mdi-speedometer</v-icon>
          </v-avatar>
          <v-card-title>عملیات سریع</v-card-title>
          <v-card-subtitle>بازدید سریع از بخش‌های پرکاربرد</v-card-subtitle>
        </v-card-item>

        <v-divider></v-divider>

        <v-list density="compact" class="rounded-b-xl">
          <v-list-item
            v-for="action in quickActions"
            :key="action.to"
            :to="action.to"
            link
            class="pa-2"
          >
            <template #prepend>
              <v-avatar
                :color="action.color"
                size="32"
                class="white--text"
              >
                <v-icon size="16">{{ action.icon }}</v-icon>
              </v-avatar>
            </template>
            <v-list-item-title class="text-body-2">{{ action.title }}</v-list-item-title>
            <template #append>
              <v-icon size="18" color="grey">mdi-chevron-right</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-card>
    </div>

    <!-- Additional sections -->
    <div class="d-flex flex-wrap gap-4 mt-4">
      <!-- Today's schedule -->
      <v-card class="flex-grow-1" min-width="400" max-width="600">
        <v-card-item>
          <template #prepend>
            <v-avatar color="info" size="40">
              <v-icon>mdi-calendar-clock</v-icon>
            </v-avatar>
          </template>
          <v-card-title>برنامه امروز</v-card-title>
          <v-card-subtitle>کلاس‌های برگزارشده امروز</v-card-subtitle>
        </v-card-item>

        <v-divider></v-divider>

        <v-list density="compact" class="rounded-b-xl">
          <v-list-item
            v-for="schedule in todaySchedule"
            :key="schedule.id"
            class="pa-2"
          >
            <v-list-item-title class="text-body-2">
              <v-icon size="18" class="mr-2" color="primary">mdi-calendar</v-icon>
              {{ schedule.class_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-caption">
              {{ schedule.day_of_week }} | {{ schedule.start_time }} - {{ schedule.end_time }}
              <v-icon size="12" class="ml-1">mdi-domain</v-icon>
              {{ schedule.trainer_name }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item v-if="todaySchedule.length === 0">
            <v-list-item-title class="text-grey text-body-2 text-center pa-4">
              کلاسی برای امروز برنامه‌ریزی نشده
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>

      <!-- Financial summary -->
      <v-card class="flex-grow-1" min-width="300">
        <v-card-item>
          <template #prepend>
            <v-avatar color="warning" size="40">
              <v-icon>mdi-currency-irr</v-icon>
            </v-avatar>
          </template>
          <v-card-title>خلاصه مالی</v-card-title>
          <v-card-subtitle>تراکنش‌های مالی امروز</v-card-subtitle>
        </v-card-item>

        <v-divider></v-divider>

        <v-list density="compact" class="rounded-b-xl">
          <v-list-item class="pa-2">
            <v-list-item-title class="text-body-2">
              <v-icon size="18" class="mr-2" color="success">mdi-cash-multiple</v-icon>
              درآمد ماهانه
            </v-list-item-title>
            <v-list-item-subtitle class="text-h6 font-weight-bold text-success">
              {{ formatCurrency(paymentStats?.month_amount || 0) }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item class="pa-2">
            <v-list-item-title class="text-body-2">
              <v-icon size="18" class="mr-2" color="info">mdi-cash</v-icon>
              کل درآمدها
            </v-list-item-title>
            <v-list-item-subtitle class="text-h6 font-weight-bold text-info">
              {{ formatCurrency(paymentStats?.total_amount || 0) }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item class="pa-2">
            <v-list-item-title class="text-body-2">
              <v-icon size="18" class="mr-2" color="warning">mdi-alert-circle</v-icon>
              تسدید‌های در انتظار
            </v-list-item-title>
            <v-list-item-subtitle class="text-h6 font-weight-bold text-warning">
              {{ paymentStats?.pending_count || 0 }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item class="pa-2">
            <v-list-item-title class="text-body-2">
              <v-icon size="18" class="mr-2" color="error">mdi-bell-ring</v-icon>
              پس‌دهد‌های سررسیدگذشته
            </v-list-item-title>
            <v-list-item-subtitle class="text-h6 font-weight-bold text-error">
              {{ paymentStats?.overdue || 0 }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const currentUser = computed(() => {
  const user = localStorage.getItem('takavar_user')
  return user ? JSON.parse(user) : null
})

const currentDate = new Date().toLocaleDateString('fa-IR', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
})

const stats = ref([])
const recentMembers = ref([])
const todaySchedule = ref([])
const paymentStats = ref({})

const quickActions = [
  { to: '/members', icon: 'mdi-account-plus', title: 'ثبت عضو جدید', color: '#33D17A' },
  { to: '/payments', icon: 'mdi-credit-card', title: 'ثبت پرداخت', color: '#F5C211' },
  { to: '/attendance', icon: 'mdi-check-circle', title: 'ثبت حضور', color: '#15AABF' },
  { to: '/workouts', icon: 'mdi-dumbbell', title: 'ثبت تمرین', color: '#E95420' },
  { to: '/schedule', icon: 'mdi-calendar-plus', title: 'برنامه‌ریزی کلاس', color: '#9B59B6' },
  { to: '/equipment', icon: 'mdi-fitness-center', title: 'مدیریت تجهیزات', color: '#FF5733' },
]

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR', {
    style: 'currency',
    currency: 'IRT',
    maximumFractionDigits: 0,
  }).format(value)
}

async function loadData() {
  try {
    const [statsRes, membersRes, scheduleRes, paymentRes] = await Promise.all([
      axios.get('/api/dashboard/stats'),
      axios.get('/api/members?page=1&per_page=5'),
      axios.get('/api/schedule'),
      axios.get('/api/payments/summary'),
    ])

    stats.value = [
      { icon: 'mdi-account-group', title: 'تعداد اعضا', value: statsRes.data.total_members || 0, color: '#33D17A' },
      { icon: 'mdi-clipboard-text', title: 'عضویت‌های فعال', value: statsRes.data.active_subscriptions || 0, color: '#15AABF' },
      { icon: 'mdi-currency-irr', title: 'درآمد این ماه', value: formatCurrency(statsRes.data.revenue_this_month || 0), color: '#F5C211', highlight: true },
      { icon: 'mdi-account-cog', title: 'کارشناسان', value: statsRes.data.total_trainers || 0, color: '#9B59B6' },
      { icon: 'mdi-calendar-check', title: 'حضور امروز', value: statsRes.data.today_attendance || 0, color: '#33D17A' },
      { icon: 'mdi-fitness-center', title: 'تجهیزات', value: statsRes.data.equipment_count || 0, color: '#FF5733' },
    ]

    recentMembers.value = membersRes.data || []
    todaySchedule.value = scheduleRes.data || []
    paymentStats.value = paymentRes.data || {}
  } catch (err) {
    console.error('Error loading dashboard data:', err)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.stat-card {
  background: #3D1A5C;
  border: 1px solid #4A2866;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: #E95420;
  transform: translateY(-2px);
}

.stat-highlight {
  border-color: #E95420;
  box-shadow: 0 0 20px rgba(233, 84, 32, 0.2);
}
</style>

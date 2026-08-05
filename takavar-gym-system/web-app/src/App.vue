<template>
  <v-app>
    <!-- navigation drawer -->
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :expand-on-hover="expandOnHover"
      permanent
      color="surface-variant"
      class="px-2"
    >
      <!-- Header -->
      <v-list-item
        class="pa-4 mb-4"
        rounded="lg"
        color="primary"
      >
        <template #prepend>
          <v-avatar color="primary" size="40">
            <v-icon>mdi-dumbbell</v-icon>
          </v-avatar>
        </template>
        <v-list-item-title class="text-h6 font-weight-bold" style="color: #E95420;">
          تکاور
        </v-list-item-title>
        <v-list-item-subtitle class="text-caption">
          سیستم مدیریت باشگاه بدنسازی
        </v-list-item-subtitle>
      </v-list-item>

      <v-divider class="mb-2" color="#4A2866"></v-divider>

      <!-- Navigation items -->
      <v-list nav density="compact" class="px-1">
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :value="item.to"
          link
          color="grey-lighten-2"
          class="px-2 rounded-lg"
          :class="{ 'bg-primary': $route.path === item.to }"
          @click="drawer = false"
        >
          <template #append>
            <v-icon v-if="$route.path === item.to" color="white" size="18">
              mdi-check-circle
            </v-icon>
          </template>
        </v-list-item>
      </v-list>

      <v-spacer></v-spacer>

      <!-- User info at bottom -->
      <v-divider class="mb-2" color="#4A2866"></v-divider>
      <v-list-item class="pa-3" rounded="lg">
        <template #prepend>
          <v-avatar color="primary" size="36">
            <v-icon size="20">mdi-account</v-icon>
          </v-avatar>
        </template>
        <v-list-item-title class="text-body-2 font-weight-medium">
          {{ currentUser?.first_name || 'کاربر' }} {{ currentUser?.last_name || '' }}
        </v-list-item-title>
        <v-list-item-subtitle class="text-caption">
          {{ currentUser?.role || 'کاربر' }}
        </v-list-item-subtitle>
      </v-list-item>

      <v-list-item
        icon="mdi-logout"
        title="خروج از sistemi"
        value="logout"
        link
        class="mt-2"
        color="error"
        @click="logout"
      >
      </v-list-item>
    </v-navigation-drawer>

    <!-- App bar -->
    <v-app-bar color="surface-variant" density="comfortable" class="px-4">
      <template #prepend>
        <v-btn
          icon
          variant="text"
          @click="drawer = !drawer"
        >
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>

      <v-toolbar-title class="text-body-1 font-weight-medium" style="color: #E95420;">
        {{ pageTitle }}
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        icon
        variant="text"
        @click="showNotifications = !showNotifications"
      >
        <v-icon>mdi-bell-outline</v-icon>
        <v-badge
          v-if="notifications > 0"
          :content="notifications"
          color="error"
          offset-x="-8"
          offset-y="-8"
          dot
        >
        </v-badge>
      </v-btn>

      <v-menu>
        <template #activator="{ props }">
          <v-btn
            icon
            variant="text"
            v-bind="props"
          >
            <v-avatar
              color="primary"
              size="32"
            >
              <v-icon size="18">mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-card min-width="200">
          <v-card-text class="pt-0">
            <div class="text-body-2 font-weight-medium mb-1">
              {{ currentUser?.first_name }} {{ currentUser?.last_name }}
            </div>
            <div class="text-caption text-grey">
              {{ currentUser?.email || 'بدون ایمیل' }}
            </div>
            <v-divider class="my-2"></v-divider>
            <v-list nav density="compact">
              <v-list-item
                to="/settings"
                link
                prepend-icon="mdi-cog-outline"
                title="تنظیمات"
                @click="showNotifications = false"
              ></v-list-item>
              <v-list-item
                @click="logout"
                prepend-icon="mdi-logout"
                title="خروج"
                color="error"
              ></v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-menu>
    </v-app-bar>

    <!-- main content -->
    <v-main class="bg-background">
      <v-container fluid class="pa-6">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </v-container>
    </v-main>

    <!-- Notification dropdown -->
    <v-menu v-model="showNotifications" location="bottom end">
      <template #activator="{ props }">
        <v-btn icon variant="text" v-bind="props">
          <v-icon>mdi-bell-outline</v-icon>
        </v-btn>
      </template>
      <v-card min-width="350" max-width="400">
        <v-card-title class="d-flex align-center py-2">
          <v-icon start color="primary">mdi-bell-outline</v-icon>
          <span class="headline text-body-2 font-weight-bold">اطلاعیه‌ها</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-list subheader density="compact">
          <v-list-subheader>اخیرین اطلاعات</v-list-subheader>
          <v-list-item
            v-for="n in notificationsList"
            :key="n.id"
            :title="n.title"
            :subtitle="n.time"
            prepend-icon="mdi-message-text-outline"
          ></v-list-item>
          <v-list-item v-if="notificationsList.length === 0">
            <v-list-item-title class="text-grey text-body-2">
              اطلاعیه‌ای وجود ندارد
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const drawer = ref(false)
const miniVariant = ref(false)
const expandOnHover = ref(true)
const showNotifications = ref(false)
const notifications = ref(0)
const notificationsList = ref([])

const currentUser = computed(() => {
  const user = localStorage.getItem('takavar_user')
  return user ? JSON.parse(user) : null
})

const pageTitle = computed(() => {
  const titles = {
    '/': 'پنجره اصلی',
    '/members': 'مدیریت اعضا',
    '/subscriptions': 'مدیریت عضویت‌ها',
    '/payments': 'مدیریت پرداخت‌ها',
    '/attendance': 'ثبت حضور و غیبت',
    '/workouts': 'مدیریت تمرینات',
    '/schedule': 'زمان‌بندی کلاس‌ها',
    '/trainers': 'مدیریت کارشناسان',
    '/equipment': 'مدیریت تجهیزات',
    '/nutrition': 'برنامه‌های تغذیه‌ای',
    '/products': 'مدیریت فروشگاه',
    '/reports': 'گزارشات و تحلیل‌ها',
    '/settings': 'تنظیمات',
  }
  return titles[route.path] || 'پنجره اصلی'
})

const navItems = [
  { to: '/', icon: 'mdi-view-dashboard', title: 'پنجره اصلی' },
  { to: '/members', icon: 'mdi-account-group', title: 'اعضا' },
  { to: '/subscriptions', icon: 'mdi-clipboard-text', title: 'عضویت‌ها' },
  { to: '/payments', icon: 'mdi-currency-usd', title: 'پرداخت‌ها' },
  { to: '/attendance', icon: 'mdi-check-circle', title: 'حضور و غیبت' },
  { to: '/workouts', icon: 'mdi-dumbbell', title: 'تمرینات' },
  { to: '/schedule', icon: 'mdi-calendar-clock', title: 'زمان‌بندی' },
  { to: '/trainers', icon: 'mdi-account-cog', title: 'کارشناسان' },
  { to: '/equipment', icon: 'mdi-fitness-center', title: 'تجهیزات' },
  { to: '/nutrition', icon: 'mdi-food', title: 'تغذیه' },
  { to: '/products', icon: 'mdi-store', title: 'فروشگاه' },
  { to: '/reports', icon: 'mdi-chart-bar', title: 'گزارشات' },
  { to: '/settings', icon: 'mdi-cog-outline', title: 'تنظیمات' },
]

async function logout() {
  localStorage.removeItem('takavar_token')
  localStorage.removeItem('takavar_user')
  router.push('/login')
}

// Check auth on mount
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('takavar_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('takavar_token')
      localStorage.removeItem('takavar_user')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

// Load notifications
setInterval(async () => {
  // notification polling can be implemented here
}, 60000)
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* RTL support */
[dir="rtl"] .v-card {
  text-align: right;
}
</style>

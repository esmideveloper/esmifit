<template>
  <div class="schedule-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          ⏰ زمان‌بندی کلاس‌ها
        </h1>
        <p class="text-body-2 text-grey">نمایش برنامه هفتگی کلاس‌ها</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-calendar-plus" @click="showAddDialog = true">
        کلاس جدید
      </v-btn>
    </div>

    <!-- Day selector -->
    <div class="d-flex flex-wrap gap-2 mb-4">
      <v-chip
        v-for="day in days"
        :key="day.value"
        :color="selectedDay === day.value ? 'primary' : 'surface-variant'"
        :variant="selectedDay === day.value ? 'flat' : 'outlined'"
        rounded="lg"
        class="text-body-2"
        @click="selectDay(day.value)"
      >
        {{ day.label }}
      </v-chip>
    </div>

    <!-- Schedule grid -->
    <v-card color="surface-variant" class="mb-4">
      <v-card-text class="pa-0">
        <div class="d-flex" style="min-height: 500px;">
          <!-- Time column -->
          <div class="d-flex flex-column border-r border-[#4A2866]" style="width: 80px; background: #2C003E;">
            <div
              v-for="hour in hours"
              :key="hour"
              class="h-12 text-center text-caption text-grey border-b border-[#4A2866]"
              style="line-height: 48px;"
            >
              {{ hour }}:00
            </div>
          </div>

          <!-- Schedule columns -->
          <div class="flex-grow-1">
            <div class="d-flex">
              <div
                v-for="hour in hours"
                :key="hour"
                class="w-20 h-12 border-b border-r border-[#4A2866]"
                style="background: #2C003E;"
              >
              </div>
            </div>

            <!-- Class blocks -->
            <div
              v-for="(schedule, index) in daySchedules"
              :key="schedule.id"
              class="position-relative mb-2"
            >
              <v-card
                color="primary"
                variant="tonal"
                class="schedule-card"
                :style="getScheduleStyle(schedule)"
              >
                <v-card-text class="pa-2">
                  <div class="text-body-2 font-weight-medium">{{ schedule.class_name }}</div>
                  <div class="text-caption text-grey">
                    {{ schedule.category }} | {{ schedule.start_time }} - {{ schedule.end_time }}
                  </div>
                  <div class="text-caption mt-1">
                    <v-icon size="12" class="mr-1">mdi-account</v-icon>
                    {{ schedule.trainer_name || 'بدون کارشناس' }}
                    <v-icon size="12" class="ml-2 mr-1">mdi-home</v-icon>
                    {{ schedule.room_name || 'بدون سالن' }}
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Today's classes -->
    <h2 class="text-h6 font-weight-bold mb-3" style="color: #15AABF;">
      📋 کلاس‌های امروز
    </h2>
    <v-card color="surface-variant">
      <v-list density="compact" class="rounded-b-xl">
        <v-list-item
          v-for="cls in todayClasses"
          :key="cls.id"
          class="pa-3"
          :to="`/schedule/${cls.id}`"
        >
          <template #prepend>
            <v-avatar :color="getCategoryColor(cls.category)" size="40">
              <v-icon :color="white" size="20">{{ getCategoryIcon(cls.category) }}</v-icon>
            </v-avatar>
          </template>
          <v-list-item-title class="text-body-1 font-weight-medium">{{ cls.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-caption">
            {{ cls.category }} | {{ cls.duration_minutes }} دقیقه
          </v-list-item-subtitle>
          <template #append>
            <v-chip :color="getCategoryColor(cls.category)" size="small" variant="tonal">
              {{ cls.difficulty_level }}
            </v-chip>
          </template>
        </v-list-item>
        <v-list-item v-if="todayClasses.length === 0">
          <v-list-item-title class="text-grey text-body-2 text-center pa-4">
            کلاسی برای امروز برنامه‌ریزی نشده
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const scheduleList = ref([])
const showAddDialog = ref(false)
const selectedDay = ref('saturday')

const days = [
  { value: 'saturday', label: 'شنبه' },
  { value: 'sunday', label: ' 일요' },
  { value: 'monday', label: 'دوشنبه' },
  { value: 'tuesday', label: 'سه‌شنبه' },
  { value: 'wednesday', label: 'چهارشنبه' },
  { value: 'thursday', label: 'پنج‌شنبه' },
  { value: 'friday', label: 'جمعه' },
]

const hours = ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']

const daySchedules = computed(() => {
  const daySchedules = scheduleList.value.filter(s => s.day_of_week === selectedDay.value)
  return daySchedules.sort((a, b) => a.start_time.localeCompare(b.start_time))
})

const todayClasses = computed(() => {
  const today = new Date().toLocaleDateString('en-US', { weekday: 'lowercase' })
  const todaySchedules = scheduleList.value.filter(s => {
    const startTime = new Date(`2000-01-01T${s.start_time}`)
    const now = new Date()
    return s.day_of_week === today && startTime <= now
  })
  return todaySchedules.slice(0, 5)
})

function getScheduleStyle(schedule) {
  const [startHour, startMin] = schedule.start_time.split(':').map(Number)
  const [endHour, endMin] = schedule.end_time.split(':').map(Number)

  const top = ((startHour - 6) * 48) + ((startMin / 60) * 48) + 8
  const height = (((endHour - startHour) * 60) + (endMin - startMin)) / 60 * 48 - 4

  return {
    position: 'absolute',
    top: `${top}px`,
    left: '80px',
    right: '0',
    height: `${height}px`,
    zIndex: 1,
  }
}

function getCategoryColor(category) {
  const colors = {
    bodybuilding: '#E95420',
    cardio: '#15AABF',
    hiit: '#33D17A',
    crossfit: '#FF5733',
    yoga: '#9B59B6',
    pilates: '#F5C211',
    functional: '#2ECC71',
    personal_training: '#3498DB',
    group: '#95A5A6',
  }
  return colors[category] || '#E95420'
}

function getCategoryIcon(category) {
  const icons = {
    bodybuilding: 'mdi-dumbbell',
    cardio: 'mdi-run',
    hiit: 'mdi-flash',
    crossfit: 'mdi-crosshairs',
    yoga: 'mdi-yoga',
    pilates: 'mdi-human',
    functional: 'mdi-function',
    personal_training: 'mdi-account-cog',
    group: 'mdi-account-group',
  }
  return icons[category] || 'mdi-dumbbell'
}

function selectDay(day) {
  selectedDay.value = day
}

async function loadSchedule() {
  loading.value = true
  try {
    const response = await axios.get('/api/schedule')
    scheduleList.value = response.data || []
  } catch (err) {
    console.error('Error loading schedule:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSchedule()
})
</script>

<style scoped>
.schedule-card {
  border-radius: 8px;
  border: 1px solid #E95420;
}

.schedule-card:hover {
  box-shadow: 0 0 10px rgba(233, 84, 32, 0.3);
}
</style>

<template>
  <div class="workouts-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          🏋️ مدیریت تمرینات
        </h1>
        <p class="text-body-2 text-grey">برنامه‌ریزی و ثبت تمرینات اعضا</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-dumbbell-plus" @click="showAddDialog = true">
        ثبت تمرین
      </v-btn>
    </div>

    <!-- Filter row -->
    <v-card class="mb-4" color="surface-variant">
      <v-card-text class="pa-3">
        <v-row density="compact">
          <v-col cols="12" sm="3">
            <v-select
              v-model="memberFilter"
              :items="memberItems"
              label="عضو"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              item-title="name"
              item-value="id"
              @update:model-value="loadWorkouts"
            >
              <template #item="{ item, props }">
                <v-list-item v-bind="props">
                  <template #subtitle>{{ item.item.phone }}</template>
                </v-list-item>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              v-model="typeFilter"
              :items="typeItems"
              label="نوع تمرین"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadWorkouts"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-text-field
              v-model="dateFrom"
              label="از تاریخ"
              type="date"
              variant="outlined"
              density="compact"
              hide-details
              @update:model-value="loadWorkouts"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="2">
            <v-text-field
              v-model="dateTo"
              label="تا تاریخ"
              type="date"
              variant="outlined"
              density="compact"
              hide-details
              @update:model-value="loadWorkouts"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Workout cards -->
    <div class="d-flex flex-wrap gap-4">
      <v-card
        v-for="workout in workouts"
        :key="workout.id"
        color="surface-variant"
        class="workout-card"
        :to="`/members/${workout.member_id}`"
      >
        <v-card-item>
          <template #prepend>
            <v-avatar :color="getTypeColor(workout.workout_type)" size="48">
              <v-icon size="24">{{ getTypeIcon(workout.workout_type) }}</v-icon>
            </v-avatar>
          </template>
          <v-card-title class="text-body-1 font-weight-medium">
            {{ workout.member?.first_name }} {{ workout.member?.last_name }}
          </v-card-title>
          <v-card-subtitle class="text-caption">
            {{ formatDate(workout.workout_date) }}
          </v-card-subtitle>
        </v-card-item>

        <v-card-text>
          <div class="d-flex flex-wrap gap-2 mt-2">
            <v-chip :color="getTypeColor(workout.workout_type)" size="small" variant="tonal">
              {{ formatTypeName(workout.workout_type) }}
            </v-chip>
            <v-chip color="grey" size="small" variant="tonal">
              <v-icon size="14" class="mr-1">mdi-clock</v-icon>
              {{ workout.duration_minutes || '-' }} دقیقه
            </v-chip>
            <v-chip color="info" size="small" variant="tonal">
              <v-icon size="14" class="mr-1">mdi-fire</v-icon>
              {{ workout.calories_burned || '-' }} کیلو کیلوکالی
            </v-chip>
          </div>

          <v-expand-transition>
            <div v-if="showDetails[workout.id]" class="mt-3 pt-3 border-t border-[#4A2866]">
              <div v-if="workout.exercise_logs && workout.exercise_logs.length > 0">
                <div class="text-caption text-grey mb-2">تمرینات انجام شده:</div>
                <v-list density="compact" class="bg-transparent">
                  <v-list-item
                    v-for="ex in workout.exercise_logs"
                    :key="ex.id"
                    class="py-1"
                  >
                    <v-list-item-title class="text-body-2">
                      {{ ex.name || 'تمرین بدون نام' }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-caption">
                      {{ ex.sets }}×{{ ex.reps }} تکرار | وزن: {{ ex.weight ? ex.weight + ' kg' : '-' }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </div>
              <div v-if="workout.notes" class="mt-2 text-caption text-grey">
                <v-icon size="14" class="mr-1">mdi-note</v-icon>
                {{ workout.notes }}
              </div>
            </div>
          </v-expand-transition>

          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            class="mt-2"
            @click.stop="toggleDetails(workout.id)"
          >
            <v-icon size="18">{{ showDetails[workout.id] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-card-text>
      </v-card>

      <v-card v-if="workouts.length === 0" color="surface-variant" class="flex-grow-1 d-flex align-center justify-center">
        <div class="text-center">
          <v-icon size="48" color="grey" class="mb-2">mdi-dumbbell</v-icon>
          <p class="text-body-2 text-grey">هیچ تمرینی ثبت نشده</p>
        </div>
      </v-card>
    </div>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="showAddDialog" max-width="600">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40">
            <v-icon>mdi-dumbbell-plus</v-icon>
          </v-avatar>
          <v-card-title>ثبت تمرین جدید</v-card-title>
          <v-card-subtitle>فرم ثبت تمرین عضو</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-select
            v-model="form.member_id"
            :items="memberItems"
            item-title="name"
            item-value="id"
            label="انتخاب عضو"
            variant="outlined"
            density="comfortable"
            hide-details
            :loading="membersLoading"
          >
            <template #item="{ item, props }">
              <v-list-item v-bind="props">
                <template #subtitle>{{ item.item.phone }} | {{ formatPlanName(item.item.membership_type) }}</template>
              </v-list-item>
            </template>
          </v-select>

          <v-row>
            <v-col cols="12" sm="6">
              <v-select v-model="form.workout_type" :items="typeItems" label="نوع تمرین" variant="outlined" density="comfortable"></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.workout_date" label="تاریخ تمرین" type="date" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.duration_minutes" label="مدت (دقیقه)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.calories_burned" label="کیلوکالی سوزانده" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
          </v-row>

          <v-textarea v-model="form.notes" label="یادداشت" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" :disabled="!form.member_id" @click="saveWorkout">
            ثبت تمرین
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const membersLoading = ref(false)
const workouts = ref([])
const members = ref([])
const memberFilter = ref('')
const typeFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const showAddDialog = ref(false)
const saving = ref(false)
const showDetails = reactive({})

const form = ref({
  member_id: null,
  workout_type: 'strength',
  workout_date: new Date().toISOString().split('T')[0],
  duration_minutes: null,
  calories_burned: null,
  notes: '',
})

const memberItems = ref([])
const typeItems = [
  { title: 'توان ( strength )', value: 'strength' },
  { title: 'کارودی', value: 'cardio' },
  { title: 'HIIT', value: 'hiit' },
  { title: 'انعطاف‌پذیری', value: 'flexibility' },
  { title: 'سلامتی', value: 'recovery' },
  { title: 'ترکیبی', value: 'mixed' },
]

function getTypeColor(type) {
  const colors = { strength: '#E95420', cardio: '#15AABF', hiit: '#FF5733', flexibility: '#9B59B6', recovery: '#33D17A', mixed: '#F5C211' }
  return colors[type] || '#E95420'
}

function getTypeIcon(type) {
  const icons = { strength: 'mdi-dumbbell', cardio: 'mdi-run', hiit: 'mdi-flash', flexibility: 'mdi-yoga', recovery: 'mdi-heart-pulse', mixed: 'mdi-dumbbell-multiple' }
  return icons[type] || 'mdi-dumbbell'
}

function formatTypeName(type) {
  const names = { strength: 'توان', cardio: 'کارودی', hiit: 'HIIT', flexibility: 'انعطاف', recovery: 'سلامتی', mixed: 'ترکیبی' }
  return names[type] || type
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch {
    return dateStr
  }
}

function formatPlanName(plan) {
  const names = { bronze: 'برونزی', silver: 'نقره‌ای', gold: 'طلایی', vip: 'VIP ویژه', free_trial: 'آزمایشی' }
  return names[plan] || plan
}

function toggleDetails(id) {
  showDetails[id] = !showDetails[id]
}

async function loadWorkouts() {
  loading.value = true
  try {
    const params = {}
    if (memberFilter.value) params.member_id = memberFilter.value
    if (typeFilter.value) params.workout_type = typeFilter.value
    if (dateFrom.value) params.from_date = dateFrom.value
    if (dateTo.value) params.to_date = dateTo.value

    const response = await axios.get('/api/workout-logs', { params })
    workouts.value = response.data || []
  } catch (err) {
    console.error('Error loading workouts:', err)
  } finally {
    loading.value = false
  }
}

async function loadMembers() {
  membersLoading.value = true
  try {
    const response = await axios.get('/api/members?status=active')
    memberItems.value = (response.data || []).map(m => ({
      id: m.id,
      name: `${m.first_name} ${m.last_name}`,
      phone: m.phone,
      membership_type: m.membership_type,
    }))
  } catch (err) {
    console.error('Error loading members:', err)
  } finally {
    membersLoading.value = false
  }
}

async function saveWorkout() {
  if (!form.value.member_id) return

  saving.value = true
  try {
    await axios.post('/api/workout-logs', {
      member_id: form.value.member_id,
      workout_type: form.value.workout_type,
      workout_date: form.value.workout_date,
      duration_minutes: form.value.duration_minutes || null,
      calories_burned: form.value.calories_burned || null,
      notes: form.value.notes || null,
    })
    showAddDialog.value = false
    resetForm()
    loadWorkouts()
  } catch (err) {
    console.error('Error saving workout:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.value = {
    member_id: null,
    workout_type: 'strength',
    workout_date: new Date().toISOString().split('T')[0],
    duration_minutes: null,
    calories_burned: null,
    notes: '',
  }
}

onMounted(() => {
  loadWorkouts()
  loadMembers()
})
</script>

<style scoped>
.workout-card {
  width: 320px;
  transition: all 0.3s ease;
}

.workout-card:hover {
  border-color: #E95420;
  transform: translateY(-2px);
}
</style>

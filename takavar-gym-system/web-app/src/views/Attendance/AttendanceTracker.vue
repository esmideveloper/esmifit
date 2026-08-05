<template>
  <div class="attendance-page">
    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          📅 ثبت حضور و غیبت
        </h1>
        <p class="text-body-2 text-grey">ثبت ورود و خروج اعضا</p>
      </div>
      <v-btn
        color="primary"
        prepend-icon="mdi-clipboard-check"
        @click="showCheckInDialog = true"
      >
        ثبت ورود
      </v-btn>
    </div>

    <!-- Stats row -->
    <div class="d-flex flex-wrap gap-4 mb-4">
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="success" size="48">
            <v-icon>mdi-check-circle</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-success">{{ todayStats.present || 0 }}</div>
            <div class="text-caption text-grey">ورود امروز</div>
          </div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="grey" size="48">
            <v-icon>mdi-clock-outline</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-grey">{{ todayStats.checked_out || 0 }}</div>
            <div class="text-caption text-grey">خروج امروز</div>
          </div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="warning" size="48">
            <v-icon>mdi-alert-circle</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-warning">{{ todayStats.active || 0 }}</div>
            <div class="text-caption text-grey">در سالن</div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Search and filter -->
    <v-card class="mb-4" color="surface-variant">
      <v-card-text class="pa-3">
        <v-row density="compact">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              label="جستجو..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadAttendance"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select
              v-model="statusFilter"
              :items="statusItems"
              label="وضعیت"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadAttendance"
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
              @update:model-value="loadAttendance"
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
              @update:model-value="loadAttendance"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Attendance list -->
    <v-card color="surface-variant">
      <v-data-table
        :headers="headers"
        :items="attendanceList"
        :loading="loading"
        class="rounded-b-xl"
        no-data-text="هیچ رکوردی找到 نشده"
        @click:row="viewAttendance"
      >
        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="tonal"
          >
            {{ item.status }}
          </v-chip>
        </template>

        <template #item.check_in_time="{ item }">
          {{ formatDateTime(item.check_in_time) }}
        </template>

        <template #item.check_out_time="{ item }">
          <span v-if="item.check_out_time">{{ formatDateTime(item.check_out_time) }}</span>
          <span v-else class="text-grey">-</span>
        </template>

        <template #item.duration_minutes="{ item }">
          {{ item.duration_minutes ? `${item.duration_minutes} دقیقه` : '-' }}
        </template>

        <template #item.actions="{ item }">
          <v-btn
            v-if="item.status === 'checked_in'"
            icon
            variant="text"
            size="small"
            color="success"
            @click.stop="checkOut(item)"
          >
            <v-icon size="18">mdi-logout</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            @click.stop="viewAttendance(item)"
          >
            <v-icon size="18" color="primary">mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>

      <template #append>
        <div class="pa-4 text-center text-caption text-grey">
          کل {{ totalRecords }} رکورد
        </div>
      </template>
    </v-card>

    <!-- Check-in dialog -->
    <v-dialog v-model="showCheckInDialog" max-width="500">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="success" size="40">
            <v-icon>mdi-check-circle</v-icon>
          </v-avatar>
          <v-card-title>ثبت ورود عضو</v-card-title>
          <v-card-subtitle>انتخاب عضو Untuk ثبت ورود</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showCheckInDialog = false">
              بستن
            </v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>

        <v-card-text>
          <v-select
            v-model="checkInForm.member_id"
            :items="members"
            item-title="first_name"
            item-value="id"
            label="انتخاب عضو"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-account-search"
            hide-details
            :loading="membersLoading"
            @update:model-value="loadMemberDetails"
          >
            <template #item="{ item, props }">
              <v-list-item v-bind="props">
                <template #subtitle>
                  {{ item.item.phone || '' }} | {{ formatPlanName(item.item.membership_type) }}
                </template>
              </v-list-item>
            </template>
          </v-select>

          <v-alert
            v-if="selectedMember"
            type="info"
            variant="tonal"
            density="compact"
            class="mt-3"
          >
            <div class="d-flex align-center gap-2">
              <v-icon size="20" class="mr-2">mdi-account</v-icon>
              <span>
                <strong>{{ selectedMember.first_name }} {{ selectedMember.last_name }}</strong>
                <span class="text-grey text-caption ml-2">
                  پلن: {{ formatPlanName(selectedMember.membership_type) }}
                </span>
              </span>
            </div>
          </v-alert>

          <v-textarea
            v-model="checkInForm.notes"
            label="یادداشت (اختیاری)"
            variant="outlined"
            density="comfortable"
            rows="2"
            auto-grow
          ></v-textarea>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showCheckInDialog = false">
            انصراف
          </v-btn>
          <v-btn
            color="success"
            variant="flat"
            :loading="saving"
            :disabled="!checkInForm.member_id"
            @click="saveCheckIn"
          >
            ثبت ورود
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const membersLoading = ref(false)
const attendanceList = ref([])
const members = ref([])
const totalRecords = ref(0)
const search = ref('')
const statusFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')

const showCheckInDialog = ref(false)
const saving = ref(false)
const selectedMember = ref(null)

const checkInForm = ref({
  member_id: null,
  notes: '',
})

const todayStats = ref({
  present: 0,
  checked_out: 0,
  active: 0,
})

const headers = [
  { title: 'ID', key: 'id', width: '60px' },
  { title: 'عضو', key: 'member.full_name', sortable: true },
  { title: 'ورود', key: 'check_in_time', sortable: true },
  { title: 'خروج', key: 'check_out_time', sortable: true },
  { title: 'مدت', key: 'duration_minutes' },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'عملیات', key: 'actions', sortable: false, width: '120px' },
]

const statusItems = ['checked_in', 'checked_out', 'no_show']

function getStatusColor(status) {
  const colors = {
    checked_in: 'success',
    checked_out: 'info',
    no_show: 'error',
  }
  return colors[status] || 'grey'
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('fa-IR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateStr
  }
}

function formatPlanName(plan) {
  const names = {
    bronze: 'برونزی',
    silver: 'نقره‌ای',
    gold: 'طلایی',
    vip: 'VIP ویژه',
    free_trial: 'آزمایشی',
  }
  return names[plan] || plan
}

async function loadAttendance() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (dateFrom.value) params.from_date = dateFrom.value
    if (dateTo.value) params.to_date = dateTo.value

    const response = await axios.get('/api/attendance', { params })
    attendanceList.value = response.data || []
    totalRecords.value = attendanceList.value.length
  } catch (err) {
    console.error('Error loading attendance:', err)
  } finally {
    loading.value = false
  }
}

async function loadMembers() {
  membersLoading.value = true
  try {
    const response = await axios.get('/api/members?status=active')
    members.value = response.data || []
  } catch (err) {
    console.error('Error loading members:', err)
  } finally {
    membersLoading.value = false
  }
}

async function loadMemberDetails(memberId) {
  try {
    const response = await axios.get(`/api/members/${memberId}`)
    selectedMember.value = response.data
  } catch {
    selectedMember.value = null
  }
}

async function saveCheckIn() {
  if (!checkInForm.value.member_id) return

  saving.value = true
  try {
    await axios.post('/api/attendance', {
      member_id: checkInForm.value.member_id,
      notes: checkInForm.value.notes || null,
    })
    showCheckInDialog.value = false
    resetCheckInForm()
    loadAttendance()
    loadStats()
  } catch (err) {
    console.error('Error saving check-in:', err)
  } finally {
    saving.value = false
  }
}

async function checkOut(attendance) {
  try {
    await axios.post(`/api/attendance/${attendance.id}/check-out`)
    loadAttendance()
    loadStats()
  } catch (err) {
    console.error('Error checking out:', err)
  }
}

function viewAttendance(item) {
  // Could open detail dialog here
  console.log('View attendance:', item)
}

async function loadStats() {
  try {
    const today = new Date().toISOString().split('T')[0]
    const response = await axios.get('/api/attendance', {
      params: { from_date: today },
    })
    const list = response.data || []
    todayStats.value = {
      present: list.filter(a => a.status === 'checked_in').length,
      checked_out: list.filter(a => a.status === 'checked_out').length,
      active: list.filter(a => a.status === 'checked_in').length,
    }
  } catch (err) {
    console.error('Error loading stats:', err)
  }
}

function resetCheckInForm() {
  checkInForm.value = {
    member_id: null,
    notes: '',
  }
  selectedMember.value = null
}

onMounted(() => {
  loadAttendance()
  loadMembers()
  loadStats()
})
</script>

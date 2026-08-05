<template>
  <div class="trainers-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          👨‍🏫 مدیریت کارشناسان بدنسازی
        </h1>
        <p class="text-body-2 text-grey">مدیریت کارشناسان و مربیان باشگاه</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-account-plus" @click="showAddDialog = true">
        کارشناس جدید
      </v-btn>
    </div>

    <v-row>
      <v-col v-for="trainer in trainers" :key="trainer.id" cols="12" sm="6" md="4" lg="3">
        <v-card color="surface-variant" class="trainer-card h-100" @click="editTrainer(trainer)">
          <v-card-item class="pa-4">
            <div class="d-flex align-center gap-3">
              <v-avatar color="primary" size="56">
                <v-icon size="28">mdi-account-supervisor</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <div class="text-body-1 font-weight-medium">
                  {{ trainer.first_name }} {{ trainer.last_name }}
                </div>
                <div class="text-caption text-grey">
                  {{ trainer.specialization || 'پیشه نمایند不明' }}
                </div>
              </div>
            </div>
          </v-card-item>

          <v-card-text class="px-4 pb-4">
            <div class="d-flex flex-wrap gap-2">
              <v-chip :color="getStatusColor(trainer.status)" size="small" variant="tonal">
                {{ formatStatusName(trainer.status) }}
              </v-chip>
              <v-chip color="grey" size="small" variant="tonal">
                <v-icon size="14" class="mr-1">mdi-clock</v-icon>
                {{ trainer.years_experience || 0 }} سال تجربه
              </v-chip>
              <v-chip color="info" size="small" variant="tonal">
                <v-icon size="14" class="mr-1">mdi-currency-irr</v-icon>
                {{ formatCurrency(trainer.hourly_rate) }} / ساعت
              </v-chip>
            </div>

            <v-divider class="my-3"></v-divider>

            <div class="text-caption text-grey">
              <v-icon size="14" class="mr-1">mdi-phone</v-icon>
              {{ trainer.phone || 'بدون تلفن' }}
            </div>
            <div class="text-caption text-grey">
              <v-icon size="14" class="mr-1">mdi-email</v-icon>
              {{ trainer.email || 'بدون ایمیل' }}
            </div>

            <v-btn
              icon
              variant="text"
              size="small"
              color="primary"
              class="mt-2"
              @click.stop="editTrainer(trainer)"
            >
              <v-icon size="18">mdi-pencil</v-icon>
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-if="trainers.length === 0" cols="12">
        <v-card color="surface-variant" class="d-flex align-center justify-center pa-8">
          <div class="text-center">
            <v-icon size="48" color="grey" class="mb-2">mdi-account-supervisor</v-icon>
            <p class="text-body-2 text-grey">هیچ کارشناسی ثبت نشده</p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40"><v-icon>mdi-account-plus</v-icon></v-avatar>
          <v-card-title>{{ editingTrainer ? 'ویرایش کارشناس' : 'ثبت کارشناس جدید' }}</v-card-title>
          <v-card-subtitle>فرم اطلاعات کارشناس</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.first_name" label="نام" variant="outlined" density="comfortable" prepend-inner-icon="mdi-account"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.last_name" label="نام خانوادگی" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.national_id" label="کد ملی" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.phone" label="تلفن" variant="outlined" density="comfortable" prepend-inner-icon="mdi-phone"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" label="ایمیل" type="email" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.specialization" label="تخصص" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.certifications" label="گواهی‌نامه‌ها" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.years_experience" label="سابقه (سال)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.hourly_rate" label="نرخ ساعتی (تومان)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
          </v-row>
          <v-select v-model="form.status" :items="statusItems" label="وضعیت" variant="outlined" density="comfortable"></v-select>
          <v-textarea v-model="form.notes" label="یادداشت" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" @click="saveTrainer">
            {{ editingTrainer ? 'ذخیره تغییرات' : 'ثبت کارشناس' }}
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
const saving = ref(false)
const trainers = ref([])
const showAddDialog = ref(false)
const editingTrainer = ref(null)

const form = reactive({
  first_name: '',
  last_name: '',
  national_id: '',
  phone: '',
  email: '',
  specialization: '',
  certifications: '',
  years_experience: null,
  hourly_rate: null,
  status: 'active',
  notes: '',
})

const statusItems = [
  { title: 'فعال', value: 'active' },
  { title: 'غیرفعال', value: 'inactive' },
  { title: 'مرخصی', value: 'on_leave' },
]

function getStatusColor(status) {
  const colors = { active: 'green', inactive: 'grey', on_leave: 'warning' }
  return colors[status] || 'grey'
}

function formatStatusName(status) {
  const names = { active: 'فعال', inactive: 'غیرفعال', on_leave: 'مرخصی' }
  return names[status] || status
}

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR', { style: 'currency', currency: 'IRT', maximumFractionDigits: 0 }).format(value || 0)
}

async function loadTrainers() {
  loading.value = true
  try {
    const response = await axios.get('/api/trainers')
    trainers.value = response.data || []
  } catch (err) {
    console.error('Error loading trainers:', err)
  } finally {
    loading.value = false
  }
}

function editTrainer(trainer) {
  editingTrainer.value = trainer
  form.first_name = trainer.first_name || ''
  form.last_name = trainer.last_name || ''
  form.national_id = trainer.national_id || ''
  form.phone = trainer.phone || ''
  form.email = trainer.email || ''
  form.specialization = trainer.specialization || ''
  form.certifications = trainer.certifications || ''
  form.years_experience = trainer.years_experience || null
  form.hourly_rate = trainer.hourly_rate || null
  form.status = trainer.status || 'active'
  form.notes = trainer.notes || ''
  showAddDialog.value = true
}

async function saveTrainer() {
  saving.value = true
  try {
    const data = { ...form }
    if (editingTrainer.value) {
      await axios.put(`/api/trainers/${editingTrainer.value.id}`, data)
    } else {
      await axios.post('/api/trainers', data)
    }
    showAddDialog.value = false
    resetForm()
    loadTrainers()
  } catch (err) {
    console.error('Error saving trainer:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.first_name = ''
  form.last_name = ''
  form.national_id = ''
  form.phone = ''
  form.email = ''
  form.specialization = ''
  form.certifications = ''
  form.years_experience = null
  form.hourly_rate = null
  form.status = 'active'
  form.notes = ''
  editingTrainer.value = null
}

onMounted(() => {
  loadTrainers()
})
</script>

<style scoped>
.trainer-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.trainer-card:hover {
  border-color: #E95420;
  transform: translateY(-2px);
}
</style>

<template>
  <div class="members-page">
    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          👥 مدیریت اعضا
        </h1>
        <p class="text-body-2 text-grey">ثبت، ویرایش و مدیریت اطلاعات اعضا</p>
      </div>
      <v-btn
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="showAddDialog = true"
      >
        عضو جدید
      </v-btn>
    </div>

    <!-- Filters -->
    <v-card class="mb-4" color="surface-variant">
      <v-card-text class="pa-3">
        <v-row density="compact">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              label="جستجو در اعضا..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadMembers"
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
              @update:model-value="loadMembers"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select
              v-model="planFilter"
              :items="planItems"
              label="نوع پلن"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadMembers"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-btn
              variant="outlined"
              color="primary"
              block
              prepend-icon="mdi-refresh"
              @click="loadMembers"
            >
              Refreshing
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Members table -->
    <v-card color="surface-variant">
      <v-data-table
        :headers="headers"
        :items="members"
        :loading="loading"
        item-value="id"
        class="rounded-b-xl"
        no-data-text="هیچ عضوسی ثبت نشده است"
        @click:row="openMemberDetail"
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

        <template #item.membership_type="{ item }">
          <v-chip
            :color="getPlanColor(item.membership_type)"
            size="small"
            variant="tonal"
          >
            {{ formatPlanName(item.membership_type) }}
          </v-chip>
        </template>

        <template #item.gender="{ item }">
          <v-icon
            :icon="item.gender === 'male' ? 'mdi-account-male' : 'mdi-account-female'"
            size="20"
          ></v-icon>
        </template>

        <template #item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            @click.stop="editMember(item)"
          >
            <v-icon size="18" color="primary">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            @click.stop="deleteMember(item)"
          >
            <v-icon size="18" color="error">mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>

      <template #append>
        <div class="pa-4 text-center text-caption text-grey">
          کل {{ totalMembers }} عضو | صفحه {{ currentPage }} از {{ totalPages }}
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            @update:model-value="goToPage"
            class="ml-4"
            color="primary"
            density="compact"
          ></v-pagination>
        </div>
      </template>
    </v-card>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="showAddDialog" max-width="600" persistent>
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40">
            <v-icon>mdi-account-plus</v-icon>
          </v-avatar>
          <v-card-title>
            {{ editingMember ? 'ویرایش عضویت' : 'ثبت عضو جدید' }}
          </v-card-title>
          <v-card-subtitle>فرم اطلاعات عضو</v-card-subtitle>
          <template #append>
            <v-btn
              variant="text"
              @click="showAddDialog = false"
            >
              بستن
            </v-btn>
          </template>
        </v-card-item>

        <v-divider></v-divider>

        <v-card-text>
          <v-form ref="memberForm">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.first_name"
                  label="نام"
                  :rules="[v => !!v || 'لطفاً نام را وارد کنید']"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.last_name"
                  label="نام خانوادگی"
                  :rules="[v => !!v || 'لطفاً نام خانوادگی را وارد کنید']"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.national_id"
                  label="کد ملی"
                  prepend-inner-icon="mdi-card-account-details"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.phone"
                  label="شماره تلفن"
                  prepend-inner-icon="mdi-phone"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.email"
                  label="ایمیل"
                  type="email"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.birth_date"
                  label="تاریخ تولد"
                  type="date"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="form.gender"
                  :items="genderItems"
                  label="جنسیت"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="form.membership_type"
                  :items="planItemsForm"
                  label="نوع پلن عضویت"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.weight"
                  label="وزن (kg)"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.height"
                  label="قد (cm)"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-textarea
              v-model="form.address"
              label="آدرس"
              variant="outlined"
              density="comfortable"
              auto-grow
              rows="2"
            ></v-textarea>

            <v-textarea
              v-model="form.medical_conditions"
              label="شرایط پزشکی (اختیاری)"
              variant="outlined"
              density="comfortable"
              auto-grow
              rows="2"
            ></v-textarea>

            <v-select
              v-model="form.status"
              :items="statusItems"
              label="وضعیت عضویت"
              variant="outlined"
              density="comfortable"
              hide-details
            ></v-select>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showAddDialog = false"
          >
            انصراف
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="saving"
            @click="saveMember"
          >
            {{ editingMember ? 'ذخیره تغییرات' : 'ثبت عضو' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete confirmation -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card color="surface-variant">
        <v-card-text class="pa-6 text-center">
          <v-icon size="48" color="error" class="mb-3">
            mdi-alert-circle
          </v-icon>
          <p class="text-body-1 font-weight-medium mb-2">
            آیا مطمئن هستید؟
          </p>
          <p class="text-body-2 text-grey">
            این عمل باعث غیرفعال شدن عضویت {{ deleteMemberData?.first_name }} {{ deleteMemberData?.last_name }} خواهد شد.
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showDeleteDialog = false">
            انصراف
          </v-btn>
          <v-btn color="error" variant="flat" @click="confirmDelete">
            غیرفعال کردن
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const loading = ref(false)
const members = ref([])
const totalMembers = ref(0)
const currentPage = ref(1)
const totalPages = ref(1)
const search = ref('')
const statusFilter = ref('')
const planFilter = ref('')

const showAddDialog = ref(false)
const showDeleteDialog = ref(false)
const saving = ref(false)
const editingMember = ref(null)
const deleteMemberData = ref(null)

const form = ref({
  first_name: '',
  last_name: '',
  national_id: '',
  phone: '',
  email: '',
  birth_date: '',
  gender: '',
  membership_type: 'bronze',
  weight: null,
  height: null,
  address: '',
  medical_conditions: '',
  status: 'active',
})

const headers = [
  { title: 'ID', key: 'id', width: '60px', sortable: true },
  { title: 'نام', key: 'first_name', sortable: true },
  { title: 'نام خانوادگی', key: 'last_name', sortable: true },
  { title: 'تلفن', key: 'phone' },
  { title: 'ایمیل', key: 'email' },
  { title: 'جنسیت', key: 'gender' },
  { title: 'پلن', key: 'membership_type' },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'تاریخ شروع', key: 'membership_start' },
  { title: 'عملیات', key: 'actions', sortable: false, width: '120px' },
]

const statusItems = ['active', 'inactive', 'suspended', 'expired', 'cancelled']
const planItems = ['bronze', 'silver', 'gold', 'vip', 'free_trial']
const planItemsForm = [
  { title: 'برونزی', value: 'bronze' },
  { title: 'نقره‌ای', value: 'silver' },
  { title: 'طلایی', value: 'gold' },
  { title: 'VIP ویژه', value: 'vip' },
  { title: 'آزمایشی', value: 'free_trial' },
]
const genderItems = [
  { title: 'مذکر', value: 'male' },
  { title: 'مونث', value: 'female' },
  { title: 'سایر', value: 'other' },
]

function getStatusColor(status) {
  const colors = {
    active: 'green',
    inactive: 'grey',
    suspended: 'red',
    expired: 'error',
    cancelled: 'grey',
  }
  return colors[status] || 'grey'
}

function getPlanColor(plan) {
  const colors = {
    bronze: 'brown',
    silver: 'grey-lighten-1',
    gold: 'warning',
    vip: 'primary',
    free_trial: 'info',
  }
  return colors[plan] || 'grey'
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

async function loadMembers() {
  loading.value = true
  try {
    const params = { page: currentPage.value, per_page: 15 }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    if (planFilter.value) params.membership_type = planFilter.value

    const response = await axios.get('/api/members', { params })
    members.value = response.data || []

    const countResponse = await axios.get('/api/members', { params: { ...params, per_page: 1 } })
    totalMembers.value = countResponse.headers?.['x-total-count'] || members.value.length
    totalPages.value = Math.ceil(totalMembers.value / 15)
  } catch (err) {
    console.error('Error loading members:', err)
    members.value = []
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  currentPage.value = page
  loadMembers()
}

function openMemberDetail(item) {
  router.push(`/members/${item.id}`)
}

function editMember(member) {
  editingMember.value = member
  form.value = {
    first_name: member.first_name || '',
    last_name: member.last_name || '',
    national_id: member.national_id || '',
    phone: member.phone || '',
    email: member.email || '',
    birth_date: member.birth_date || '',
    gender: member.gender || '',
    membership_type: member.membership_type || 'bronze',
    weight: member.weight || null,
    height: member.height || null,
    address: member.address || '',
    medical_conditions: member.medical_conditions || '',
    status: member.status || 'active',
  }
  showAddDialog.value = true
}

function deleteMember(member) {
  deleteMemberData.value = member
  showDeleteDialog.value = true
}

async function confirmDelete() {
  try {
    await axios.delete(`/api/members/${deleteMemberData.value.id}`)
    showDeleteDialog.value = false
    loadMembers()
  } catch (err) {
    console.error('Error deleting member:', err)
  }
}

async function saveMember() {
  saving.value = true
  try {
    const apiData = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      national_id: form.value.national_id || null,
      phone: form.value.phone || null,
      email: form.value.email || null,
      birth_date: form.value.birth_date || null,
      gender: form.value.gender || null,
      membership_type: form.value.membership_type,
      weight: form.value.weight ? parseFloat(form.value.weight) : null,
      height: form.value.height ? parseFloat(form.value.height) : null,
      address: form.value.address || null,
      medical_conditions: form.value.medical_conditions || null,
      status: form.value.status,
    }

    if (editingMember.value) {
      await axios.put(`/api/members/${editingMember.value.id}`, apiData)
    } else {
      await axios.post('/api/members', apiData)
    }

    showAddDialog.value = false
    resetForm()
    loadMembers()
  } catch (err) {
    console.error('Error saving member:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.value = {
    first_name: '',
    last_name: '',
    national_id: '',
    phone: '',
    email: '',
    birth_date: '',
    gender: '',
    membership_type: 'bronze',
    weight: null,
    height: null,
    address: '',
    medical_conditions: '',
    status: 'active',
  }
  editingMember.value = null
}

onMounted(() => {
  loadMembers()
})
</script>

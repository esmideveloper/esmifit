<template>
  <div class="member-detail-page" v-if="member">
    <v-breadcrumbs :items="breadcrumbs" class="mb-4">
      <template #item="{ item, active }">
        <v-breadcrumbs-item :active="active" :to="item.to">
          {{ item.text }}
        </v-breadcrumbs-item>
      </template>
    </v-breadcrumbs>

    <v-card color="surface-variant" class="mb-4">
      <v-card-item>
        <v-avatar color="primary" size="80" class="ml-4">
          <v-icon size="40">{{ member.gender === 'male' ? 'mdi-account-male' : 'mdi-account-female' }}</v-icon>
        </v-avatar>
        <v-card-title class="text-h5 font-weight-bold">
          {{ member.first_name }} {{ member.last_name }}
        </v-card-title>
        <v-card-subtitle>
          <v-chip :color="getStatusColor(member.status)" variant="tonal" class="mr-2">
            {{ member.status }}
          </v-chip>
          <v-chip :color="getPlanColor(member.membership_type)" variant="tonal">
            {{ formatPlanName(member.membership_type) }}
          </v-chip>
        </v-card-subtitle>
        <template #append>
          <v-btn color="primary" variant="flat" prepend-icon="mdi-pencil" @click="editMember">ویرایش</v-btn>
          <v-btn variant="outlined" color="error" prepend-icon="mdi-delete" @click="deleteMember">حذف</v-btn>
          <v-btn variant="outlined" prepend-icon="mdi-qrcode" @click="showQrCode">QR کد</v-btn>
        </template>
      </v-card-item>
      <v-divider></v-divider>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-list-subheader>اطلاعاتBasic</v-list-subheader>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list-subheader>신체 정보</v-list-subheader>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list-subheader>تاریخ‌ها</v-list-subheader>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list-subheader>تماس</v-list-subheader>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-list dense class="bg-transparent">
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-card-account-details</v-icon></template>
                <v-list-item-title class="text-body-2">کد ملی:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.national_id || '-' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-human-male-female</v-icon></template>
                <v-list-item-title class="text-body-2">جنسیت:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ formatGender(member.gender) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-calendar</v-icon></template>
                <v-list-item-title class="text-body-2">تاریخ تولد:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ formatDate(member.birth_date) }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list dense class="bg-transparent">
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-weight</v-icon></template>
                <v-list-item-title class="text-body-2">وزن:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.weight || '-' }} kg</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-ruler</v-icon></template>
                <v-list-item-title class="text-body-2">قد:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.height || '-' }} cm</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-scale-bathroom</v-icon></template>
                <v-list-item-title class="text-body-2">BFH:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.body_fat_pct || '-' }}%</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list dense class="bg-transparent">
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-calendar-start</v-icon></template>
                <v-list-item-title class="text-body-2">شروع عضویت:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ formatDate(member.membership_start) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-calendar-check</v-icon></template>
                <v-list-item-title class="text-body-2">انقضای عضویت:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2" :style="{ color: isExpired ? '#FF5733' : '#33D17A' }">
                  {{ formatDate(member.membership_end) }}
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-history</v-icon></template>
                <v-list-item-title class="text-body-2">ثبت:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ formatDateTime(member.created_at) }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-list dense class="bg-transparent">
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-phone</v-icon></template>
                <v-list-item-title class="text-body-2">تلفن:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.phone || '-' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-email</v-icon></template>
                <v-list-item-title class="text-body-2">ایمیل:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.email || '-' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend><v-icon size="20" color="grey">mdi-map-marker</v-icon></template>
                <v-list-item-title class="text-body-2">آدرس:</v-list-item-title>
                <v-list-item-subtitle class="text-body-2">{{ member.address || '-' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>

        <v-alert v-if="member.medical_conditions" type="warning" variant="tonal" density="compact" class="mt-4">
          <div class="d-flex align-center gap-2">
            <v-icon size="20" class="mr-2">mdi-medical-bag</v-icon>
            <span>{{ member.medical_conditions }}</span>
          </div>
        </v-alert>

        <v-alert v-if="member.notes" type="info" variant="tonal" density="compact" class="mt-2">
          <div class="d-flex align-center gap-2">
            <v-icon size="20" class="mr-2">mdi-note</v-icon>
            <span>{{ member.notes }}</span>
          </div>
        </v-alert>
      </v-card-text>
    </v-card>

    <v-row>
      <v-col cols="12" md="6">
        <v-card color="surface-variant">
          <v-card-item>
            <v-avatar color="green" size="40"><v-icon>mdi-currency-usd</v-icon></v-avatar>
            <v-card-title>تراکنش‌های مالی</v-card-title>
          </v-card-item>
          <v-divider></v-divider>
          <v-data-table :headers="paymentHeaders" :items="payments" :loading="loading" class="rounded-b-xl" no-data-text="هیچ تراکنشی ثبت نشده">
            <template #item.status="{ item }">
              <v-chip :color="getPaymentStatusColor(item.status)" size="small" variant="tonal">{{ item.status }}</v-chip>
            </template>
            <template #item.amount="{ item }">
              <span class="font-weight-bold">{{ formatCurrency(item.amount) }}</span>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card color="surface-variant">
          <v-card-item>
            <v-avatar color="info" size="40"><v-icon>mdi-clipboard-text</v-icon></v-avatar>
            <v-card-title>تاریخچه عضویت</v-card-title>
          </v-card-item>
          <v-divider></v-divider>
          <v-data-table :headers="subscriptionHeaders" :items="subscriptions" :loading="loading" class="rounded-b-xl" no-data-text="هیچ عضvitی ثبت نشده">
            <template #item.payment_status="{ item }">
              <v-chip :color="getPlanStatusColor(item.payment_status)" size="small" variant="tonal">{{ item.payment_status }}</v-chip>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showQrDialog" max-width="300">
      <v-card color="surface-variant" class="pa-4 text-center">
        <v-img v-if="qrCodePath" :src="qrCodePath" height="200" contain></v-img>
        <div v-else class="text-grey text-body-2">QR code not available</div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showQrDialog = false">بستن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

  <v-card v-else color="surface-variant" class="d-flex align-center justify-center pa-8">
    <div class="text-center">
      <v-icon size="48" color="grey" class="mb-2">mdi-account-search</v-icon>
      <p class="text-body-2 text-grey">عضو یافت نشد</p>
    </div>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const member = ref(null)
const payments = ref([])
const subscriptions = ref([])
const showQrDialog = ref(false)
const qrCodePath = ref('')

const breadcrumbs = [
  { text: 'اعضا', to: '/members' },
  { text: 'جزییات عضو', to: null },
]

const paymentHeaders = [
  { title: 'تاریخ', key: 'payment_date' },
  { title: 'مبلغ', key: 'amount' },
  { title: 'شیوه پرداخت', key: 'payment_method' },
  { title: 'وضعیت', key: 'status' },
]

const subscriptionHeaders = [
  { title: 'پلن', key: 'plan.name' },
  { title: 'شروع', key: 'start_date' },
  { title: 'انقضا', key: 'end_date' },
  { title: 'وضعیت', key: 'payment_status' },
]

const isExpired = computed(() => {
  if (!member.value?.membership_end) return false
  return new Date(member.value.membership_end) < new Date()
})

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try { return new Date(dateStr).toLocaleDateString('fa-IR') } catch { return dateStr }
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  try { return new Date(dateStr).toLocaleString('fa-IR') } catch { return dateStr }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR', { style: 'currency', currency: 'IRT', maximumFractionDigits: 0 }).format(value || 0)
}

function formatPlanName(plan) {
  const names = { bronze: 'برونزی', silver: 'نقره‌ای', gold: 'طلایی', vip: 'VIP ویژه', free_trial: 'آزمایشی' }
  return names[plan] || plan
}

function formatGender(gender) {
  const names = { male: 'مذکر', female: 'مونث', other: 'سایر' }
  return names[gender] || gender
}

function getStatusColor(status) {
  const colors = { active: 'green', inactive: 'grey', suspended: 'red', expired: 'error', cancelled: 'grey' }
  return colors[status] || 'grey'
}

function getPlanColor(plan) {
  const colors = { bronze: 'brown', silver: 'grey-lighten-1', gold: 'warning', vip: 'primary', free_trial: 'info' }
  return colors[plan] || 'grey'
}

function getPaymentStatusColor(status) {
  const colors = { completed: 'green', pending: 'warning', failed: 'error', refunded: 'grey' }
  return colors[status] || 'grey'
}

function getPlanStatusColor(status) {
  const colors = { pending: 'warning', paid: 'green', partial: 'orange', overdue: 'red', cancelled: 'grey' }
  return colors[status] || 'grey'
}

async function loadMember() {
  loading.value = true
  try {
    const id = route.params.id
    const [memberRes, paymentsRes, subsRes] = await Promise.all([
      axios.get(`/api/members/${id}`),
      axios.get('/api/payments', { params: { member_id: id } }),
      axios.get('/api/subscriptions', { params: { member_id: id } }),
    ])
    member.value = memberRes.data
    payments.value = paymentsRes.data || []
    subscriptions.value = subsRes.data || []
  } catch (err) {
    console.error('Error loading member:', err)
  } finally {
    loading.value = false
  }
}

async function showQrCode() {
  try {
    const id = route.params.id
    const res = await axios.get(`/api/members/${id}/qr`)
    qrCodePath.value = res.data?.qr_code_path
    showQrDialog.value = true
  } catch (err) {
    console.error('Error loading QR code:', err)
  }
}

function editMember() {
  router.push(`/members/${member.value.id}`)
}

function deleteMember() {
  if (confirm(`آیا مطمئن هستید که می‌خواهید عضویت ${member.value?.first_name} ${member.value?.last_name} را غیرفعال کنید؟`)) {
    // In real app, call API to deactivate member
    member.value.status = 'inactive'
  }
}

onMounted(() => {
  loadMember()
})
</script>

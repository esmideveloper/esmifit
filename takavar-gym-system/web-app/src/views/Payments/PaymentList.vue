<template>
  <div class="payments-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          💰 مدیریت پرداخت‌ها
        </h1>
        <p class="text-body-2 text-grey">ثبت و مدیریت تراکنش‌های مالی</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-currency-usd" @click="showAddDialog = true">
        پرداخت جدید
      </v-btn>
    </div>

    <!-- Stats -->
    <div class="d-flex flex-wrap gap-4 mb-4">
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="success" size="48">
            <v-icon>mdi-cash-multiple</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-success">{{ formatCurrency(paymentStats.month_amount || 0) }}</div>
            <div class="text-caption text-grey">درآمد ماه</div>
          </div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="info" size="48">
            <v-icon>mdi-cash</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-info">{{ formatCurrency(paymentStats.total_amount || 0) }}</div>
            <div class="text-caption text-grey">کل درآمد</div>
          </div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="warning" size="48">
            <v-icon>mdi-timer-sand</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-warning">{{ paymentStats.pending_count || 0 }}</div>
            <div class="text-caption text-grey">در انتظار</div>
          </div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="200" flex-grow="1">
        <div class="d-flex align-center gap-3">
          <v-avatar color="error" size="48">
            <v-icon>mdi-bell-ring</v-icon>
          </v-avatar>
          <div>
            <div class="text-h4 font-weight-bold text-error">{{ paymentStats.overdue || 0 }}</div>
            <div class="text-caption text-grey">سررسیدگذشته</div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Filters -->
    <v-card class="mb-4" color="surface-variant">
      <v-card-text class="pa-3">
        <v-row density="compact">
          <v-col cols="12" sm="3">
            <v-select
              v-model="memberFilter"
              :items="memberItems"
              item-title="name"
              item-value="id"
              label="عضو"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadPayments"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              v-model="statusFilter"
              :items="statusItems"
              label="وضعیت"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadPayments"
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
              @update:model-value="loadPayments"
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
              @update:model-value="loadPayments"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Payments table -->
    <v-card color="surface-variant">
      <v-data-table
        :headers="headers"
        :items="payments"
        :loading="loading"
        class="rounded-b-xl"
        no-data-text="هیچ پرداختی ثبت نشده"
        @click:row="viewPayment"
      >
        <template #item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" variant="tonal">
            {{ item.status }}
          </v-chip>
        </template>

        <template #item.payment_date="{ item }">
          {{ formatDate(item.payment_date) }}
        </template>

        <template #item.amount="{ item }">
          <span class="font-weight-bold" :style="{ color: getStatusColor(item.status) }">
            {{ formatCurrency(item.amount) }}
          </span>
        </template>

        <template #item.member.name="{ item }">
          {{ item.member?.first_name }} {{ item.member?.last_name }}
        </template>

        <template #item.invoice_number="{ item }">
          {{ item.invoice_number || '-' }}
        </template>

        <template #item.actions="{ item }">
          <v-btn icon variant="text" size="small" @click.stop="generateReceipt(item)">
            <v-icon size="18" color="primary">mdi-receipt</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add Payment Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40"><v-icon>mdi-currency-usd</v-icon></v-avatar>
          <v-card-title>ثبت پرداخت جدید</v-card-title>
          <v-card-subtitle>فرم ثبت تراکنش مالی</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-select v-model="form.member_id" :items="memberItems" item-title="name" item-value="id" label="انتخاب عضو" variant="outlined" density="comfortable" hide-details :loading="membersLoading">
            <template #item="{ item, props }">
              <v-list-item v-bind="props">
                <template #subtitle>{{ item.item.phone }} | پلن: {{ formatPlanName(item.item.membership_type) }}</template>
              </v-list-item>
            </template>
          </v-select>

          <v-text-field v-model.number="form.amount" label="مبلغ (توマン)" type="number" variant="outlined" density="comfortable" prepend-inner-icon="mdi-currency-irr"></v-text-field>

          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.payment_date" label="تاریخ پرداخت" type="date" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select v-model="form.payment_method" :items="methodItems" label="شیوه پرداخت" variant="outlined" density="comfortable"></v-select>
            </v-col>
          </v-row>

          <v-text-field v-model="form.transaction_ref" label="شماره تراکنش (اختیاری)" variant="outlined" density="comfortable"></v-text-field>
          <v-text-field v-model="form.invoice_number" label="شماره فاکتور (اختیاری)" variant="outlined" density="comfortable"></v-text-field>
          <v-textarea v-model="form.notes" label="یادداشت" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" :disabled="!form.member_id" @click="savePayment">ثبت پرداخت</v-btn>
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
const payments = ref([])
const members = ref([])
const memberFilter = ref('')
const statusFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const showAddDialog = ref(false)
const saving = ref(false)
const paymentStats = ref({})

const form = ref({
  member_id: null,
  amount: null,
  payment_date: new Date().toISOString().split('T')[0],
  payment_method: 'cash',
  transaction_ref: '',
  invoice_number: '',
  notes: '',
})

const memberItems = ref([])
const headers = [
  { title: 'تاریخ', key: 'payment_date', sortable: true },
  { title: 'عضو', key: 'member', sortable: true, align: 'start' },
  { title: 'مبلغ', key: 'amount', sortable: true },
  { title: 'شیوه پرداخت', key: 'payment_method' },
  { title: 'شماره فاکتور', key: 'invoice_number' },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'عملیات', key: 'actions', sortable: false, width: '80px' },
]
const statusItems = ['completed', 'pending', 'failed', 'refunded']
const methodItems = [
  { title: 'نقدی', value: 'cash' },
  { title: 'کارت', value: 'card' },
  { title: 'انتقال بانکی', value: 'bank_transfer' },
  { title: 'آنلاین', value: 'online' },
  { title: 'てる分け', value: 'installment' },
]

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR', { style: 'currency', currency: 'IRT', maximumFractionDigits: 0 }).format(value || 0)
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try { return new Date(dateStr).toLocaleDateString('fa-IR') } catch { return dateStr }
}

function formatPlanName(plan) {
  const names = { bronze: 'برونزی', silver: 'نقره‌ای', gold: 'طلایی', vip: 'VIP ویژه', free_trial: 'آزمایشی' }
  return names[plan] || plan
}

function getStatusColor(status) {
  const colors = { completed: 'green', pending: 'warning', failed: 'error', refunded: 'grey' }
  return colors[status] || 'grey'
}

function viewPayment(item) {
  console.log('View payment:', item)
}

async function generateReceipt(item) {
  try {
    const response = await axios.get(`/api/payments/${item.id}/receipt`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `receipt_${item.id}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    console.error('Error generating receipt:', err)
  }
}

async function loadPayments() {
  loading.value = true
  try {
    const params = {}
    if (memberFilter.value) params.member_id = memberFilter.value
    if (statusFilter.value) params.status = statusFilter.value
    if (dateFrom.value) params.from_date = dateFrom.value
    if (dateTo.value) params.to_date = dateTo.value

    const response = await axios.get('/api/payments', { params })
    payments.value = response.data || []
  } catch (err) {
    console.error('Error loading payments:', err)
  } finally {
    loading.value = false
  }
}

async function loadPaymentStats() {
  try {
    const response = await axios.get('/api/payments/summary')
    paymentStats.value = response.data || {}
  } catch (err) {
    console.error('Error loading payment stats:', err)
  }
}

async function loadMembers() {
  membersLoading.value = true
  try {
    const response = await axios.get('/api/members?status=active')
    memberItems.value = (response.data || []).map(m => ({ id: m.id, name: `${m.first_name} ${m.last_name}`, phone: m.phone, membership_type: m.membership_type }))
  } catch (err) {
    console.error('Error loading members:', err)
  } finally {
    membersLoading.value = false
  }
}

async function savePayment() {
  if (!form.value.member_id) return

  saving.value = true
  try {
    await axios.post('/api/payments', {
      member_id: form.value.member_id,
      amount: form.value.amount,
      payment_date: form.value.payment_date,
      payment_method: form.value.payment_method,
      transaction_ref: form.value.transaction_ref || null,
      invoice_number: form.value.invoice_number || null,
      notes: form.value.notes || null,
    })
    showAddDialog.value = false
    resetForm()
    loadPayments()
    loadPaymentStats()
  } catch (err) {
    console.error('Error saving payment:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.value = { member_id: null, amount: null, payment_date: new Date().toISOString().split('T')[0], payment_method: 'cash', transaction_ref: '', invoice_number: '', notes: '' }
}

onMounted(() => {
  loadPayments()
  loadPaymentStats()
  loadMembers()
})
</script>

<template>
  <div class="reports-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          📊 گزارشات و تحلیل‌ها
        </h1>
        <p class="text-body-2 text-grey">گزارشات جامع کسب‌وکار باشگاه</p>
      </div>
    </div>

    <v-card class="mb-4" color="surface-variant">
      <v-card-text class="pa-4">
        <h2 class="text-h6 font-weight-bold mb-3" style="color: #15AABF;">انواع گزارشات</h2>
        <v-row>
          <v-col v-for="report in reportTypes" :key="report.id" cols="12" sm="6" md="4">
            <v-card color="primary" variant="tonal" class="report-type-card cursor-pointer" @click="selectedReport = report.id">
              <v-card-text class="pa-3 text-center">
                <v-icon size="32" class="mb-2">{{ report.icon }}</v-icon>
                <div class="text-body-2 font-weight-medium">{{ report.title }}</div>
                <div class="text-caption text-grey">{{ report.description }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card color="surface-variant">
      <v-card-item>
        <v-avatar :color="getReportColor(selectedReport)" size="40">
          <v-icon>{{ getReportIcon(selectedReport) }}</v-icon>
        </v-avatar>
        <v-card-title>{{ getReportTitle(selectedReport) }}</v-card-title>
        <v-card-subtitle>تاریخ تولید: {{ currentDate }}</v-card-subtitle>
        <template #append>
          <v-btn variant="outlined" color="primary" prepend-icon="mdi-printer" @click="printReport">چاپ</v-btn>
          <v-btn variant="outlined" color="success" prepend-icon="mdi-file-pdf-box" @click="exportPdf">PDF</v-btn>
          <v-btn variant="outlined" color="info" prepend-icon="mdi-file-excel" @click="exportExcel">Excel</v-btn>
        </template>
      </v-card-item>
      <v-divider></v-divider>
      <v-card-text>
        <div class="d-flex flex-wrap gap-4 mb-6">
          <v-card v-for="stat in summaryStats" :key="stat.label" class="pa-3" color="primary" variant="tonal" max-width="180" flex-grow="1">
            <div class="text-center">
              <div class="text-h4 font-weight-bold" :style="{ color: stat.color }">{{ stat.value }}</div>
              <div class="text-caption text-grey">{{ stat.label }}</div>
            </div>
          </v-card>
        </div>

        <v-data-table :headers="tableHeaders" :items="reportData" :loading="loading" class="rounded-b-xl" no-data-text="هیچ داده‌ای یافت نشد">
          <template #item.actions="{ item }">
            <v-btn icon variant="text" size="small" @click="viewDetail(item)">
              <v-icon size="18" color="primary">mdi-eye</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const selectedReport = ref('members')
const reportData = ref([])
const summaryStats = ref([])

const currentDate = new Date().toLocaleDateString('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' })

const reportTypes = [
  { id: 'members', title: 'گزارش اعضا', description: 'آمار و underperforming اعضا', icon: 'mdi-account-group', color: '#33D17A' },
  { id: 'payments', title: 'گزارش مالی', description: 'تراکنش‌های مالی و درآمدها', icon: 'mdi-currency-usd', color: '#F5C211' },
  { id: 'attendance', title: 'گزارش حضور', description: 'آمار حضور و غیبت اعضا', icon: 'mdi-check-circle', color: '#15AABF' },
  { id: 'workouts', title: 'گزارش تمرینات', description: 'آمار فعالیت‌های تمرینی', icon: 'mdi-dumbbell', color: '#E95420' },
  { id: 'equipment', title: 'گزارش تجهیزات', description: 'وضعیت و نگهداری تجهیزات', icon: 'mdi-fitness-center', color: '#9B59B6' },
  { id: 'subscriptions', title: 'گزارش عضویت‌ها', description: 'عضویت‌ها و تجدیدها', icon: 'mdi-clipboard-text', color: '#FF5733' },
]

const tableHeaders = [
  { title: 'نام', key: 'name' },
  { title: 'تعداد', key: 'count' },
  { title: 'درصد', key: 'percentage' },
  { title: 'مبلغ', key: 'amount' },
  { title: 'عملیات', key: 'actions', sortable: false, width: '80px' },
]

function getReportColor(id) {
  const report = reportTypes.find(r => r.id === id)
  return report ? report.color : '#E95420'
}

function getReportIcon(id) {
  const report = reportTypes.find(r => r.id === id)
  return report ? report.icon : 'mdi-chart-bar'
}

function getReportTitle(id) {
  const report = reportTypes.find(r => r.id === id)
  return report ? report.title : 'گزارش'
}

function viewDetail(item) {
  console.log('View detail:', item)
}

function printReport() {
  window.print()
}

function exportPdf() {
  alert('در حال تولید PDF... (قابلیت joints디아Uz)')
}

function exportExcel() {
  alert('در حال تولید Excel... (قابلیت joints디아Uz)')
}

async function loadReport() {
  loading.value = true
  try {
    if (selectedReport.value === 'members') {
      const res = await axios.get('/api/members')
      const members = res.data || []
      const total = members.length
      const active = members.filter(m => m.status === 'active').length
      summaryStats.value = [
        { label: 'کل اعضا', value: total, color: '#33D17A' },
        { label: 'اعضا فعال', value: active, color: '#33D17A' },
        { label: 'اعضا غیرفعال', value: total - active, color: '#FF5733' },
        { label: 'نرخ عضویت', value: total > 0 ? ((active / total) * 100).toFixed(1) + '%' : '0%', color: '#15AABF' },
      ]
      reportData.value = members.slice(0, 20).map(m => ({
        name: `${m.first_name} ${m.last_name}`,
        count: 1,
        percentage: total > 0 ? ((1 / total) * 100).toFixed(1) : 0,
        amount: 0,
        id: m.id,
      }))
    } else if (selectedReport.value === 'payments') {
      const res = await axios.get('/api/payments/summary')
      const stats = res.data || {}
      summaryStats.value = [
        { label: 'کل درآمد', value: (stats.total_amount || 0).toLocaleString('fa-IR'), color: '#F5C211' },
        { label: 'درآمد ماه', value: (stats.month_amount || 0).toLocaleString('fa-IR'), color: '#15AABF' },
        { label: 'پرداخت‌های انجام شده', value: stats.total_payments || 0, color: '#33D17A' },
        { label: 'در انتظار', value: stats.pending_count || 0, color: '#FF5733' },
      ]
      reportData.value = []
    } else {
      summaryStats.value = [
        { label: 'تعداد رکوردها', value: reportData.value.length, color: '#E95420' },
        { label: 'نام.report', value: getReportTitle(selectedReport.value), color: '#15AABF' },
      ]
    }
  } catch (err) {
    console.error('Error loading report:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadReport()
})

watch(() => selectedReport.value, () => {
  loadReport()
})
</script>

<style scoped>
.report-type-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.report-type-card:hover {
  background: rgba(233, 84, 32, 0.1);
  border-color: #E95420;
}
</style>

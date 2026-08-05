<template>
  <div class="equipment-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          🏗️ مدیریت تجهیزات
        </h1>
        <p class="text-body-2 text-grey">مدیریت تجهیزات باشگاه</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-fitness-center-plus" @click="showAddDialog = true">
        تجهیز جدید
      </v-btn>
    </div>

    <!-- Stats -->
    <div class="d-flex flex-wrap gap-4 mb-4">
      <v-card class="pa-4" color="surface-variant" max-width="180" flex-grow="1">
        <div class="text-center">
          <v-icon size="32" color="grey" class="mb-2">mdi-fitness-center</v-icon>
          <div class="text-h4 font-weight-bold text-grey">{{ stats.total || 0 }}</div>
          <div class="text-caption text-grey">کل تجهیزات</div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="180" flex-grow="1">
        <div class="text-center">
          <v-icon size="32" color="green" class="mb-2">mdi-check-circle</v-icon>
          <div class="text-h4 font-weight-bold text-green">{{ stats.available || 0 }}</div>
          <div class="text-caption text-grey">در دسترس</div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="180" flex-grow="1">
        <div class="text-center">
          <v-icon size="32" color="orange" class="mb-2">mdi-wrench</v-icon>
          <div class="text-h4 font-weight-bold text-orange">{{ stats.maintenance || 0 }}</div>
          <div class="text-caption text-grey">در تعمیر</div>
        </div>
      </v-card>
      <v-card class="pa-4" color="surface-variant" max-width="180" flex-grow="1">
        <div class="text-center">
          <v-icon size="32" color="red" class="mb-2">mdi-alert-circle</v-icon>
          <div class="text-h4 font-weight-bold text-red">{{ stats.damaged || 0 }}</div>
          <div class="text-caption text-grey">خارج از کار</div>
        </div>
      </v-card>
    </div>

    <!-- Filters -->
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
              @update:model-value="loadEquipment"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select
              v-model="categoryFilter"
              :items="categoryItems"
              label="دسته بندی"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="loadEquipment"
            ></v-select>
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
              @update:model-value="loadEquipment"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card color="surface-variant">
      <v-data-table
        :headers="headers"
        :items="equipmentList"
        :loading="loading"
        class="rounded-b-xl"
        no-data-text="هیچ تجهیزاتی ثبت نشده"
      >
        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="tonal"
          >
            {{ formatStatusName(item.status) }}
          </v-chip>
        </template>

        <template #item.category="{ item }">
          <v-chip
            :color="getCategoryColor(item.category)"
            size="small"
            variant="tonal"
          >
            {{ formatCategoryName(item.category) }}
          </v-chip>
        </template>

        <template #item.quantity="{ item }">
          <div class="d-flex align-center gap-2">
            <v-icon size="16" color="grey">mdi-cube-outline</v-icon>
            <span class="font-weight-medium">{{ item.quantity }}</span>
          </div>
        </template>

        <template #item.actions="{ item }">
          <v-btn icon variant="text" size="small" @click.stop="editEquipment(item)">
            <v-icon size="18" color="primary">mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon variant="text" size="small" @click.stop="toggleStatus(item)">
            <v-icon
              size="18"
              :color="item.status === 'available' ? 'success' : 'warning'"
            >
              {{ item.status === 'available' ? 'mdi-archive' : 'mdi-archive-alert' }}
            </v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="showAddDialog" max-width="600">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40">
            <v-icon>mdi-fitness-center-plus</v-icon>
          </v-avatar>
          <v-card-title>{{ editingItem ? 'ویرایش تجهیز' : 'ثبت تجهیز جدید' }}</v-card-title>
          <v-card-subtitle>فرم اطلاعات تجهیز</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" label="نام تجهیز" variant="outlined" density="comfortable" prepend-inner-icon="mdi-fitness-center"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select v-model="form.category" :items="categoryFormItems" label="دسته بندی" variant="outlined" density="comfortable"></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select v-model="form.status" :items="statusFormItems" label="وضعیت" variant="outlined" density="comfortable"></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.brand" label="برند" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.model" label="مدل" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.serial_number" label="شماره سریال" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.location" label="موقعیت" variant="outlined" density="comfortable" prepend-inner-icon="mdi-map-marker"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.quantity" label="تعداد" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.purchase_date" label="تاریخ خرید" type="date" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.purchase_price" label="قیمت خرید" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
          </v-row>
          <v-textarea v-model="form.notes" label="یادداشت" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" @click="saveEquipment">
            {{ editingItem ? 'ذخیره تغییرات' : 'ثبت تجهیز' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const saving = ref(false)
const equipmentList = ref([])
const search = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const showAddDialog = ref(false)
const editingItem = ref(null)

const form = ref({
  name: '',
  category: 'cardio',
  status: 'available',
  brand: '',
  model: '',
  serial_number: '',
  location: '',
  quantity: 1,
  purchase_date: '',
  purchase_price: null,
  notes: '',
})

const headers = [
  { title: 'نام', key: 'name', sortable: true },
  { title: 'دسته بندی', key: 'category' },
  { title: 'برند', key: 'brand' },
  { title: 'موقعیت', key: 'location' },
  { title: 'تعداد', key: 'quantity' },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'عملیات', key: 'actions', sortable: false, width: '120px' },
]

const categoryItems = ['cardio', 'strength', 'free_weights', 'machines', 'accessories', 'safety']
const categoryFormItems = [
  { title: 'کارودی', value: 'cardio' },
  { title: 'توان', value: 'strength' },
  { title: 'وزنه‌های آزاد', value: 'free_weights' },
  { title: 'ماشین‌ها', value: 'machines' },
  { title: 'لوازم جانبی', value: 'accessories' },
  { title: 'ایمنی', value: 'safety' },
]
const statusItems = ['available', 'in_use', 'maintenance', 'damaged', 'out_of_order']
const statusFormItems = [
  { title: 'در دسترس', value: 'available' },
  { title: 'در استفاده', value: 'in_use' },
  { title: 'در تعمیر', value: 'maintenance' },
  { title: 'خ손', value: 'damaged' },
  { title: 'خارج از کار', value: 'out_of_order' },
]

const stats = ref({ total: 0, available: 0, maintenance: 0, damaged: 0 })

function getStatusColor(status) {
  const colors = { available: 'green', in_use: 'info', maintenance: 'orange', damaged: 'error', out_of_order: 'error' }
  return colors[status] || 'grey'
}

function getCategoryColor(category) {
  const colors = { cardio: 'blue', strength: 'green', free_weights: 'brown', machines: 'purple', accessories: 'grey', safety: 'red' }
  return colors[category] || 'grey'
}

function formatStatusName(status) {
  const names = { available: 'در دسترس', in_use: 'در استفاده', maintenance: 'در تعمیر', damaged: 'خ손', out_of_order: 'خارج از کار' }
  return names[status] || status
}

function formatCategoryName(category) {
  const names = { cardio: 'کارودی', strength: 'توان', free_weights: 'وزنه آزاد', machines: 'ماشین‌ها', accessories: 'لوازم جانبی', safety: 'ایمنی' }
  return names[category] || category
}

async function loadEquipment() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (categoryFilter.value) params.category = categoryFilter.value
    if (statusFilter.value) params.status = statusFilter.value

    const response = await axios.get('/api/equipment', { params })
    equipmentList.value = response.data || []

    // Calculate stats
    const all = await axios.get('/api/equipment')
    const list = all.data || []
    stats.value = {
      total: list.length,
      available: list.filter(e => e.status === 'available').length,
      maintenance: list.filter(e => e.status === 'maintenance').length,
      damaged: list.filter(e => e.status === 'damaged' || e.status === 'out_of_order').length,
    }
  } catch (err) {
    console.error('Error loading equipment:', err)
  } finally {
    loading.value = false
  }
}

function editEquipment(item) {
  editingItem.value = item
  form.value = {
    name: item.name || '',
    category: item.category || 'cardio',
    status: item.status || 'available',
    brand: item.brand || '',
    model: item.model || '',
    serial_number: item.serial_number || '',
    location: item.location || '',
    quantity: item.quantity || 1,
    purchase_date: item.purchase_date || '',
    purchase_price: item.purchase_price || null,
    notes: item.notes || '',
  }
  showAddDialog.value = true
}

async function saveEquipment() {
  saving.value = true
  try {
    const data = { ...form.value }
    if (editingItem.value) {
      await axios.put(`/api/equipment/${editingItem.value.id}`, data)
    } else {
      await axios.post('/api/equipment', data)
    }
    showAddDialog.value = false
    editingItem.value = null
    resetForm()
    loadEquipment()
  } catch (err) {
    console.error('Error saving equipment:', err)
  } finally {
    saving.value = false
  }
}

async function toggleStatus(item) {
  try {
    const newStatus = item.status === 'available' ? 'in_use' : 'available'
    await axios.put(`/api/equipment/${item.id}`, { status: newStatus })
    loadEquipment()
  } catch (err) {
    console.error('Error toggling status:', err)
  }
}

function resetForm() {
  form.value = {
    name: '',
    category: 'cardio',
    status: 'available',
    brand: '',
    model: '',
    serial_number: '',
    location: '',
    quantity: 1,
    purchase_date: '',
    purchase_price: null,
    notes: '',
  }
}

onMounted(() => {
  loadEquipment()
})
</script>

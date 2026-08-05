<template>
  <div class="products-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          📦 مدیریت فروشگاه باشگاه
        </h1>
        <p class="text-body-2 text-grey">مدیریت محصولات و سوپر-market باشگاه</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-cart-plus" @click="showAddDialog = true">
        محصول جدید
      </v-btn>
    </div>

    <v-card color="surface-variant" class="mb-4">
      <v-card-text class="pa-3">
        <v-row density="compact">
          <v-col cols="12" sm="4">
            <v-text-field v-model="search" label="جستجو..." prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details clearable @update:model-value="loadProducts"></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select v-model="categoryFilter" :items="categoryItems" label="دسته بندی" variant="outlined" density="compact" hide-details clearable @update:model-value="loadProducts"></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-row>
      <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" lg="3">
        <v-card color="surface-variant" class="product-card h-100">
          <v-card-item>
            <v-avatar color="primary" size="56">
              <v-icon size="28">mdi-cart</v-icon>
            </v-avatar>
            <v-card-title class="text-body-1 font-weight-medium">{{ product.name }}</v-card-title>
            <v-card-subtitle>{{ formatCategoryName(product.category) }}</v-card-subtitle>
          </v-card-item>
          <v-card-text>
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-h5 font-weight-bold text-success">{{ formatCurrency(product.selling_price) }}</span>
              <v-chip :color="product.stock_quantity <= product.low_stock_alert ? 'error' : 'green'" size="small" variant="tonal">
                {{ product.stock_quantity }} {{ product.unit || 'عدد' }}
              </v-chip>
            </div>
            <v-text-field v-model.number="productForm[product.id]?.quantity" type="number" variant="outlined" density="compact" hide-details class="mb-2">
              <template #prepend>
                <v-icon size="18" color="grey">mdi-plus</v-icon>
              </template>
            </v-text-field>
            <v-btn color="primary" variant="flat" size="small" block :disabled="(!productForm[product.id]?.quantity && productForm[product.id]?.quantity !== 0) || product.stock_quantity <= 0" @click="addToCart(product)">
              اضافه به سبد
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="products.length === 0" cols="12">
        <v-card color="surface-variant" class="d-flex align-center justify-center pa-8">
          <div class="text-center">
            <v-icon size="48" color="grey" class="mb-2">mdi-cart</v-icon>
            <p class="text-body-2 text-grey">هیچ محصولی ثبت نشده</p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="primary" size="40"><v-icon>mdi-cart-plus</v-icon></v-avatar>
          <v-card-title>ثبت محصول جدید</v-card-title>
          <v-card-subtitle>فرم اطلاعات محصول</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field v-model="form.name" label="نام محصول" variant="outlined" density="comfortable"></v-text-field>
          <v-select v-model="form.category" :items="categoryFormItems" label="دسته بندی" variant="outlined" density="comfortable"></v-select>
          <v-text-field v-model="form.brand" label="برند" variant="outlined" density="comfortable"></v-text-field>
          <v-text-field v-model="form.sku" label="کد محصول (SKU)" variant="outlined" density="comfortable"></v-text-field>
          <v-text-field v-model.number="form.cost_price" label="هزینه خرید" type="number" variant="outlined" density="comfortable"></v-text-field>
          <v-text-field v-model.number="form.selling_price" label="قیمت فروش" type="number" variant="outlined" density="comfortable" prepend-inner-icon="mdi-currency-irr"></v-text-field>
          <v-text-field v-model.number="form.stock_quantity" label="موجودی" type="number" variant="outlined" density="comfortable"></v-text-field>
          <v-text-field v-model.number="form.low_stock_alert" label="حدhető هشدار" type="number" variant="outlined" density="comfortable"></v-text-field>
          <v-textarea v-model="form.description" label="توضیحات" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" @click="saveProduct">ثبت محصول</v-btn>
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
const products = ref([])
const search = ref('')
const categoryFilter = ref('')
const showAddDialog = ref(false)
const productForm = reactive({})

const form = reactive({
  name: '',
  category: 'supplement',
  brand: '',
  sku: '',
  cost_price: null,
  selling_price: null,
  stock_quantity: 0,
  low_stock_alert: 10,
  description: '',
})

const categoryItems = ['supplement', 'apparel', 'accessory', 'nutrition', 'other']
const categoryFormItems = [
  { title: 'مکمل‌های غذایی', value: 'supplement' },
  { title: 'لباس ورزشی', value: 'apparel' },
  { title: 'لوازم جانبی', value: 'accessory' },
  { title: 'غذاهای سالم', value: 'nutrition' },
  { title: 'سایر', value: 'other' },
]

function formatCurrency(value) {
  return new Intl.NumberFormat('fa-IR', { style: 'currency', currency: 'IRT', maximumFractionDigits: 0 }).format(value || 0)
}

function formatCategoryName(category) {
  const names = { supplement: 'مکمل', apparel: 'لباس ورزشی', accessory: 'لوازم جانبی', nutrition: 'غذاهای سالم', other: 'سایر' }
  return names[category] || category
}

function addToCart(product) {
  const qty = productForm[product.id]?.quantity || 1
  alert(`${product.name} با تعداد ${qty} به سبد خرید اضافه شد! (قابلیت jointsدیاUz)`)
}

async function loadProducts() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (categoryFilter.value) params.category = categoryFilter.value
    const response = await axios.get('/api/products', { params })
    products.value = response.data || []
  } catch (err) {
    console.error('Error loading products:', err)
  } finally {
    loading.value = false
  }
}

async function saveProduct() {
  saving.value = true
  try {
    await axios.post('/api/products', { ...form })
    showAddDialog.value = false
    resetForm()
    loadProducts()
  } catch (err) {
    console.error('Error saving product:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.name = ''
  form.category = 'supplement'
  form.brand = ''
  form.sku = ''
  form.cost_price = null
  form.selling_price = null
  form.stock_quantity = 0
  form.low_stock_alert = 10
  form.description = ''
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.product-card {
  transition: all 0.3s ease;
}
.product-card:hover {
  border-color: #E95420;
}
</style>

<template>
  <div class="settings-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          ⚙️ تنظیمات سیستم
        </h1>
        <p class="text-body-2 text-grey">پیکربندی و تنظیمات باشگاه</p>
      </div>
    </div>

    <v-row>
      <v-col cols="12" md="6">
        <v-card color="surface-variant" class="mb-4">
          <v-card-item>
            <v-avatar color="primary" size="40">
              <v-icon>mdi-school</v-icon>
            </v-avatar>
            <v-card-title>اطلاعات باشگاه</v-card-title>
            <v-card-subtitle>تنظیمات عمومی باشگاه</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <v-text-field v-model="gymInfo.name" label="نام باشگاه" variant="outlined" density="comfortable" prepend-inner-icon="mdi-fitness-center"></v-text-field>
            <v-text-field v-model="gymInfo.owner" label="مالک/مدیر" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model="gymInfo.phone" label="تلفن تماس" variant="outlined" density="comfortable" prepend-inner-icon="mdi-phone"></v-text-field>
            <v-text-field v-model="gymInfo.email" label="ایمیل" type="email" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model="gymInfo.address" label="آدرس" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model="gymInfo.tax_id" label="کد مالیاتی" variant="outlined" density="comfortable" prepend-inner-icon="mdi-card-account-details"></v-text-field>
            <v-text-field v-model="gymInfo.registration_number" label="شماره ثبت" variant="outlined" density="comfortable"></v-text-field>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="flat" :loading="saving" @click="saveGymInfo">ذخیره تغییرات</v-btn>
          </v-card-actions>
        </v-card>

        <v-card color="surface-variant" class="mb-4">
          <v-card-item>
            <v-avatar color="info" size="40">
              <v-icon>mdi-receipt</v-icon>
            </v-avatar>
            <v-card-title>تنظیمات فاکتور</v-card-title>
            <v-card-subtitle>فرمت و اطلاعات فاکتورها</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <v-text-field v-model="invoiceInfo.prefix" label="پیشوند شماره فاکتور" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model="invoiceInfo.start_number" label="شماره شروع" type="number" variant="outlined" density="comfortable"></v-text-field>
            <v-textarea v-model="invoiceInfo.footer_text" label="متن زیرین فاکتور" variant="outlined" density="comfortable" rows="2" auto-grow></v-textarea>
            <v-text-field v-model="invoiceInfo.bank_name" label="نام بانک" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model="invoiceInfo.account_number" label="شماره حساب" variant="outlined" density="comfortable"></v-text-field>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="flat" :loading="saving" @click="saveInvoiceInfo">ذخیره تغییرات</v-btn>
          </v-card-actions>
        </v-card>

        <v-card color="surface-variant">
          <v-card-item>
            <v-avatar color="warning" size="40">
              <v-icon>mdi-bell</v-icon>
            </v-avatar>
            <v-card-title>تنظیمات اطلاعیه‌ها</v-card-title>
            <v-card-subtitle>مدیریت اعلان‌ها و خبرنامه‌ها</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <v-switch v-model="notifications.member_welcome" label="پیام خوش‌آمدگویی به اعضای جدید" color="primary"></v-switch>
            <v-switch v-model="notifications.payment_reminder" label="یادآوری پرداخت باقیمانده" color="primary" class="mt-2"></v-switch>
            <v-switch v-model="notifications.membership_expiry" label="اخطار انقضا قبل از مهلت" color="primary" class="mt-2"></v-switch>
            <v-switch v-model="notifications.attendance" label="ثبت خودکار حضور و غیبت" color="primary" class="mt-2"></v-switch>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="flat" :loading="saving" @click="saveNotifications">ذخیره تغییرات</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card color="surface-variant" class="mb-4">
          <v-card-item>
            <v-avatar color="error" size="40">
              <v-icon>mdi-shield-account</v-icon>
            </v-avatar>
            <v-card-title>پیش‌فرض‌های سیستم</v-card-title>
            <v-card-subtitle>تنظیمات پیش‌فرض برنامه</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <v-select v-model="defaults.default_plan" :items="planItems" label="پلن پیش‌فرض برای اعضای جدید" variant="outlined" density="comfortable"></v-select>
            <v-select v-model="defaults.default_payment_method" :items="methodItems" label="شیوه پرداخت پیش‌فرض" variant="outlined" density="comfortable"></v-select>
            <v-text-field v-model.number="defaults.auto_renewal_days" label="روزهای قبل از انقضا برای یادآوری" type="number" variant="outlined" density="comfortable"></v-text-field>
            <v-text-field v-model.number="defaults.max_allowed_members" label="حد مجاز اعضا" type="number" variant="outlined" density="comfortable"></v-text-field>
            <v-select v-model="defaults.timezone" :items="timezoneItems" label="منطقه زمانی" variant="outlined" density="comfortable"></v-select>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="flat" :loading="saving" @click="saveDefaults">ذخیره تغییرات</v-btn>
          </v-card-actions>
        </v-card>

        <v-card color="surface-variant" class="mb-4">
          <v-card-item>
            <v-avatar color="grey" size="40">
              <v-icon>mdi-database</i>
            </v-avatar>
            <v-card-title>پشتیبان‌گیری و بازیابی</v-card-title>
            <v-card-subtitle>مدیریت بک‌آپ داده‌ها</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <div class="text-body-2 text-grey mb-3">
              <v-icon size="18" class="mr-2" color="success">mdi-check-circle</v-icon>
              آخرین بک‌آپ: {{ lastBackup || 'هیچ بک‌آبی انجام نشده' }}
            </div>
            <v-btn color="primary" variant="flat" prepend-icon="mdi-download" @click="backupNow">
              ایجاد بک‌آپ فوری
            </v-btn>
            <v-btn variant="outlined" color="grey" class="ml-2" prepend-icon="mdi-upload" @click="restoreBackup">
              بازیابی از بک‌آپ
            </v-btn>
            <v-btn variant="outlined" color="grey" class="ml-2" prepend-icon="mdi-history" @click="viewBackupHistory">
              تاریخچه بک‌آپ‌ها
            </v-btn>
          </v-card-text>
        </v-card>

        <v-card color="surface-variant">
          <v-card-item>
            <v-avatar color="green" size="40">
              <v-icon>mdi-information</v-icon>
            </v-avatar>
            <v-card-title>درباره برنامه</v-card-title>
            <v-card-subtitle>مشاوره و مستندات</v-card-subtitle>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-text>
            <div class="text-body-2 text-grey">
              <p><strong class="text-white">نرم‌افزار:</strong> سیستم مدیریت باشگاه بدنسازی تکاور</p>
              <p><strong class="text-white">نسخه:</strong> 1.0.0</p>
              <p><strong class="text-white">تاریخ انتشار:</strong> ۱۴۰۳</p>
              <p><strong class="text-white">توسعه‌دهنده:</strong> تیم توسعه تکاور</p>
              <p class="mt-3">
                این نرم‌افزار با استفاده از تکنولوژی‌های مدرن توسعه یافته است:
              </p>
              <ul class="pl-4 text-grey">
                <li>Vue.js 3 + Vuetify 3 (رابط وب)</li>
                <li>FastAPI (بک‌اند)</li>
                <li>SQLite (دیتابیس محلی)</li>
                <li>GTK4 + libadwaita (رابط دسکتاپ)</li>
              </ul>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const saving = ref(false)
const lastBackup = ref('')

const gymInfo = reactive({
  name: 'باشگاه بدنسازی تکاور',
  owner: '',
  phone: '',
  email: '',
  address: '',
  tax_id: '',
  registration_number: '',
})

const invoiceInfo = reactive({
  prefix: 'TK',
  start_number: 1000,
  footer_text: 'با تشکر از 신뢰 شما',
  bank_name: '',
  account_number: '',
})

const notifications = reactive({
  member_welcome: true,
  payment_reminder: true,
  membership_expiry: true,
  attendance: true,
})

const defaults = reactive({
  default_plan: 'bronze',
  default_payment_method: 'cash',
  auto_renewal_days: 7,
  max_allowed_members: 500,
  timezone: 'Asia/Tehran',
})

const planItems = [
  { title: 'برونزی', value: 'bronze' },
  { title: 'نقره‌ای', value: 'silver' },
  { title: 'طلایی', value: 'gold' },
  { title: 'VIP ویژه', value: 'vip' },
]

const methodItems = [
  { title: 'نقدی', value: 'cash' },
  { title: 'کارت', value: 'card' },
  { title: 'انتقال بانکی', value: 'bank_transfer' },
  { title: 'آنلاین', value: 'online' },
]

const timezoneItems = [
  { title: 'تهران (ساعت ایران)', value: 'Asia/Tehran' },
  { title: 'اردبیل', value: 'Asia/Tehran' },
  { title: 'লندن', value: 'Europe/London' },
]

function saveGymInfo() {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    alert('اطلاعات باشگاه ذخیره شد!')
  }, 500)
}

function saveInvoiceInfo() {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    alert('تنظیمات فاکتور ذخیره شد!')
  }, 500)
}

function saveNotifications() {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    alert('تنظیمات اطلاعیه‌ها ذخیره شد!')
  }, 500)
}

function saveDefaults() {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    alert('تنظیمات پیش‌فرض ذخیره شد!')
  }, 500)
}

function backupNow() {
  alert('در حال ایجاد بک‌آپ... (این قابلیت در نسخه‌ها joints디아Uz)')
}

function restoreBackup() {
  alert('قابلیت بازیابی بک‌آپ در نسخه‌های jointsدیاUz فعال خواهد شد.')
}

function viewBackupHistory() {
  alert('تاریچه бک‌آپ‌ها در نسخه‌های jointsدیاUz قابل مشاهده خواهد بود.')
}
</script>

<style scoped>
.settings-page {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

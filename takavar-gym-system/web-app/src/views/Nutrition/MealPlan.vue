<template>
  <div class="nutrition-page">
    <div class="d-flex align-center justify-space-between mb-4">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: #E95420;">
          🍎 برنامه‌های تغذیه‌ای
        </h1>
        <p class="text-body-2 text-grey">برنامه رژیم غذایی و تغذیه برای اعضا</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-food-plus" @click="showAddDialog = true">
        برنامه جدید
      </v-btn>
    </div>

    <v-row>
      <v-col v-for="plan in mealPlans" :key="plan.id" cols="12" md="6" lg="4">
        <v-card color="surface-variant" class="plan-card h-100">
          <v-card-item>
            <v-avatar color="green" size="48">
              <v-icon>mdi-food</v-icon>
            </v-avatar>
            <v-card-title>{{ plan.plan_name || 'برنامه تغذیه' }}</v-card-title>
            <v-card-subtitle>
              <v-chip size="small" color="green" variant="tonal">
                {{ plan.target_calories || 0 }} کیلوکالی
              </v-chip>
            </v-card-subtitle>
          </v-card-item>
          <v-card-text>
            <div class="d-flex flex-wrap gap-2 mb-3">
              <v-chip color="primary" size="small" variant="tonal">
                پروتئین: {{ plan.protein_grams || 0 }}g
              </v-chip>
              <v-chip color="info" size="small" variant="tonal">
                کربوهیدرات: {{ plan.carbs_grams || 0 }}g
              </v-chip>
              <v-chip color="orange" size="small" variant="tonal">
                چربی: {{ plan.fat_grams || 0 }}g
              </v-chip>
            </div>
            <v-textarea v-model="plan.notes" label="یادداشت" variant="outlined" density="compact" rows="2" readonly auto-grow></v-textarea>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="mealPlans.length === 0" cols="12">
        <v-card color="surface-variant" class="d-flex align-center justify-center pa-8">
          <div class="text-center">
            <v-icon size="48" color="grey" class="mb-2">mdi-food</v-icon>
            <p class="text-body-2 text-grey">هیچ برنامه تغذیه‌ای ثبت نشده</p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface-variant">
        <v-card-item>
          <v-avatar color="green" size="40"><v-icon>mdi-food-plus</v-icon></v-avatar>
          <v-card-title>ثبت برنامه تغذیه جدید</v-card-title>
          <v-card-subtitle>فرم برنامه رژیم غذایی</v-card-subtitle>
          <template #append>
            <v-btn variant="text" @click="showAddDialog = false">بستن</v-btn>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <v-select v-model="form.member_id" :items="memberItems" item-title="name" item-value="id" label="انتخاب عضو" variant="outlined" density="comfortable" hide-details :loading="membersLoading"></v-select>
          <v-text-field v-model="form.plan_name" label="نام برنامه" variant="outlined" density="comfortable"></v-text-field>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.target_calories" label="هدف کالری" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model.number="form.protein_grams" label="پروتئین (g)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="4">
              <v-text-field v-model.number="form.carbs_grams" label="کربوهیدرات (g)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
            <v-col cols="12" sm="4">
              <v-text-field v-model.number="form.fat_grams" label="چربی (g)" type="number" variant="outlined" density="comfortable"></v-text-field>
            </v-col>
          </v-row>
          <v-textarea v-model="form.notes" label="یادداشت" variant="outlined" density="comfortable" rows="3" auto-grow></v-textarea>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showAddDialog = false">انصراف</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" :disabled="!form.member_id" @click="savePlan">ثبت برنامه</v-btn>
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
const mealPlans = ref([])
const members = ref([])
const memberItems = ref([])
const showAddDialog = ref(false)
const saving = ref(false)

const form = reactive({
  member_id: null,
  plan_name: 'برنامه رژیم غذایی',
  target_calories: 2000,
  protein_grams: 150,
  carbs_grams: 200,
  fat_grams: 60,
  notes: '',
})

async function loadPlans() {
  loading.value = true
  try {
    const response = await axios.get('/api/meal-plans')
    mealPlans.value = response.data || []
  } catch (err) {
    console.error('Error loading meal plans:', err)
    mealPlans.value = []
  } finally {
    loading.value = false
  }
}

async function loadMembers() {
  membersLoading.value = true
  try {
    const response = await axios.get('/api/members?status=active')
    members.value = response.data || []
    memberItems.value = members.map(m => ({ id: m.id, name: `${m.first_name} ${m.last_name}`, phone: m.phone }))
  } catch (err) {
    console.error('Error loading members:', err)
  } finally {
    membersLoading.value = false
  }
}

async function savePlan() {
  if (!form.member_id) return
  saving.value = true
  try {
    await axios.post('/api/meal-plans', {
      member_id: form.member_id,
      plan_name: form.plan_name,
      target_calories: form.target_calories,
      protein_grams: form.protein_grams,
      carbs_grams: form.carbs_grams,
      fat_grams: form.fat_grams,
      notes: form.notes,
    })
    showAddDialog.value = false
    resetForm()
    loadPlans()
  } catch (err) {
    console.error('Error saving meal plan:', err)
  } finally {
    saving.value = false
  }
}

function resetForm() {
  form.member_id = null
  form.plan_name = 'برنامه رژیم غذایی'
  form.target_calories = 2000
  form.protein_grams = 150
  form.carbs_grams = 200
  form.fat_grams = 60
  form.notes = ''
}

onMounted(() => {
  loadPlans()
  loadMembers()
})
</script>

<style scoped>
.plan-card {
  transition: all 0.3s ease;
}
.plan-card:hover {
  border-color: #E95420;
}
</style>

<template>
  <v-app class="login-app">
    <v-main class="d-flex align-center justify-center login-bg">
      <v-card
        class="login-card mx-auto"
        rounded="xl"
        elevation="8"
        max-width="440"
      >
        <v-card-text class="pa-8">
          <!-- Logo and title -->
          <div class="text-center mb-6">
            <div class="d-flex justify-center mb-3">
              <v-avatar
                color="primary"
                size="72"
                class="mb-2"
              >
                <v-icon size="40" color="white">
                  mdi-dumbbell
                </v-icon>
              </v-avatar>
            </div>
            <h1 class="text-h4 font-weight-bold" style="color: #E95420;">
              تکاور
            </h1>
            <p class="text-body-1 text-grey mt-1">
              سیستم مدیریت باشگاه بدنسازی
            </p>
          </div>

          <!-- Login form -->
          <v-form @submit.prevent="login">
            <v-text-field
              v-model="username"
              label="نام کاربری"
              prepend-inner-icon="mdi-account-outline"
              variant="outlined"
              :rules="[v => !!v || 'لطفاً نام کاربری را وارد کنید']"
              density="comfortable"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="password"
              type="password"
              label="رمز عبور"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              :rules="[v => !!v || 'لطفاً رمز عبور را وارد کنید']"
              density="comfortable"
              class="mb-4"
              @keyup.enter="login"
            ></v-text-field>

            <v-btn
              type="submit"
              block
              size="large"
              color="primary"
              variant="flat"
              :loading="loading"
              class="mb-3"
            >
              ورود به سیستم
            </v-btn>
          </v-form>

          <!-- Error message -->
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            density="compact"
            class="mb-3"
          >
            {{ error }}
          </v-alert>

          <!-- Demo credentials -->
          <div class="text-center mt-4 pa-3" style="background: #2C003E; border-radius: 8px;">
            <p class="text-caption text-grey mb-1">برنامه نمونه برای تست:</p>
            <p class="text-caption text-grey">
              <v-icon size="14" class="mr-1">mdi-account</v-icon>
              کاربر: <strong class="text-white">admin</strong> | رمز: <strong class="text-white">admin123</strong>
            </p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="pa-4 text-center">
          <p class="text-caption text-grey">
            © ۱۴۰۳ - باشگاه بدنسازی تکاور
          </p>
          <p class="text-caption text-grey mt-1">
            تمامی حقوق محفوظ است
          </p>
        </v-card-text>
      </v-card>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function login() {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.post('/api/auth/login', {
      username: username.value,
      password: password.value,
    })

    const { access_token, user } = response.data
    localStorage.setItem('takavar_token', access_token)
    localStorage.setItem('takavar_user', JSON.stringify(user))

    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || err.response?.data?.error || 'خطا در ورود. لطفاً مجدداً تلاش کنید.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-app {
  background: #300A4F;
}

.login-bg {
  background: linear-gradient(135deg, #2C003E 0%, #300A4F 50%, #4A2866 100%);
  min-height: 100vh;
}

.login-card {
  border: 1px solid #4A2866;
  background: #3D1A5C;
}

.login-card .v-card-text {
  background: #3D1A5C;
}

.login-card .v-divider {
  border-color: #4A2866 !important;
}
</style>

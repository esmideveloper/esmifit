import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { fa } from 'vuetify/iconsets/fa'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi, fa },
  },
  theme: {
    defaultTheme: 'takavarTheme',
    themes: {
      takavarTheme: {
        dark: true,
        colors: {
          background: '#300A4F',
          surface: '#3D1A5C',
          'surface-variant': '#2C003E',
          primary: '#E95420',
          'primary-darken-1': '#D04818',
          secondary: '#15AABF',
          accent: '#33D17A',
          error: '#FF5733',
          warning: '#F5C211',
          info: '#15AABF',
          success: '#33D17A',
          'on-background': '#FFFFFF',
          'on-surface': '#FFFFFF',
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-error': '#FFFFFF',
        },
      },
    },
  },
  defaults: {
    VBtn: {
      variant: 'flat',
      color: 'primary',
      rounded: 'lg',
      size: 'small',
    },
    VTextField: {
      variant: 'outlined',
      color: 'primary',
      density: 'comfortable',
      hideDetails: 'auto',
    },
    VCard: {
      rounded: 'lg',
      elevation: 2,
    },
    VChip: {
      rounded: 'lg',
    },
    VDataTable: {
      hover: true,
      itemsPerPage: 10,
      noDataText: 'هیچ داده‌ای یافت شد',
    },
    VCards: {
      variant: 'tonal',
      color: 'surface-variant',
    },
  },
  locale: {
    locale: 'fa',
    fallback: 'en',
    messages: {
      fa: {
        components: {
          VDataTable: {
            itemsPerPage: 'تعداد در صفحه',
            previous: 'قبلی',
            next: 'بعدی',
            first: 'اولین',
            last: 'آخرین',
            sortBy: 'مرتب‌سازی بر اساس',
            sortByAscending: 'صعودی',
            sortByDescending: 'نزولی',
            noData: 'هیچ داده‌ای یافت نشد',
            loading: 'در حال بارگذاری...',
            rowsPerPage: 'تعداد ردیف در صفحه:',
            search: 'جستجو',
            noResults: 'نتیجه‌ای یافت نشد',
            items: 'آیتم‌ها',
            itemsSelected: '{count} آیتم انتخاب شد',
          },
        },
      },
    },
  },
})

# نرم‌افزار مدیریت باشگاه بدنسازی تکاور

Professional Gym Management Desktop Application built with Flutter for Windows.

## ویژگی‌ها

### ماژول‌های اصلی

1. **داشبورد مدیریت**
   - نمای کلی وضعیت روزانه
   - نمودار هفتگی حضور و غیاب
   - KPIهای کلیدی (ورود امروز، تمدیدها، ثبت‌نام جدید، جلسات PT، کلاس‌های گروهی، فاکتورها)
   - کارت‌های شعبه‌ها

2. **اعضا و اشتراک‌ها**
   - پرونده کامل اعضا
   - مدیریت اشتراک‌ها و تمدیدها
   - جستجو و فیلتر پیشرفته

3. **گزارش‌ها و مالی**
   - گزارش درآمد روزانه/ماهانه
   - مدیریت بدهی‌ها و بستانکاری‌ها
   - صدور فاکتور
   - خروجی PDF/Excel

4. **کلاس‌ها و تقویم**
   - برنامه کلاس‌های گروهی
   - جلسات PT
   - تقویم مربیان

5. **تنظیمات**
   - پشتیبان‌گیری و بازیابی
   - Import/Export اعضا
   - تنظیمات چاپ و گزارش‌ها

## طراحی UI

این برنامه از زبان طراحی **Liquid Glass** استفاده می‌کند:
- پنل‌های شیشه‌ای با BackdropFilter blur
- گرادیان‌های دقیق و borderهای نازک
- انیمیشن‌های ورود با زمان‌بندی مشخص
- سیستم Scaling مبتنی بر واحد `u`

### مشخصات فنی طراحی

- Reference canvas: 1357 × 871 logical pixels
- Scaling unit: `u = min(screenWidth / 1357, screenHeight / 871)`
- فونت: Vazirmatn (وزیر)
- رنگ پس‌زمینه: `#04121B`
- رنگ متن: `#FFFFFF`

## پیش‌نیازها

- Flutter SDK >= 3.0.0
- Windows 10/11 (برای build نهایی)
- Visual Studio 2022 با کامپوننت‌های C++ Desktop development

## نصب و اجرا

### 1. دریافت فونت‌ها و Assets

فونت‌های وزیر را از مخزن رسمی دانلود کنید:
```bash
# Download from https://github.com/rastikerdar/vazirmatn/releases
```

فایل‌های مورد نیاز:
- `assets/fonts/Vazirmatn-Regular.ttf`
- `assets/fonts/Vazirmatn-Medium.ttf`
- `assets/fonts/Vazirmatn-SemiBold.ttf`
- `assets/fonts/Vazirmatn-Bold.ttf`
- `assets/images/storm-background.jpg` (تصویر پس‌زمینه)
- `assets/images/avatar.jpg` (آواتار کاربر)

### 2. نصب وابستگی‌ها

```bash
cd takavor_gym_app
flutter pub get
```

### 3. اجرای برنامه

```bash
# برای Windows Desktop
flutter run -d windows

# یا برای تست سریع‌تر (وب)
flutter run -d chrome
```

### 4. ساخت فایل اجرایی

```bash
flutter build windows --release
```

خروجی در مسیر زیر قرار می‌گیرد:
```
build/windows/runner/Release/takavor_gym_app.exe
```

## ساختار پروژه

```
lib/
├── main.dart                 # نقطه شروع برنامه
├── routes/
│   └── app_router.dart       # تنظیمات مسیریابی
├── data/
│   ├── database/             # لایه دیتابیس (SQLite/Drift)
│   ├── repositories/         # repository implementations
│   └── sources/              # data sources
├── domain/
│   ├── entities/             # business entities
│   ├── repositories/         # repository interfaces
│   └── usecases/             # business logic
└── presentation/
    ├── providers/            # Riverpod state management
    ├── screens/              # صفحات برنامه
    │   ├── dashboard/
    │   ├── members/
    │   ├── finance/
    │   ├── classes/
    │   └── settings/
    └── widgets/              # ویجت‌های سفارشی
        ├── liquid_glass_widgets.dart
        └── wave_chart_painter.dart
```

## تکنولوژی‌های استفاده شده

- **Flutter** - فریم‌ورک UI
- **Riverpod** - State Management
- **GoRouter** - مسیریابی
- **Drift** - دیتابیس SQLite
- **Shamsi Date** - تاریخ شمسی
- **Window Manager** - مدیریت پنجره دسکتاپ
- **PDF** - تولید گزارش PDF
- **CSV** - خروجی Excel

## مجوزها

فونت Vazirmatn تحت مجوز OFL منتشر شده است.

## تماس و پشتیبانی

برای گزارش مشکلات یا پیشنهاد ویژگی‌های جدید، لطفاً از طریق Issues اقدام کنید.

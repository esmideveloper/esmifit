-- takavar Gym System - Initial Database Schema
-- Version: 1.0.0
-- تاریخ: ۱۴۰۳

-- ═══════════════════════════════════════════════════════════════
-- جدول‌های اصلی
-- ═══════════════════════════════════════════════════════════════

-- کاربران و دسترسی‌ها
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    role ENUM('admin', 'manager', 'trainer', 'staff', 'accountant') DEFAULT 'staff',
    status ENUM('active', 'inactive', 'locked') DEFAULT 'active',
    last_login DATETIME,
    failed_attempts INTEGER DEFAULT 0,
    locked_until DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- اعضا
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    national_id VARCHAR(20) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(255),
    birth_date DATE,
    gender ENUM('male', 'female', 'other'),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    medical_conditions TEXT,
    membership_type ENUM('gold', 'silver', 'bronze', 'vip', 'free_trial') DEFAULT 'bronze',
    membership_start DATE,
    membership_end DATE,
    status ENUM('active', 'inactive', 'suspended', 'expired', 'cancelled') DEFAULT 'active',
    weight DECIMAL(5, 2),
    height DECIMAL(5, 2),
    body_fat_pct DECIMAL(5, 2),
    chest_circumference DECIMAL(5, 2),
    waist_circumference DECIMAL(5, 2),
    hip_circumference DECIMAL(5, 2),
    notes TEXT,
    profile_picture_path VARCHAR(500),
    qr_code VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);

-- پلن‌های عضویت
CREATE TABLE IF NOT EXISTS subscription_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_days INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'IRT',
    is_active BOOLEAN DEFAULT TRUE,
    max_allowed_members INTEGER,
    included_features JSON,
    priority INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- عضویت‌های اعضا
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES members(id),
    plan_id INTEGER NOT NULL REFERENCES subscription_plans(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price_paid DECIMAL(10, 2),
    payment_status ENUM('pending', 'paid', 'partial', 'overdue', 'cancelled') DEFAULT 'pending',
    auto_renewal BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- پرداخت‌ها
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_id INTEGER REFERENCES subscriptions(id),
    member_id INTEGER NOT NULL REFERENCES members(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('cash', 'card', 'bank_transfer', 'online', 'installment') DEFAULT 'cash',
    transaction_ref VARCHAR(100),
    invoice_number VARCHAR(50),
    status ENUM('completed', 'pending', 'failed', 'refunded') DEFAULT 'completed',
    receipt_path VARCHAR(500),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);

-- سالن‌ها
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    capacity INTEGER DEFAULT 0,
    equipment_ids JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- کلاس‌های ورزشی
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('bodybuilding', 'cardio', 'hiit', 'crossfit', 'yoga', 'pilates', 'functional', 'personal_training', 'group') NOT NULL,
    duration_minutes INTEGER NOT NULL,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced', 'all_levels') DEFAULT 'all_levels',
    max_capacity INTEGER NOT NULL,
    room_id INTEGER REFERENCES rooms(id),
    trainer_id INTEGER REFERENCES trainers(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- زمان‌بندی کلاس‌ها
CREATE TABLE IF NOT EXISTS class_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL REFERENCES classes(id),
    day_of_week ENUM('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- تمرینات
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    muscle_group ENUM('chest', 'back', 'shoulders', 'biceps', 'triceps', 'legs', 'core', 'full_body', 'cardio') NOT NULL,
    equipment_needed TEXT,
    instructions TEXT,
    video_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE
);

-- لاگ‌های تمرینی
CREATE TABLE IF NOT EXISTS workout_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES members(id),
    trainer_id INTEGER REFERENCES trainers(id),
    workout_date DATE NOT NULL,
    workout_type ENUM('strength', 'cardio', 'hiit', 'flexibility', 'recovery', 'mixed') NOT NULL,
    duration_minutes INTEGER,
    calories_burned INTEGER,
    notes TEXT,
    exercise_logs JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--Details تمرین در هر لاگ
CREATE TABLE IF NOT EXISTS workout_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_log_id INTEGER NOT NULL REFERENCES workout_logs(id),
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    sets INTEGER,
    reps INTEGER,
    weight DECIMAL(8, 2),
    duration_seconds INTEGER,
    notes TEXT
);

-- تجهیزات
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category ENUM('cardio', 'strength', 'free_weights', 'machines', 'accessories', 'safety') NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    purchase_date DATE,
    purchase_price DECIMAL(10, 2),
    warranty_end_date DATE,
    status ENUM('available', 'in_use', 'maintenance', 'damaged', 'out_of_order') DEFAULT 'available',
    location VARCHAR(200),
    quantity INTEGER DEFAULT 1,
    maintenance_count INTEGER DEFAULT 0,
    last_maintenance_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- کارشناسان بدنسازی
CREATE TABLE IF NOT EXISTS trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    national_id VARCHAR(20) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(255),
    specialization TEXT,
    certifications TEXT,
    years_experience INTEGER,
    hourly_rate DECIMAL(10, 2),
    status ENUM('active', 'inactive', 'on_leave') DEFAULT 'active',
    profile_picture_path VARCHAR(500),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- حضور و غیبت
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES members(id),
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME,
    duration_minutes INTEGER,
    status ENUM('checked_in', 'checked_out', 'no_show') DEFAULT 'checked_in',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- محصولات فروشگاه
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category ENUM('supplement', 'apparel', 'accessory', 'nutrition', 'other') NOT NULL,
    brand VARCHAR(100),
    sku VARCHAR(50) UNIQUE,
    bar_code VARCHAR(50),
    cost_price DECIMAL(10, 2),
    selling_price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    low_stock_alert INTEGER DEFAULT 10,
    unit VARCHAR(50) DEFAULT 'piece',
    expiry_date DATE,
    supplier_id INTEGER REFERENCES suppliers(id),
    image_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- تامین‌کنندگان
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    tax_number VARCHAR(50),
    notes TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- برنامه‌های تغذیه
CREATE TABLE IF NOT EXISTS meal_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES members(id),
    plan_name VARCHAR(100),
    target_calories INTEGER,
    protein_grams DECIMAL(8, 2),
    carbs_grams DECIMAL(8, 2),
    fat_grams DECIMAL(8, 2),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- لاگ‌های تغذیه
CREATE TABLE IF NOT EXISTS nutrition_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES members(id),
    meal_date DATE NOT NULL,
    meal_type VARCHAR(50),
    food_items JSON,
    total_calories INTEGER,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════════
-- ایندکس‌ها
-- ═══════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_members_status ON members(status);
CREATE INDEX IF NOT EXISTS idx_members_membership_type ON members(membership_type);
CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);

CREATE INDEX IF NOT EXISTS idx_subscriptions_member ON subscriptions(member_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_plan ON subscriptions(plan_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(payment_status);

CREATE INDEX IF NOT EXISTS idx_payments_member ON payments(member_id);
CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(payment_date);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

CREATE INDEX IF NOT EXISTS idx_attendance_member ON attendance(member_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(check_in_time);

CREATE INDEX IF NOT EXISTS idx_workout_logs_member ON workout_logs(member_id);
CREATE INDEX IF NOT EXISTS idx_workout_logs_date ON workout_logs(workout_date);

CREATE INDEX IF NOT EXISTS idx_equipment_status ON equipment(status);
CREATE INDEX IF NOT EXISTS idx_equipment_category ON equipment(category);

CREATE INDEX IF NOT EXISTS idx_trainers_status ON trainers(status);

CREATE INDEX IF NOT EXISTS idx_class_schedule_class ON class_schedule(class_id);
CREATE INDEX IF NOT EXISTS idx_class_schedule_day ON class_schedule(day_of_week);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);

-- ═══════════════════════════════════════════════════════════════
-- Triggerها
-- ═══════════════════════════════════════════════════════════════

-- به‌روزرسانی خودکار updated_at
CREATE TRIGGER IF NOT EXISTS update_members_timestamp
AFTER UPDATE ON members
FOR EACH ROW
BEGIN
    UPDATE members SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_subscriptions_timestamp
AFTER UPDATE ON subscriptions
FOR EACH ROW
BEGIN
    UPDATE subscriptions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_equipment_timestamp
AFTER UPDATE ON equipment
FOR EACH ROW
BEGIN
    UPDATE equipment SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_trainers_timestamp
AFTER UPDATE ON trainers
FOR EACH ROW
BEGIN
    UPDATE trainers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_products_timestamp
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_meal_plans_timestamp
AFTER UPDATE ON meal_plans
FOR EACH ROW
BEGIN
    UPDATE meal_plans SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

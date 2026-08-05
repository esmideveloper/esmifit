from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, Numeric, Boolean, Enum, ForeignKey, JSON, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import enum
from datetime import datetime
from typing import Optional

Base = declarative_base()

# ── Enums ──────────────────────────────────────────────────────────
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class MembershipTypeEnum(str, enum.Enum):
    gold = "gold"
    silver = "silver"
    bronze = "bronze"
    vip = "vip"
    free_trial = "free_trial"

class MemberStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    expired = "expired"
    cancelled = "cancelled"

class PlanStatusEnum(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    partial = "partial"
    overdue = "overdue"
    cancelled = "cancelled"

class PaymentStatusEnum(str, enum.Enum):
    completed = "completed"
    pending = "pending"
    failed = "failed"
    refunded = "refunded"

class PaymentMethodEnum(str, enum.Enum):
    cash = "cash"
    card = "card"
    bank_transfer = "bank_transfer"
    online = "online"
    installment = "installment"

class ClassCategoryEnum(str, enum.Enum):
    bodybuilding = "bodybuilding"
    cardio = "cardio"
    hiit = "hiit"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    functional = "functional"
    personal_training = "personal_training"
    group = "group"

class DifficultyLevelEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    all_levels = "all_levels"

class EquipmentCategoryEnum(str, enum.Enum):
    cardio = "cardio"
    strength = "strength"
    free_weights = "free_weights"
    machines = "machines"
    accessories = "accessories"
    safety = "safety"

class EquipmentStatusEnum(str, enum.Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"
    damaged = "damaged"
    out_of_order = "out_of_order"

class DayOfWeekEnum(str, enum.Enum):
    saturday = "saturday"
    sunday = "sunday"
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"

class WorkoutTypeEnum(str, enum.Enum):
    strength = "strength"
    cardio = "cardio"
    hiit = "hiit"
    flexibility = "flexibility"
    recovery = "recovery"
    mixed = "mixed"

class MuscleGroupEnum(str, enum.Enum):
    chest = "chest"
    back = "back"
    shoulders = "shoulders"
    biceps = "biceps"
    triceps = "triceps"
    legs = "legs"
    core = "core"
    full_body = "full_body"
    cardio_muscle = "cardio"

class TrainerStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    on_leave = "on_leave"

class AttendStatusEnum(str, enum.Enum):
    checked_in = "checked_in"
    checked_out = "checked_out"
    no_show = "no_show"

class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    trainer = "trainer"
    staff = "staff"
    accountant = "accountant"

class UserStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    locked = "locked"

class ProductCategoryEnum(str, enum.Enum):
    supplement = "supplement"
    apparel = "apparel"
    accessory = "accessory"
    nutrition = "nutrition"
    other = "other"

class ProductStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class SupplierStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class AttendanceStatusEnum(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"


# ── Tables ─────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.staff)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.active)
    last_login = Column(DateTime)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    national_id = Column(String(20), unique=True)
    phone = Column(String(20))
    email = Column(String(255))
    birth_date = Column(Date)
    gender = Column(Enum(GenderEnum))
    address = Column(Text)
    city = Column(String(100))
    postal_code = Column(String(20))
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    medical_conditions = Column(Text)
    membership_type = Column(Enum(MembershipTypeEnum), default=MembershipTypeEnum.bronze)
    membership_start = Column(Date)
    membership_end = Column(Date)
    status = Column(Enum(MemberStatusEnum), default=MemberStatusEnum.active)
    weight = Column(Numeric(5, 2))
    height = Column(Numeric(5, 2))
    body_fat_pct = Column(Numeric(5, 2))
    chest_circumference = Column(Numeric(5, 2))
    waist_circumference = Column(Numeric(5, 2))
    hip_circumference = Column(Numeric(5, 2))
    notes = Column(Text)
    profile_picture_path = Column(String(500))
    qr_code = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    updated_by = Column(Integer, ForeignKey('users.id'))

    subscriptions = relationship("Subscription", back_populates="member")
    payments = relationship("Payment", back_populates="member")
    workout_logs = relationship("WorkoutLog", back_populates="member")
    attendance_records = relationship("Attendance", back_populates="member")


class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='IRT')
    is_active = Column(Boolean, default=True)
    max_allowed_members = Column(Integer)
    included_features = Column(JSON)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price_paid = Column(Numeric(10, 2))
    payment_status = Column(Enum(PlanStatusEnum), default=PlanStatusEnum.pending)
    auto_renewal = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(Enum(PaymentMethodEnum), default=PaymentMethodEnum.cash)
    transaction_ref = Column(String(100))
    invoice_number = Column(String(50))
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.completed)
    receipt_path = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))

    member = relationship("Member", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    capacity = Column(Integer, default=0)
    equipment_ids = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(Enum(ClassCategoryEnum), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    difficulty_level = Column(Enum(DifficultyLevelEnum), default=DifficultyLevelEnum.all_levels)
    max_capacity = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    trainer_id = Column(Integer, ForeignKey('trainers.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    schedule_entries = relationship("ClassSchedule", back_populates="class_")
    room = relationship("Room")


class ClassSchedule(Base):
    __tablename__ = 'class_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    day_of_week = Column(Enum(DayOfWeekEnum), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    class_ = relationship("Class", back_populates="schedule_entries")


class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    muscle_group = Column(Enum(MuscleGroupEnum), nullable=False)
    equipment_needed = Column(Text)
    instructions = Column(Text)
    video_url = Column(String(500))
    is_active = Column(Boolean, default=True)


class WorkoutLog(Base):
    __tablename__ = 'workout_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainers.id'))
    workout_date = Column(Date, nullable=False)
    workout_type = Column(Enum(WorkoutTypeEnum), nullable=False)
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer)
    notes = Column(Text)
    exercise_logs = Column(JSON)
    created_at = Column(DateTime, default=func.now())

    member = relationship("Member", back_populates="workout_logs")
    exercises = relationship("WorkoutExercise", back_populates="workout_log")


class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'
    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_log_id = Column(Integer, ForeignKey('workout_logs.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Numeric(8, 2))
    duration_seconds = Column(Integer)
    notes = Column(Text)

    workout_log = relationship("WorkoutLog", back_populates="exercises")
    exercise = relationship("Exercise")


class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(EquipmentCategoryEnum), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    purchase_date = Column(Date)
    purchase_price = Column(Numeric(10, 2))
    warranty_end_date = Column(Date)
    status = Column(Enum(EquipmentStatusEnum), default=EquipmentStatusEnum.available)
    location = Column(String(200))
    quantity = Column(Integer, default=1)
    maintenance_count = Column(Integer, default=0)
    last_maintenance_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Trainer(Base):
    __tablename__ = 'trainers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    national_id = Column(String(20), unique=True)
    phone = Column(String(20))
    email = Column(String(255))
    specialization = Column(Text)
    certifications = Column(Text)
    years_experience = Column(Integer)
    hourly_rate = Column(Numeric(10, 2))
    status = Column(Enum(TrainerStatusEnum), default=TrainerStatusEnum.active)
    profile_picture_path = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime)
    duration_minutes = Column(Integer)
    status = Column(Enum(AttendStatusEnum), default=AttendStatusEnum.checked_in)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    member = relationship("Member", back_populates="attendance_records")


class Produc(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(Enum(ProductCategoryEnum), nullable=False)
    brand = Column(String(100))
    sku = Column(String(50), unique=True)
    bar_code = Column(String(50))
    cost_price = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    low_stock_alert = Column(Integer, default=10)
    unit = Column(String(50), default='piece')
    expiry_date = Column(Date)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    image_path = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    tax_number = Column(String(50))
    notes = Column(Text)
    status = Column(Enum(SupplierStatusEnum), default=SupplierStatusEnum.active)
    created_at = Column(DateTime, default=func.now())


class MealPlan(Base):
    __tablename__ = 'meal_plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    plan_name = Column(String(100))
    target_calories = Column(Integer)
    protein_grams = Column(Numeric(8, 2))
    carbs_grams = Column(Numeric(8, 2))
    fat_grams = Column(Numeric(8, 2))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    meal_date = Column(Date, nullable=False)
    meal_type = Column(String(50))  # breakfast, lunch, dinner, snack
    food_items = Column(JSON)
    total_calories = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())


# ── DB Helper ──────────────────────────────────────────────────────
def init_db(db_path: str = "gym_system.db"):
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

#!/usr/bin/env python3
import os, sys, time, base64, json, hashlib
from datetime import datetime, timedelta, date
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
import uvicorn
import qrcode
import jwt
import bcrypt
import pdfkit
from io import BytesIO
import threading
import uuid

# ── Add parent to path ──
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models import (
    Base, User, Member, SubscriptionPlan, Subscription, Payment,
    Class, ClassSchedule, Exercise, WorkoutLog, WorkoutExercise,
    Equipment, Trainer, Attendance, Produc, Supplier,
    MealPlan, NutritionLog, Room, init_db, GenderEnum, UserRoleEnum,
    UserStatusEnum, MemberStatusEnum, PlanStatusEnum,
    PaymentStatusEnum, PaymentMethodEnum, ClassCategoryEnum,
    DifficultyLevelEnum, EquipmentCategoryEnum, EquipmentStatusEnum,
    DayOfWeekEnum, WorkoutTypeEnum, MuscleGroupEnum,
    TrainerStatusEnum, AttendStatusEnum,
    ProductCategoryEnum, ProductStatusEnum, SupplierStatusEnum
)

# ── Config ──
SECRET_KEY = "takavar-gym-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7일

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "gym_system.db")
db_path_abs = os.path.abspath(DB_PATH)

engine, SessionLocal = None, None

# ── Init DB ──
engine, SessionLocal = init_db(db_path_abs)


# ── Pydantic Schemas ──
class UserCreate(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: UserRoleEnum = UserRoleEnum.staff

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    national_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_conditions: Optional[str] = None
    membership_type: MembershipTypeEnum = MembershipTypeEnum.bronze
    membership_start: Optional[str] = None
    membership_end: Optional[str] = None
    status: MemberStatusEnum = MemberStatusEnum.active
    weight: Optional[float] = None
    height: Optional[float] = None
    body_fat_pct: Optional[float] = None
    chest_circumference: Optional[float] = None
    waist_circumference: Optional[float] = None
    hip_circumference: Optional[float] = None
    notes: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    national_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[GenderEnum] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_conditions: Optional[str] = None
    membership_type: Optional[MembershipTypeEnum] = None
    membership_start: Optional[str] = None
    membership_end: Optional[str] = None
    status: Optional[MemberStatusEnum] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    body_fat_pct: Optional[float] = None
    chest_circumference: Optional[float] = None
    waist_circumference: Optional[float] = None
    hip_circumference: Optional[float] = None
    notes: Optional[str] = None

class MemberResponse(MemberBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SubscriptionPlanCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration_days: int
    price: float
    currency: str = "IRT"
    max_allowed_members: Optional[int] = None
    included_features: Optional[dict] = None
    priority: int = 0

class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration_days: int
    price: float
    currency: str
    is_active: bool
    max_allowed_members: Optional[int]
    included_features: Optional[dict]
    priority: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    member_id: int
    plan_id: int
    start_date: str
    end_date: str
    price_paid: Optional[float] = None
    payment_status: PlanStatusEnum = PlanStatusEnum.pending
    auto_renewal: bool = False
    notes: Optional[str] = None

class SubscriptionResponse(BaseModel):
    id: int
    member_id: int
    plan_id: int
    start_date: str
    end_date: str
    price_paid: Optional[float]
    payment_status: PlanStatusEnum
    auto_renewal: bool
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    subscription_id: Optional[int] = None
    member_id: int
    amount: float
    payment_date: str
    payment_method: PaymentMethodEnum = PaymentMethodEnum.cash
    transaction_ref: Optional[str] = None
    invoice_number: Optional[str] = None
    status: PaymentStatusEnum = PaymentStatusEnum.completed
    notes: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    subscription_id: Optional[int]
    member_id: int
    amount: float
    payment_date: str
    payment_method: PaymentMethodEnum
    transaction_ref: Optional[str]
    invoice_number: Optional[str]
    status: PaymentStatusEnum
    receipt_path: Optional[str]
    notes: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

class EquipmentCreate(BaseModel):
    name: str
    category: EquipmentCategoryEnum
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_price: Optional[float] = None
    warranty_end_date: Optional[str] = None
    status: EquipmentStatusEnum = EquipmentStatusEnum.available
    location: Optional[str] = None
    quantity: int = 1
    notes: Optional[str] = None

class EquipmentResponse(BaseModel):
    id: int
    name: str
    category: EquipmentCategoryEnum
    brand: Optional[str]
    model: Optional[str]
    serial_number: Optional[str]
    purchase_date: Optional[str]
    purchase_price: Optional[float]
    warranty_end_date: Optional[str]
    status: EquipmentStatusEnum
    location: Optional[str]
    quantity: int
    maintenance_count: int
    last_maintenance_date: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class TrainerCreate(BaseModel):
    first_name: str
    last_name: str
    national_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None
    certifications: Optional[str] = None
    years_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    status: TrainerStatusEnum = TrainerStatusEnum.active
    notes: Optional[str] = None

class TrainerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    national_id: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    specialization: Optional[str]
    certifications: Optional[str]
    years_experience: Optional[int]
    hourly_rate: Optional[float]
    status: TrainerStatusEnum
    profile_picture_path: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class ClassCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: ClassCategoryEnum
    duration_minutes: int
    difficulty_level: DifficultyLevelEnum = DifficultyLevelEnum.all_levels
    max_capacity: int
    room_id: Optional[int] = None
    trainer_id: Optional[int] = None

class ClassScheduleCreate(BaseModel):
    class_id: int
    day_of_week: DayOfWeekEnum
    start_time: str
    end_time: str

class ClassResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: ClassCategoryEnum
    duration_minutes: int
    difficulty_level: DifficultyLevelEnum
    max_capacity: int
    room_id: Optional[int]
    trainer_id: Optional[int]
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class WorkoutLogCreate(BaseModel):
    member_id: int
    trainer_id: Optional[int] = None
    workout_date: str
    workout_type: WorkoutTypeEnum
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    exercise_logs: Optional[list] = None

class WorkoutLogResponse(BaseModel):
    id: int
    member_id: int
    trainer_id: Optional[int]
    workout_date: str
    workout_type: WorkoutTypeEnum
    duration_minutes: Optional[int]
    calories_burned: Optional[int]
    notes: Optional[str]
    exercise_logs: Optional[list]
    created_at: str

    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    member_id: int
    check_in_time: Optional[str] = None
    notes: Optional[str] = None

class AttendanceResponse(BaseModel):
    id: int
    member_id: int
    check_in_time: str
    check_out_time: Optional[str]
    duration_minutes: Optional[int]
    status: AttendStatusEnum
    notes: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: ProductCategoryEnum
    brand: Optional[str] = None
    sku: Optional[str] = None
    bar_code: Optional[str] = None
    cost_price: Optional[float] = None
    selling_price: float
    stock_quantity: int = 0
    low_stock_alert: int = 10
    unit: str = "piece"
    expiry_date: Optional[str] = None
    supplier_id: Optional[int] = None
    image_path: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: ProductCategoryEnum
    brand: Optional[str]
    sku: Optional[str]
    bar_code: Optional[str]
    cost_price: Optional[float]
    selling_price: float
    stock_quantity: int
    low_stock_alert: int
    unit: str
    expiry_date: Optional[str]
    supplier_id: Optional[int]
    image_path: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_person: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    tax_number: Optional[str]
    notes: Optional[str]
    status: SupplierStatusEnum
    created_at: str

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    new_members_this_month: int
    total_subscriptions: int
    active_subscriptions: int
    total_revenue: float
    revenue_this_month: float
    pending_payments: int
    overdue_payments: int
    total_trainers: int
    total_classes: int
    today_attendance: int
    equipment_count: int
    equipment_available: int
    equipment_maintenance: int


# ── Auth ──
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

oauth2_scheme = HTTPBearer()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_token(creds.credentials)
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        db: Session = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        if not user or user.status != UserStatusEnum.active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ── App ──
app = FastAPI(title="Takavar Gym System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ──
@app.get("/")
async def root():
    return {"message": "Takavar Gym System API", "version": "1.0.0", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}


# ── Auth Endpoints ──
@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == user_data.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            password_hash=hashed,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            role=user_data.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        token = create_access_token({"sub": new_user.username, "role": new_user.role.value})
        return Token(
            access_token=token,
            user={
                "id": new_user.id,
                "username": new_user.username,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "role": new_user.role.value,
            }
        )
    finally:
        db.close()


@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == credentials.username).first()
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if user.status != UserStatusEnum.active:
            raise HTTPException(status_code=401, detail="Account is locked or inactive")
        token = create_access_token({"sub": user.username, "role": user.role.value})
        user.last_login = datetime.utcnow()
        db.commit()
        return Token(
            access_token=token,
            user={
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.value,
            }
        )
    finally:
        db.close()


@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role.value,
        "status": current_user.status.value,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
    }


# ── Member Endpoints ──
@app.post("/api/members", response_model=MemberResponse)
async def create_member(member: MemberCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_member = Member(**member.model_dump(), created_by=current_user.id)
        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        # Generate QR code
        qr_data = f"MEMBER:{new_member.id}:{new_member.first_name} {new_member.last_name}"
        qr = qrcode.make(qr_data)
        qr_path = os.path.join(os.path.dirname(__file__), "..", "qr_codes", f"member_{new_member.id}.png")
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr.save(qr_path)
        new_member.qr_code = qr_path
        db.commit()
        db.refresh(new_member)
        return new_member
    finally:
        db.close()


@app.get("/api/members", response_model=List[MemberResponse])
async def list_members(
    status: Optional[str] = None,
    membership_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 50,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(Member)
        if status:
            query = query.filter(Member.status == status)
        if membership_type:
            query = query.filter(Member.membership_type == membership_type)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Member.first_name.ilike(search_term),
                    Member.last_name.ilike(search_term),
                    Member.phone.ilike(search_term),
                    Member.email.ilike(search_term),
                    Member.national_id.ilike(search_term),
                )
            )
        total = query.count()
        members = query.order_by(Member.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return members
    finally:
        db.close()


@app.get("/api/members/{member_id}", response_model=MemberResponse)
async def get_member(member_id: int, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return member
    finally:
        db.close()


@app.put("/api/members/{member_id}", response_model=MemberResponse)
async def update_member(member_id: int, member_data: MemberUpdate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        update_data = member_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(member, key, value)
        member.updated_by = current_user.id
        db.commit()
        db.refresh(member)
        return member
    finally:
        db.close()


@app.delete("/api/members/{member_id}")
async def delete_member(member_id: int, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        member.status = MemberStatusEnum.inactive
        member.updated_by = current_user.id
        db.commit()
        return {"message": "Member deactivated successfully"}


@app.get("/api/members/{member_id}/qr")
async def get_member_qr(member_id: int, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        if not member.qr_code or not os.path.exists(member.qr_code):
            qr_data = f"MEMBER:{member.id}:{member.first_name} {member.last_name}"
            qr = qrcode.make(qr_data)
            qr_path = os.path.join(os.path.dirname(__file__), "..", "qr_codes", f"member_{member.id}.png")
            os.makedirs(os.path.dirname(qr_path), exist_ok=True)
            qr.save(qr_path)
            member.qr_code = qr_path
            db.commit()
        return {"qr_code_path": member.qr_code}
    finally:
        db.close()


@app.get("/api/members/export")
async def export_members(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        members = db.query(Member).order_by(Member.created_at.desc()).all()
        csv_data = "ID,First Name,Last Name,Phone,Email,Status,Membership Type,Membership Start,Membership End,Created At\n"
        for m in members:
            csv_data += f'{m.id},"{m.first_name}","{m.last_name}","{m.phone or ""}","{m.email or ""}",{m.status.value},{m.membership_type.value},{m.membership_start or ""},{m.membership_end or ""},{m.created_at}\n'
        return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=members.csv"})
    finally:
        db.close()


# ── Subscription Plan Endpoints ──
@app.post("/api/subscription-plans", response_model=SubscriptionPlanResponse)
async def create_plan(plan: SubscriptionPlanCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_plan = SubscriptionPlan(**plan.model_dump())
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        return new_plan
    finally:
        db.close()


@app.get("/api/subscription-plans", response_model=List[SubscriptionPlanResponse])
async def list_plans(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        plans = db.query(SubscriptionPlan).order_by(SubscriptionPlan.priority.desc()).all()
        return plans
    finally:
        db.close()


@app.put("/api/subscription-plans/{plan_id}", response_model=SubscriptionPlanResponse)
async def update_plan(plan_id: int, plan_data: SubscriptionPlanCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        for key, value in plan_data.model_dump().items():
            setattr(plan, key, value)
        db.commit()
        db.refresh(plan)
        return plan
    finally:
        db.close()


# ── Subscription Endpoints ──
@app.post("/api/subscriptions", response_model=SubscriptionResponse)
async def create_subscription(sub: SubscriptionCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == sub.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == sub.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        new_sub = Subscription(**sub.model_dump())
        db.add(new_sub)
        member.status = MemberStatusEnum.active
        member.membership_type = plan.name.lower().replace(" ", "_")
        member.membership_start = sub.start_date
        member.membership_end = sub.end_date
        db.commit()
        db.refresh(new_sub)
        return new_sub
    finally:
        db.close()


@app.get("/api/subscriptions", response_model=List[SubscriptionResponse])
async def list_subscriptions(
    status: Optional[str] = None,
    member_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(Subscription).options(joinedload(Subscription.member), joinedload(Subscription.plan))
        if status:
            query = query.filter(Subscription.payment_status == status)
        if member_id:
            query = query.filter(Subscription.member_id == member_id)
        return query.order_by(Subscription.end_date.desc()).all()
    finally:
        db.close()


@app.get("/api/subscriptions/{sub_id}", response_model=SubscriptionResponse)
async def get_subscription(sub_id: int, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
        if not sub:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return sub
    finally:
        db.close()


@app.put("/api/subscriptions/{sub_id}")
async def update_subscription(sub_id: int, sub_data: dict, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
        if not sub:
            raise HTTPException(status_code=404, detail="Subscription not found")
        for k, v in sub_data.items():
            setattr(sub, k, v)
        db.commit()
        return {"message": "Subscription updated successfully"}
    finally:
        db.close()


# ── Payment Endpoints ──
@app.post("/api/payments", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == payment.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        new_payment = Payment(**payment.model_dump(), created_by=current_user.id)
        db.add(new_payment)
        if payment.subscription_id:
            sub = db.query(Subscription).filter(Subscription.id == payment.subscription_id).first()
            if sub:
                sub.payment_status = PlanStatusEnum.paid
        db.commit()
        db.refresh(new_payment)
        return new_payment
    finally:
        db.close()


@app.get("/api/payments", response_model=List[PaymentResponse])
async def list_payments(
    member_id: Optional[int] = None,
    status: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(Payment).options(joinedload(Payment.member))
        if member_id:
            query = query.filter(Payment.member_id == member_id)
        if status:
            query = query.filter(Payment.status == status)
        if from_date:
            query = query.filter(Payment.payment_date >= from_date)
        if to_date:
            query = query.filter(Payment.payment_date <= to_date)
        return query.order_by(Payment.payment_date.desc()).all()
    finally:
        db.close()


@app.get("/api/payments/summary")
async def payment_summary(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        total_payments = db.query(Payment).filter(Payment.status == PaymentStatusEnum.completed).count()
        total_amount = db.query(Payment).filter(Payment.status == PaymentStatusEnum.completed).with_entities(
            db.func.sum(Payment.amount)
        ).scalar() or 0

        this_month = date.today().replace(day=1)
        month_amount = db.query(Payment).filter(
            Payment.status == PaymentStatusEnum.completed,
            Payment.payment_date >= this_month
        ).with_entities(db.func.sum(Payment.amount)).scalar() or 0

        pending = db.query(Payment).filter(Payment.status == PaymentStatusEnum.pending).count()
        return {
            "total_payments": total_payments,
            "total_amount": float(total_amount),
            "month_amount": float(month_amount),
            "pending_count": pending,
        }
    finally:
        db.close()


# ── Equipment Endpoints ──
@app.post("/api/equipment", response_model=EquipmentResponse)
async def create_equipment(equip: EquipmentCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_equip = Equipment(**equip.model_dump())
        db.add(new_equip)
        db.commit()
        db.refresh(new_equip)
        return new_equip
    finally:
        db.close()


@app.get("/api/equipment", response_model=List[EquipmentResponse])
async def list_equipment(
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(Equipment)
        if category:
            query = query.filter(Equipment.category == category)
        if status:
            query = query.filter(Equipment.status == status)
        if search:
            query = query.filter(Equipment.name.ilike(f"%{search}%"))
        return query.order_by(Equipment.name).all()
    finally:
        db.close()


@app.put("/api/equipment/{equip_id}", response_model=EquipmentResponse)
async def update_equipment(equip_id: int, equip_data: dict, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        equip = db.query(Equipment).filter(Equipment.id == equip_id).first()
        if not equip:
            raise HTTPException(status_code=404, detail="Equipment not found")
        for k, v in equip_data.items():
            setattr(equip, k, v)
        db.commit()
        db.refresh(equip)
        return equip
    finally:
        db.close()


# ── Trainer Endpoints ──
@app.post("/api/trainers", response_model=TrainerResponse)
async def create_trainer(trainer: TrainerCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_trainer = Trainer(**trainer.model_dump())
        db.add(new_trainer)
        db.commit()
        db.refresh(new_trainer)
        return new_trainer
    finally:
        db.close()


@app.get("/api/trainers", response_model=List[TrainerResponse])
async def list_trainers(status: Optional[str] = None, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        query = db.query(Trainer)
        if status:
            query = query.filter(Trainer.status == status)
        return query.order_by(Trainer.first_name).all()
    finally:
        db.close()


@app.put("/api/trainers/{trainer_id}", response_model=TrainerResponse)
async def update_trainer(trainer_id: int, trainer_data: dict, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
        if not trainer:
            raise HTTPException(status_code=404, detail="Trainer not found")
        for k, v in trainer_data.items():
            setattr(trainer, k, v)
        db.commit()
        db.refresh(trainer)
        return trainer
    finally:
        db.close()


# ── Class & Schedule Endpoints ──
@app.post("/api/classes", response_model=ClassResponse)
async def create_class(cls: ClassCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_cls = Class(**cls.model_dump())
        db.add(new_cls)
        db.commit()
        db.refresh(new_cls)
        return new_cls
    finally:
        db.close()


@app.get("/api/classes", response_model=List[ClassResponse])
async def list_classes(category: Optional[str] = None, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        query = db.query(Class)
        if category:
            query = query.filter(Class.category == category)
        return query.filter(Class.is_active == True).order_by(Class.name).all()
    finally:
        db.close()


@app.post("/api/classes/{class_id}/schedule")
async def add_schedule(class_id: int, schedule: ClassScheduleCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        cls = db.query(Class).filter(Class.id == class_id).first()
        if not cls:
            raise HTTPException(status_code=404, detail="Class not found")
        new_schedule = ClassSchedule(**schedule.model_dump())
        db.add(new_schedule)
        db.commit()
        return {"message": "Schedule added successfully", "schedule": new_schedule}
    finally:
        db.close()


@app.get("/api/schedule")
async def get_schedule(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        schedules = db.query(ClassSchedule).options(
            joinedload(ClassSchedule.class_).joinedload(Class.trainer),
            joinedload(ClassSchedule.class_).joinedload(Class.room),
        ).filter(ClassSchedule.is_active == True).all()
        result = []
        for s in schedules:
            result.append({
                "id": s.id,
                "class_id": s.class_id,
                "class_name": s.class_.name if s.class_ else None,
                "category": s.class_.category.value if s.class_ else None,
                "trainer_name": f"{s.class_.trainer.first_name} {s.class_.trainer.last_name}" if s.class_ and s.class_.trainer else None,
                "room_name": s.class_.room.name if s.class_ and s.class_.room else None,
                "day_of_week": s.day_of_week.value,
                "start_time": str(s.start_time),
                "end_time": str(s.end_time),
            })
        return result
    finally:
        db.close()


# ── Workout Log Endpoints ──
@app.post("/api/workout-logs", response_model=WorkoutLogResponse)
async def create_workout_log(log: WorkoutLogCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == log.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        new_log = WorkoutLog(**log.model_dump())
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log
    finally:
        db.close()


@app.get("/api/workout-logs", response_model=List[WorkoutLogResponse])
async def list_workout_logs(
    member_id: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(WorkoutLog).options(joinedload(WorkoutLog.member))
        if member_id:
            query = query.filter(WorkoutLog.member_id == member_id)
        if from_date:
            query = query.filter(WorkoutLog.workout_date >= from_date)
        if to_date:
            query = query.filter(WorkoutLog.workout_date <= to_date)
        return query.order_by(WorkoutLog.workout_date.desc()).all()
    finally:
        db.close()


# ── Attendance Endpoints ──
@app.post("/api/attendance", response_model=AttendanceResponse)
async def create_attendance(attendance: AttendanceCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        member = db.query(Member).filter(Member.id == attendance.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        if not attendance.check_in_time:
            attendance.check_in_time = datetime.utcnow().isoformat()
        new_att = Attendance(**attendance.model_dump())
        db.add(new_att)
        member.status = MemberStatusEnum.active
        db.commit()
        db.refresh(new_att)
        return new_att
    finally:
        db.close()


@app.get("/api/attendance", response_model=List[AttendanceResponse])
async def list_attendance(
    member_id: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()
    try:
        query = db.query(Attendance).options(joinedload(Attendance.member))
        if member_id:
            query = query.filter(Attendance.member_id == member_id)
        if from_date:
            query = query.filter(Attendance.check_in_time >= from_date)
        if to_date:
            query = query.filter(Attendance.check_in_time <= to_date)
        return query.order_by(Attendance.check_in_time.desc()).all()
    finally:
        db.close()


@app.post("/api/attendance/{att_id}/check-out")
async def check_out(att_id: int, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        att = db.query(Attendance).filter(Attendance.id == att_id).first()
        if not att:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        att.check_out_time = datetime.utcnow()
        att.status = AttendStatusEnum.checked_out
        db.commit()
        return {"message": "Checked out successfully"}
    finally:
        db.close()


# ── Product Endpoints ──
@app.post("/api/products", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_product = Produc(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    finally:
        db.close()


@app.get("/api/products", response_model=List[ProductResponse])
async def list_products(category: Optional[str] = None, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        query = db.query(Produc)
        if category:
            query = query.filter(Produc.category == category)
        return query.filter(Produc.is_active == True).order_by(Produc.name).all()
    finally:
        db.close()


@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: dict, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        product = db.query(Produc).filter(Produc.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        for k, v in product_data.items():
            setattr(product, k, v)
        db.commit()
        db.refresh(product)
        return product
    finally:
        db.close()


# ── Supplier Endpoints ──
@app.post("/api/suppliers", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        new_supplier = Supplier(**supplier.model_dump())
        db.add(new_supplier)
        db.commit()
        db.refresh(new_supplier)
        return new_supplier
    finally:
        db.close()


@app.get("/api/suppliers", response_model=List[SupplierResponse])
async def list_suppliers(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        return db.query(Supplier).filter(Supplier.status == SupplierStatusEnum.active).order_by(Supplier.name).all()
    finally:
        db.close()


# ── Dashboard Stats ──
@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def dashboard_stats(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        total_members = db.query(Member).count()
        active_members = db.query(Member).filter(Member.status == MemberStatusEnum.active).count()
        new_members_this_month = db.query(Member).filter(
            Member.created_at >= month_start
        ).count()
        total_subscriptions = db.query(Subscription).count()
        active_subscriptions = db.query(Subscription).filter(
            Subscription.payment_status == PlanStatusEnum.paid
        ).count()
        total_revenue = db.query(Payment).filter(
            Payment.status == PaymentStatusEnum.completed
        ).with_entities(db.func.sum(Payment.amount)).scalar() or 0
        revenue_this_month = db.query(Payment).filter(
            Payment.status == PaymentStatusEnum.completed,
            Payment.payment_date >= month_start
        ).with_entities(db.func.sum(Payment.amount)).scalar() or 0
        pending_payments = db.query(Subscription).filter(
            Subscription.payment_status == PlanStatusEnum.pending
        ).count()
        overdue_payments = db.query(Subscription).filter(
            Subscription.payment_status == PlanStatusEnum.overdue
        ).count()
        total_trainers = db.query(Trainer).filter(Trainer.status == TrainerStatusEnum.active).count()
        total_classes = db.query(Class).filter(Class.is_active == True).count()
        today_attendance = db.query(Attendance).filter(
            db.func.date(Attendance.check_in_time) == date.today()
        ).count()
        equipment_count = db.query(Equipment).count()
        equipment_available = db.query(Equipment).filter(
            Equipment.status == EquipmentStatusEnum.available
        ).count()
        equipment_maintenance = db.query(Equipment).filter(
            Equipment.status == EquipmentStatusEnum.maintenance
        ).count()

        return DashboardStats(
            total_members=total_members,
            active_members=active_members,
            new_members_this_month=new_members_this_month,
            total_subscriptions=total_subscriptions,
            active_subscriptions=active_subscriptions,
            total_revenue=float(total_revenue),
            revenue_this_month=float(revenue_this_month),
            pending_payments=pending_payments,
            overdue_payments=overdue_payments,
            total_trainers=total_trainers,
            total_classes=total_classes,
            today_attendance=today_attendance,
            equipment_count=equipment_count,
            equipment_available=equipment_available,
            equipment_maintenance=equipment_maintenance,
        )
    finally:
        db.close()


# ── Initialize default data ──
def seed_default_data():
    db: Session = SessionLocal()
    try:
        # Create default admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                email="admin@takavar.com",
                role=UserRoleEnum.admin,
                status=UserStatusEnum.active,
            )
            db.add(admin)
            db.commit()
            print("Default admin user created: admin / admin123")

        # Create default subscription plans
        plans = db.query(SubscriptionPlan).all()
        if not plans:
            default_plans = [
                SubscriptionPlan(
                    name="برونزی",
                    description="پکیج مقدماتی برای اعضای جدید",
                    duration_days=30,
                    price=500000,
                    currency="IRT",
                    max_allowed_members=100,
                    included_features={"gym_access": True, "locker": True, "towel": False},
                    priority=1,
                ),
                SubscriptionPlan(
                    name="نقره‌ای",
                    description="پکیج پیشرفته با دسترسی‌های بیشتر",
                    duration_days=30,
                    price=800000,
                    currency="IRT",
                    max_allowed_members=50,
                    included_features={"gym_access": True, "locker": True, "towel": True, "sauna": True},
                    priority=2,
                ),
                SubscriptionPlan(
                    name="طلایی",
                    description="پکیج لوکس با بهترینVidائت‌ها",
                    duration_days=30,
                    price=1200000,
                    currency="IRT",
                    max_allowed_members=20,
                    included_features={"gym_access": True, "locker": True, "towel": True, "sauna": True, "personal_trainer": True},
                    priority=3,
                ),
                SubscriptionPlan(
                    name="VIP ویژه",
                    description="پکیج کمیته ویژه با تمامی Vorteile",
                    duration_days=30,
                    price=2000000,
                    currency="IRT",
                    max_allowed_members=5,
                    included_features={"gym_access": True, "locker": True, "towel": True, "sauna": True, "personal_trainer": True, "massage": True, "private_room": True},
                    priority=4,
                ),
                SubscriptionPlan(
                    name="س最低限度 ماهه",
                    description="برای تلاش‌های اولیه",
                    duration_days=30,
                    price=200000,
                    currency="IRT",
                    max_allowed_members=200,
                    included_features={"gym_access": True},
                    priority=0,
                ),
            ]
            for plan in default_plans:
                db.add(plan)
            db.commit()
            print(f"{len(default_plans)} default subscription plans created.")

        # Create default exercises
       exercises = db.query(Exercise).all()
        if not exams:
            default_exercises = [
                Exercise(name="پرس سینه", muscle_group=MuscleGroupEnum.chest, equipment_needed="پرس 망가토니"),
                Exercise(name="پرزilu-back", muscle_group=MuscleGroupEnum.back, equipment_needed="کابل"),
                Exercise(name="زبان فردا-دست", muscle_group=MuscleGroupEnum.shoulders),
                Exercise(name="करवत Triceps", muscle_group=MuscleGroupEnum.triceps),
                Exercise(name="خم شدن زانو", muscle_group=MuscleGroupEnum.legs, equipment_needed=" dumb_bel"),
                Exercise(name="Deadlift", muscle_group=MuscleGroupEnum.back, equipment_needed="بار"),
                Exercise(name="Bench Press", muscle_group=MuscleGroupEnum.chest, equipment_needed="بنس‏ پرسینگ"),
                Exercise(name="ت전극 زانو", muscle_group=MuscleGroupEnum.legs),
                Exercise(name="Cardio Treadmill", muscle_group=MuscleGroupEnum.cardio_muscle, equipment_needed="تترین"t"),
                Exercise(name="جیم باد الحاقی", muscle_group=MuscleGroupEnum.full_body),
                Exercise(name="Core Plank", muscle_group=MuscleGroupEnum.core),
                Exercise(name="Biceps Curl", muscle_group=MuscleGroupEnum.biceps, equipment_needed=" dumb_bel"),
                Exercise(name="Lat Pulldown", muscle_group=MuscleGroupEnum.back, equipment_needed="تجهیزات gravité"),
                Exercise(name="Leg Press", muscle_group=MuscleGroupEnum.legs, equipment_needed="Leg Press ماشین"),
                Exercise(name="Shoulder Press", muscle_group=MuscleGroupEnum.shoulders, equipment_needed=" dumb_bel"),
                Exercise(name="Triceps Pushdown", muscle_group=MuscleGroupEnum.triceps, equipment_needed="کابل"),
                Exercise(name="Romanian Deadlift", muscle_group=MuscleGroupEnum.back, equipment_needed="بار"),
                Exercise(name="Hammer Curl", muscle_group=MuscleGroupEnum.biceps, equipment_needed=" dumb_bel"),
                Exercise(name="Face Pull", muscle_group=MuscleGroupEnum.shoulders, equipment_needed="کابل"),
                Exercise(name="Dumbbell Row", muscle_group=MuscleGroupEnum.back, equipment_needed=" dumb_bel"),
                Exercise(name="Incline Bench Press", muscle_group=MuscleGroupEnum.chest, equipment_needed="بنس‏ پرسینگ"),
                Exercise(name="Leg Curl", muscle_group=MuscleGroupEnum.legs, equipment_needed="Leg Curl ماشین"),
                Exercise(name="Leg Extension", muscle_group=MuscleGroupEnum.legs, equipment_needed="Leg Extension ماشین"),
                Exercise(name="Calf Raise", muscle_group=MuscleGroupEnum.legs),
                Exercise(name="Oblique Crunch", muscle_group=MuscleGroupEnum.core),
                Exercise(name="Pull-ups", muscle_group=MuscleGroupEnum.back, equipment_needed="철봉"),
                Exercise(name="Dips", muscle_group=MuscleGroupEnum.chest, equipment_needed="تلكی دایپر"),
                Exercise(name="Cable Fly", muscle_group=MuscleGroupEnum.chest, equipment_needed="کابل"),
                Exercise(name="Seated Row", muscle_group=MuscleGroupEnum.back, equipment_needed="کابل"),
                Exercise(name="Upright Row", muscle_group=MuscleGroupEnum.shoulders, equipment_needed=" dumb_bel or بار"),
            ]
            for ex in default_exercises:
                db.add(ex)
            db.commit()
            print(f"{len(default_exercises)} default exercises created.")

        # Create default rooms
        rooms = db.query(Room).all()
        if not rooms:
            default_rooms = [
                Room(name="سالن اصلی بدنسازی", description="سالن اصلی با تجهیزات بدنسازی", capacity=50),
                Room(name="سالن کارودی", description="سالن کارودی با دوچرخه و میخک", capacity=30),
                Room(name="سالن یوگا و پیشنهاد", description="سالن یوگا و کلاس‌های سبک", capacity=20),
                Room(name="سالن شخصی‌سازی", description="سالن شخصی‌سازی با کارشناسان", capacity=5),
            ]
            for room in default_rooms:
                db.add(room)
            db.commit()
            print(f"{len(default_rooms)} default rooms created.")

        print("Database seeding completed.")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()


# ── Run ──
if __name__ == "__main__":
    seed_default_data()
    print(f"\n{'='*60}")
    print(" takavar Gym System Backend Server")
    print(f"{'='*60}")
    print(f" Database: {db_path_abs}")
    print(f" API Server: http://0.0.0.0:8000")
    print(f" API Docs: http://0.0.0.0:8000/docs")
    print(f" Default login: admin / admin123")
    print(f"{'='*60}\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# ── Response imports fix ──
from fastapi.responses import Response

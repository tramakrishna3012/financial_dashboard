from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum

# ----------------- User Schemas -----------------
class UserRole(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.viewer

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# ---------------- Record Schemas ----------------
class RecordBase(BaseModel):
    user_id: int
    amount: float
    type: str # 'income' or 'expense'
    category: str
    date: date # Pydantic will automatically parse and validate YYYY-MM-DD input
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordResponse(RecordBase):
    id: int

    class Config:
        from_attributes = True

# --------------- Dashboard Schemas --------------
class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_totals: dict

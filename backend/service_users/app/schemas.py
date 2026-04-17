from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional
from enum import Enum


# ==================== Enums ====================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    PARTNER = "partner"


class PartnerRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# ==================== Auth Schemas ====================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1)


class UserRegisterPartner(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    description: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class EmailVerify(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)


class EmailResend(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


# ==================== User Schemas ====================

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None


# ==================== Category Schemas ====================

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)


class CategoryResponse(BaseModel):
    id: int
    name: str
    is_custom: bool

    class Config:
        from_attributes = True


# ==================== Ad Schemas ====================

class AdCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    discount_percent: int = Field(..., ge=1, le=100)
    url: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    end_date: datetime
    category_ids: List[int] = Field(..., min_length=1)
    emodzi_id: Optional[int] = None
    prioritet: int = Field(default=0, ge=0)


class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percent: Optional[int] = Field(None, ge=1, le=100)
    url: Optional[str] = None
    address: Optional[str] = None
    end_date: Optional[datetime] = None
    category_ids: Optional[List[int]] = None
    emodzi_id: Optional[int] = None
    prioritet: Optional[int] = Field(None, ge=0)


class AdResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    discount_percent: int
    url: str
    address: str
    end_date: datetime
    clicks_count: int
    partner_id: int
    partner_name: str
    categories: List[str]
    is_favorite: Optional[bool] = False
    emodzi_id: Optional[int]
    prioritet: int

    class Config:
        from_attributes = True


class AdDetailResponse(AdResponse):
    created_at: datetime
    updated_at: datetime


class AdListResponse(BaseModel):
    items: List[AdResponse]
    total: int
    page: int
    limit: int
    pages: int


# ==================== Favorite Schemas ====================

class FavoriteResponse(BaseModel):
    ad_id: int
    title: str
    discount_percent: int
    end_date: datetime
    partner_name: str

    class Config:
        from_attributes = True


class FavoriteListResponse(BaseModel):
    items: List[FavoriteResponse]
    total: int
    page: int
    limit: int


# ==================== Partner Schemas ====================

class PartnerResponse(BaseModel):
    id: int
    company_name: str
    description: Optional[str]
    logo_url: Optional[str]
    ads_count: int = 0

    class Config:
        from_attributes = True


class PartnerDetailResponse(PartnerResponse):
    email: EmailStr
    phone: str
    ads_limit: int
    created_at: datetime


class PartnerAdsResponse(BaseModel):
    items: List[AdResponse]
    total: int
    page: int
    limit: int
    pages: int
    ads_used: int
    ads_limit: int


# ==================== Partner Request Schemas ====================

class PartnerRequestCreate(BaseModel):
    company_name: str = Field(..., min_length=1)
    contact_person: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    description: Optional[str] = None


class PartnerRequestResponse(BaseModel):
    id: int
    company_name: str
    contact_person: str
    phone: str
    description: Optional[str]
    status: PartnerRequestStatus
    admin_comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PartnerRequestUpdate(BaseModel):
    status: PartnerRequestStatus
    admin_comment: Optional[str] = None


# ==================== Admin Schemas ====================

class AdminUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUserListResponse(BaseModel):
    items: List[AdminUserResponse]
    total: int
    page: int
    limit: int
    pages: int


class AdminUserRoleUpdate(BaseModel):
    role: UserRole


class AdminPartnerRequestListResponse(BaseModel):
    items: List[PartnerRequestResponse]
    total: int
    page: int
    limit: int
    pages: int


# ==================== Common Query Params ====================

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)


class AdFilterParams(PaginationParams):
    category: Optional[str] = None
    search: Optional[str] = None
    sort: Optional[str] = Field(None, pattern="^(newest|ending_soon|popular)$")
from pydantic import BaseModel, validator
from datetime import datetime
from typing import List
from uuid import UUID



class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str

    @validator('role')
    def validate_role(cls, v):
        allowed = ['engineer', 'manager', 'seo']
        if v not in allowed:
            raise ValueError(f'role must be one of: {allowed}')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    created_at: datetime
    updated_at: datetime

class LoginResponse(BaseModel):
    message: str
    token_type: str

class MessageResponse(BaseModel):
    message: str
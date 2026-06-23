from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from ..models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserVerifyOTP(BaseModel):
    email: EmailStr
    otp_code: str

class UserResponse(UserBase):
    uuid: UUID4
    role: UserRole
    is_verified: bool
    profile_pic_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
"""
User-related Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid

from app.models.user import EnglishLevel


class UserBase(BaseModel):
    """Base user schema."""
    name: str
    email: EmailStr
    english_level: EnglishLevel
    bio: Optional[str] = None
    goals: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    english_level: Optional[EnglishLevel] = None
    bio: Optional[str] = None
    goals: Optional[str] = None
    fcm_token: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip() if v else v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: uuid.UUID
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenData(BaseModel):
    """Token data schema for JWT payload."""
    user_id: Optional[str] = None
    email: Optional[str] = None


class OAuthUserCreate(BaseModel):
    """Schema for OAuth user creation."""
    name: str
    email: EmailStr
    avatar_url: Optional[str] = None
    google_id: Optional[str] = None
    facebook_id: Optional[str] = None
    english_level: EnglishLevel = EnglishLevel.BEGINNER


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

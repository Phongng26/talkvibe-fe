"""
Translation-related Pydantic schemas.
"""
from pydantic import BaseModel, validator
from typing import Optional, Dict, List
from datetime import datetime
import uuid


class TranslationResponse(BaseModel):
    """Schema for translation response."""
    id: uuid.UUID
    language_code: str
    key: str
    value: str
    context: Optional[str] = None
    category: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TranslationCreate(BaseModel):
    """Schema for creating translations (admin use)."""
    language_code: str
    key: str
    value: str
    context: Optional[str] = None
    category: Optional[str] = None
    
    @validator('language_code')
    def validate_language_code(cls, v):
        # Basic validation for language codes (ISO 639-1)
        if len(v) < 2 or len(v) > 10:
            raise ValueError('Language code must be between 2 and 10 characters')
        return v.lower()
    
    @validator('key')
    def validate_key(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('Translation key cannot be empty')
        return v.strip()
    
    @validator('value')
    def validate_value(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('Translation value cannot be empty')
        return v


class TranslationUpdate(BaseModel):
    """Schema for updating translations."""
    value: Optional[str] = None
    context: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('value')
    def validate_value(cls, v):
        if v is not None and len(v.strip()) < 1:
            raise ValueError('Translation value cannot be empty')
        return v


class TranslationBulkCreate(BaseModel):
    """Schema for bulk creating translations."""
    language_code: str
    translations: Dict[str, str]  # key -> value mapping
    context: Optional[str] = None
    category: Optional[str] = None
    
    @validator('language_code')
    def validate_language_code(cls, v):
        if len(v) < 2 or len(v) > 10:
            raise ValueError('Language code must be between 2 and 10 characters')
        return v.lower()
    
    @validator('translations')
    def validate_translations(cls, v):
        if not v:
            raise ValueError('Translations dictionary cannot be empty')
        for key, value in v.items():
            if not key.strip():
                raise ValueError('Translation keys cannot be empty')
            if not value.strip():
                raise ValueError('Translation values cannot be empty')
        return v


class ContentResponse(BaseModel):
    """Schema for content response by language."""
    language_code: str
    content: Dict[str, str]  # key -> value mapping
    categories: Dict[str, Dict[str, str]]  # category -> {key -> value}


class LanguageList(BaseModel):
    """Schema for available languages."""
    languages: List[Dict[str, str]]  # [{"code": "en", "name": "English"}, ...]

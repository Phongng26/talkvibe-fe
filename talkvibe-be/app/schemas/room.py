"""
Room-related Pydantic schemas.
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.user import EnglishLevel


class RoomBase(BaseModel):
    """Base room schema."""
    name: str
    topic: str
    description: Optional[str] = None
    max_participants: int = 4
    is_public: bool = True
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Room name must be at least 3 characters long')
        return v.strip()
    
    @validator('topic')
    def validate_topic(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Topic must be at least 3 characters long')
        return v.strip()
    
    @validator('max_participants')
    def validate_max_participants(cls, v):
        if v < 2 or v > 10:
            raise ValueError('Max participants must be between 2 and 10')
        return v


class RoomCreate(RoomBase):
    """Schema for room creation."""
    allow_recording: bool = False
    require_approval: bool = False
    english_level_filter: Optional[EnglishLevel] = None


class RoomUpdate(BaseModel):
    """Schema for room updates."""
    name: Optional[str] = None
    topic: Optional[str] = None
    description: Optional[str] = None
    max_participants: Optional[int] = None
    is_public: Optional[bool] = None
    allow_recording: Optional[bool] = None
    require_approval: Optional[bool] = None
    english_level_filter: Optional[EnglishLevel] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError('Room name must be at least 3 characters long')
        return v.strip() if v else v
    
    @validator('topic')
    def validate_topic(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError('Topic must be at least 3 characters long')
        return v.strip() if v else v
    
    @validator('max_participants')
    def validate_max_participants(cls, v):
        if v is not None and (v < 2 or v > 10):
            raise ValueError('Max participants must be between 2 and 10')
        return v


class RoomResponse(RoomBase):
    """Schema for room response."""
    id: uuid.UUID
    creator_id: uuid.UUID
    participant_ids: List[uuid.UUID]
    participant_count: int
    is_active: bool
    is_full: bool
    is_joinable: bool
    allow_recording: bool
    require_approval: bool
    english_level_filter: Optional[EnglishLevel] = None
    session_id: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RoomJoin(BaseModel):
    """Schema for joining a room."""
    pass  # No additional fields needed, user ID comes from JWT


class RoomLeave(BaseModel):
    """Schema for leaving a room."""
    pass  # No additional fields needed, user ID comes from JWT


class RoomControls(BaseModel):
    """Schema for room media controls."""
    microphone_enabled: bool
    camera_enabled: bool


class RoomFilter(BaseModel):
    """Schema for room filtering."""
    is_public: Optional[bool] = None
    topic: Optional[str] = None
    english_level: Optional[EnglishLevel] = None
    creator_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = True
    
    # Pagination
    skip: int = 0
    limit: int = 20
    
    @validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Limit cannot exceed 100')
        return v


class RoomSearch(BaseModel):
    """Schema for room search."""
    query: str
    filters: Optional[RoomFilter] = None
    
    @validator('query')
    def validate_query(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Search query must be at least 2 characters long')
        return v.strip()

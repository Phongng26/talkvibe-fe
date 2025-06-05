"""
Session-related Pydantic schemas.
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import uuid


class SessionResponse(BaseModel):
    """Schema for session response."""
    id: uuid.UUID
    room_id: uuid.UUID
    user_ids: List[uuid.UUID]
    topic: str
    duration: int  # in minutes
    room_name: str
    participant_count: int
    notes: Optional[str] = None
    audio_quality: Optional[int] = None
    video_quality: Optional[int] = None
    overall_rating: Optional[int] = None
    date: datetime
    started_at: datetime
    ended_at: datetime
    
    class Config:
        from_attributes = True


class SessionStats(BaseModel):
    """Schema for user session statistics."""
    total_sessions: int
    total_hours: float
    average_session_duration: float
    favorite_topics: List[str]
    recent_sessions: List[SessionResponse]
    monthly_hours: List[dict]  # [{month: "2024-01", hours: 15.5}, ...]


class SessionCreate(BaseModel):
    """Schema for creating a session (internal use)."""
    room_id: uuid.UUID
    user_ids: List[uuid.UUID]
    topic: str
    room_name: str
    started_at: datetime
    ended_at: datetime
    
    @validator('ended_at')
    def validate_end_time(cls, v, values):
        if 'started_at' in values and v <= values['started_at']:
            raise ValueError('End time must be after start time')
        return v


class SessionFilter(BaseModel):
    """Schema for session filtering."""
    user_id: Optional[uuid.UUID] = None
    room_id: Optional[uuid.UUID] = None
    topic: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    
    # Pagination
    skip: int = 0
    limit: int = 20
    
    @validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Limit cannot exceed 100')
        return v


class SessionRating(BaseModel):
    """Schema for rating a session."""
    session_id: uuid.UUID
    audio_quality: Optional[int] = None
    video_quality: Optional[int] = None
    overall_rating: Optional[int] = None
    notes: Optional[str] = None
    
    @validator('audio_quality', 'video_quality', 'overall_rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

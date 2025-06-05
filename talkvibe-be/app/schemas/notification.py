"""
Notification-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.notification import NotificationType


class NotificationResponse(BaseModel):
    """Schema for notification response."""
    id: uuid.UUID
    user_id: uuid.UUID
    type: NotificationType
    title: str
    message: str
    room_id: Optional[uuid.UUID] = None
    sender_id: Optional[uuid.UUID] = None
    is_read: bool
    is_sent: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class NotificationMarkRead(BaseModel):
    """Schema for marking notifications as read."""
    notification_ids: List[uuid.UUID]


class NotificationCreate(BaseModel):
    """Schema for creating notifications (internal use)."""
    user_id: uuid.UUID
    type: NotificationType
    title: str
    message: str
    room_id: Optional[uuid.UUID] = None
    sender_id: Optional[uuid.UUID] = None


class NotificationFilter(BaseModel):
    """Schema for notification filtering."""
    is_read: Optional[bool] = None
    type: Optional[NotificationType] = None
    
    # Pagination
    skip: int = 0
    limit: int = 50
    
    @validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Limit cannot exceed 100')
        return v

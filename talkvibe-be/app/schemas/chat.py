"""
Chat-related Pydantic schemas.
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import uuid

from app.models.chat import MessageType


class ChatBase(BaseModel):
    """Base chat schema."""
    message: str
    message_type: MessageType = MessageType.TEXT
    
    @validator('message')
    def validate_message(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:
            raise ValueError('Message cannot exceed 2000 characters')
        return v.strip()


class ChatCreate(ChatBase):
    """Schema for creating a chat message."""
    room_id: uuid.UUID
    reply_to_id: Optional[uuid.UUID] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[str] = None


class ChatUpdate(BaseModel):
    """Schema for updating a chat message."""
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:
            raise ValueError('Message cannot exceed 2000 characters')
        return v.strip()


class ChatResponse(ChatBase):
    """Schema for chat response."""
    id: uuid.UUID
    room_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[str] = None
    is_edited: bool
    is_deleted: bool
    reply_to_id: Optional[uuid.UUID] = None
    timestamp: datetime
    edited_at: Optional[datetime] = None
    
    # User information (joined from user table)
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChatFilter(BaseModel):
    """Schema for chat filtering."""
    room_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    message_type: Optional[MessageType] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    
    # Pagination
    skip: int = 0
    limit: int = 50
    
    @validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Limit cannot exceed 100')
        return v


class ChatDelete(BaseModel):
    """Schema for deleting a chat message."""
    message_id: uuid.UUID


class FileUpload(BaseModel):
    """Schema for file upload metadata."""
    file_name: str
    file_size: int
    content_type: str
    
    @validator('file_size')
    def validate_file_size(cls, v):
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError(f'File size cannot exceed {max_size} bytes')
        return v
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif', 'image/webp',
            'application/pdf', 'text/plain', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        if v not in allowed_types:
            raise ValueError(f'Content type {v} is not allowed')
        return v

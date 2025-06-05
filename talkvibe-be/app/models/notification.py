"""
Notification model for TalkVibe application.
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class NotificationType(str, enum.Enum):
    """Notification types."""
    ROOM_INVITE = "room_invite"
    NEW_MESSAGE = "new_message"
    ROOM_STARTED = "room_started"
    ROOM_ENDED = "room_ended"
    SYSTEM_UPDATE = "system_update"
    FRIEND_REQUEST = "friend_request"
    ACHIEVEMENT = "achievement"


class Notification(Base):
    """Notification model."""
    
    __tablename__ = "notifications"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    type = Column(
        Enum(NotificationType),
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Optional data for specific notification types
    room_id = Column(UUID(as_uuid=True), nullable=True)
    sender_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Notification state
    is_read = Column(Boolean, nullable=False, default=False, index=True)
    is_sent = Column(Boolean, nullable=False, default=False)
    
    # FCM specific data
    fcm_message_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    read_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type})>"

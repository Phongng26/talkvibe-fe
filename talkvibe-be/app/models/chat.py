"""
Chat model for TalkVibe application.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class MessageType(str, enum.Enum):
    """Message types."""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    EMOJI = "emoji"


class Chat(Base):
    """Chat message model."""
    
    __tablename__ = "chats"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    room_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,  # Nullable for system messages
        index=True
    )
    
    # Message content
    message = Column(Text, nullable=False)
    message_type = Column(
        Enum(MessageType),
        nullable=False,
        default=MessageType.TEXT
    )
    
    # File/media information (for non-text messages)
    file_url = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(String(50), nullable=True)
    
    # Message metadata
    is_edited = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    
    # Reply functionality
    reply_to_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chats.id"),
        nullable=True
    )
    
    # Timestamps
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    edited_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Chat(id={self.id}, room_id={self.room_id}, user_id={self.user_id})>"

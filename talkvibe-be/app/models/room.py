"""
Room model for TalkVibe application.
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Room(Base):
    """Practice room model."""
    
    __tablename__ = "rooms"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    max_participants = Column(Integer, nullable=False, default=4)
    is_public = Column(Boolean, nullable=False, default=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Creator and participants
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    participant_ids = Column(
        ARRAY(UUID(as_uuid=True)),
        nullable=False,
        default=list
    )
    
    # Room settings
    allow_recording = Column(Boolean, nullable=False, default=False)
    require_approval = Column(Boolean, nullable=False, default=False)
    english_level_filter = Column(String(20), nullable=True)  # Optional level filter
    
    # WebRTC session info
    session_id = Column(String(100), nullable=True)  # Current active session
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}, topic={self.topic})>"
    
    @property
    def participant_count(self):
        """Get current number of participants."""
        return len(self.participant_ids) if self.participant_ids else 0
    
    @property
    def is_full(self):
        """Check if room is at capacity."""
        return self.participant_count >= self.max_participants
    
    @property
    def is_joinable(self):
        """Check if room can be joined."""
        return self.is_active and not self.is_full

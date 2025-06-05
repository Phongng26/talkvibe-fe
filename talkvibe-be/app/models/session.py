"""
Session model for TalkVibe application.
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Session(Base):
    """Practice session model for tracking user activity."""
    
    __tablename__ = "sessions"
    
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
    user_ids = Column(
        ARRAY(UUID(as_uuid=True)),
        nullable=False
    )
    
    # Session details
    topic = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False, default=0)  # Duration in minutes
    
    # Session metadata
    room_name = Column(String(100), nullable=False)
    participant_count = Column(Integer, nullable=False)
    
    # Optional session notes or summary
    notes = Column(Text, nullable=True)
    
    # Quality metrics (optional)
    audio_quality = Column(Integer, nullable=True)  # 1-5 rating
    video_quality = Column(Integer, nullable=True)  # 1-5 rating
    overall_rating = Column(Integer, nullable=True)  # 1-5 rating
    
    # Timestamps
    date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self):
        return f"<Session(id={self.id}, room_id={self.room_id}, duration={self.duration})>"

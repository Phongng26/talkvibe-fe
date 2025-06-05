"""
User model for TalkVibe application.
"""
from sqlalchemy import Column, String, Text, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class EnglishLevel(str, enum.Enum):
    """English proficiency levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    avatar_url = Column(String(500), nullable=True)
    english_level = Column(
        Enum(EnglishLevel),
        nullable=False,
        default=EnglishLevel.BEGINNER
    )
    bio = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # OAuth fields
    google_id = Column(String(100), nullable=True, unique=True)
    facebook_id = Column(String(100), nullable=True, unique=True)
    
    # FCM token for notifications
    fcm_token = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"

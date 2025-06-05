"""
Translation model for TalkVibe application.
"""
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Translation(Base):
    """Translation model for multilingual support."""
    
    __tablename__ = "translations"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    language_code = Column(String(10), nullable=False, index=True)  # e.g., 'en', 'vi', 'es'
    key = Column(String(200), nullable=False, index=True)  # Translation key
    value = Column(Text, nullable=False)  # Translated text
    
    # Optional context and category
    context = Column(String(100), nullable=True)  # e.g., 'notifications', 'ui', 'errors'
    category = Column(String(50), nullable=True)  # e.g., 'buttons', 'messages', 'labels'
    
    # Metadata
    is_active = Column(String(10), nullable=False, default=True)
    
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
    
    # Composite index for efficient lookups
    __table_args__ = (
        Index('ix_translations_lang_key', 'language_code', 'key'),
    )
    
    def __repr__(self):
        return f"<Translation(language_code={self.language_code}, key={self.key})>"

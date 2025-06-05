"""
Translation API routes for TalkVibe application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import logging

from app.core.database import get_db
from app.schemas.translation import ContentResponse, LanguageList
from app.models.user import User
from app.utils.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{language_code}", response_model=ContentResponse)
async def get_content_by_language(
    language_code: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get translated content for a specific language.
    
    - **language_code**: Language code (e.g., 'en', 'vi', 'es')
    
    Returns all translations for the specified language organized by category.
    """
    # Implementation placeholder
    return {
        "language_code": language_code,
        "content": {
            "welcome_message": "Welcome to TalkVibe!",
            "login_button": "Login",
            "register_button": "Register"
        },
        "categories": {
            "ui": {
                "welcome_message": "Welcome to TalkVibe!",
                "login_button": "Login",
                "register_button": "Register"
            },
            "notifications": {
                "room_invite": "You've been invited to a room",
                "new_message": "New message received"
            }
        }
    }


@router.get("/languages", response_model=LanguageList)
async def get_available_languages(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of available languages.
    
    Returns list of supported language codes and names.
    """
    # Implementation placeholder
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "vi", "name": "Tiếng Việt"},
            {"code": "es", "name": "Español"},
            {"code": "fr", "name": "Français"},
            {"code": "de", "name": "Deutsch"},
            {"code": "ja", "name": "日本語"},
            {"code": "ko", "name": "한국어"},
            {"code": "zh", "name": "中文"}
        ]
    }

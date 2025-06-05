"""
Translation service for TalkVibe application.
"""
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import logging

from app.models.translation import Translation
from app.schemas.translation import TranslationCreate, TranslationBulkCreate

logger = logging.getLogger(__name__)


class TranslationService:
    """Service class for translation operations."""
    
    @staticmethod
    async def get_content_by_language(
        db: AsyncSession,
        language_code: str
    ) -> Dict[str, any]:
        """Get all translations for a specific language."""
        try:
            stmt = select(Translation).where(
                and_(
                    Translation.language_code == language_code.lower(),
                    Translation.is_active == True
                )
            )
            
            result = await db.execute(stmt)
            translations = result.scalars().all()
            
            # Organize translations
            content = {}
            categories = {}
            
            for translation in translations:
                # Add to general content
                content[translation.key] = translation.value
                
                # Add to categories if category is specified
                if translation.category:
                    if translation.category not in categories:
                        categories[translation.category] = {}
                    categories[translation.category][translation.key] = translation.value
            
            return {
                "language_code": language_code,
                "content": content,
                "categories": categories
            }
            
        except Exception as e:
            logger.error(f"Error getting content by language: {e}")
            return {
                "language_code": language_code,
                "content": {},
                "categories": {}
            }
    
    @staticmethod
    async def get_available_languages(db: AsyncSession) -> List[Dict[str, str]]:
        """Get list of available languages."""
        try:
            # Get distinct language codes
            stmt = select(Translation.language_code).distinct()
            result = await db.execute(stmt)
            language_codes = result.scalars().all()
            
            # Language code to name mapping
            language_names = {
                "en": "English",
                "vi": "Tiếng Việt",
                "es": "Español",
                "fr": "Français",
                "de": "Deutsch",
                "ja": "日本語",
                "ko": "한국어",
                "zh": "中文",
                "pt": "Português",
                "it": "Italiano",
                "ru": "Русский",
                "ar": "العربية",
                "hi": "हिन्दी",
                "th": "ไทย"
            }
            
            languages = []
            for code in language_codes:
                languages.append({
                    "code": code,
                    "name": language_names.get(code, code.upper())
                })
            
            # Sort by name
            languages.sort(key=lambda x: x["name"])
            
            return languages
            
        except Exception as e:
            logger.error(f"Error getting available languages: {e}")
            return []
    
    @staticmethod
    async def create_translation(
        db: AsyncSession,
        translation_data: TranslationCreate
    ) -> Optional[Translation]:
        """Create a new translation."""
        try:
            # Check if translation already exists
            existing = await TranslationService.get_translation(
                db, translation_data.language_code, translation_data.key
            )
            
            if existing:
                logger.warning(f"Translation already exists: {translation_data.language_code}.{translation_data.key}")
                return None
            
            db_translation = Translation(
                language_code=translation_data.language_code.lower(),
                key=translation_data.key,
                value=translation_data.value,
                context=translation_data.context,
                category=translation_data.category
            )
            
            db.add(db_translation)
            await db.commit()
            await db.refresh(db_translation)
            
            logger.info(f"Translation created: {translation_data.language_code}.{translation_data.key}")
            return db_translation
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating translation: {e}")
            return None
    
    @staticmethod
    async def bulk_create_translations(
        db: AsyncSession,
        bulk_data: TranslationBulkCreate
    ) -> int:
        """Create multiple translations at once."""
        try:
            created_count = 0
            
            for key, value in bulk_data.translations.items():
                # Check if translation already exists
                existing = await TranslationService.get_translation(
                    db, bulk_data.language_code, key
                )
                
                if existing:
                    logger.debug(f"Translation already exists, skipping: {bulk_data.language_code}.{key}")
                    continue
                
                db_translation = Translation(
                    language_code=bulk_data.language_code.lower(),
                    key=key,
                    value=value,
                    context=bulk_data.context,
                    category=bulk_data.category
                )
                
                db.add(db_translation)
                created_count += 1
            
            await db.commit()
            
            logger.info(f"Bulk created {created_count} translations for {bulk_data.language_code}")
            return created_count
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error bulk creating translations: {e}")
            return 0
    
    @staticmethod
    async def get_translation(
        db: AsyncSession,
        language_code: str,
        key: str
    ) -> Optional[Translation]:
        """Get a specific translation."""
        try:
            stmt = select(Translation).where(
                and_(
                    Translation.language_code == language_code.lower(),
                    Translation.key == key
                )
            )
            
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Error getting translation: {e}")
            return None
    
    @staticmethod
    async def update_translation(
        db: AsyncSession,
        language_code: str,
        key: str,
        new_value: str
    ) -> Optional[Translation]:
        """Update a translation value."""
        try:
            translation = await TranslationService.get_translation(db, language_code, key)
            if not translation:
                return None
            
            translation.value = new_value
            await db.commit()
            await db.refresh(translation)
            
            logger.info(f"Translation updated: {language_code}.{key}")
            return translation
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating translation: {e}")
            return None
    
    @staticmethod
    async def delete_translation(
        db: AsyncSession,
        language_code: str,
        key: str
    ) -> bool:
        """Delete a translation."""
        try:
            translation = await TranslationService.get_translation(db, language_code, key)
            if not translation:
                return False
            
            await db.delete(translation)
            await db.commit()
            
            logger.info(f"Translation deleted: {language_code}.{key}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting translation: {e}")
            return False
    
    @staticmethod
    async def seed_default_translations(db: AsyncSession) -> int:
        """Seed database with default translations."""
        try:
            default_translations = {
                "en": {
                    # UI Elements
                    "welcome_message": "Welcome to TalkVibe!",
                    "login_button": "Login",
                    "register_button": "Register",
                    "logout_button": "Logout",
                    "profile_button": "Profile",
                    "settings_button": "Settings",
                    "create_room_button": "Create Room",
                    "join_room_button": "Join Room",
                    "leave_room_button": "Leave Room",
                    
                    # Notifications
                    "room_invite_title": "Room Invitation",
                    "room_invite_message": "You've been invited to join a room",
                    "new_message_title": "New Message",
                    "room_started_title": "Room Started",
                    "room_started_message": "Your practice room has started",
                    
                    # Errors
                    "error_invalid_credentials": "Invalid email or password",
                    "error_room_full": "Room is full",
                    "error_room_not_found": "Room not found",
                    "error_permission_denied": "Permission denied",
                    
                    # Success Messages
                    "success_room_created": "Room created successfully",
                    "success_room_joined": "Joined room successfully",
                    "success_profile_updated": "Profile updated successfully"
                },
                "vi": {
                    # UI Elements
                    "welcome_message": "Chào mừng đến với TalkVibe!",
                    "login_button": "Đăng nhập",
                    "register_button": "Đăng ký",
                    "logout_button": "Đăng xuất",
                    "profile_button": "Hồ sơ",
                    "settings_button": "Cài đặt",
                    "create_room_button": "Tạo phòng",
                    "join_room_button": "Tham gia phòng",
                    "leave_room_button": "Rời phòng",
                    
                    # Notifications
                    "room_invite_title": "Lời mời tham gia phòng",
                    "room_invite_message": "Bạn được mời tham gia một phòng",
                    "new_message_title": "Tin nhắn mới",
                    "room_started_title": "Phòng đã bắt đầu",
                    "room_started_message": "Phòng luyện tập của bạn đã bắt đầu"
                }
            }
            
            total_created = 0
            
            for lang_code, translations in default_translations.items():
                bulk_data = TranslationBulkCreate(
                    language_code=lang_code,
                    translations=translations,
                    category="default"
                )
                
                created = await TranslationService.bulk_create_translations(db, bulk_data)
                total_created += created
            
            logger.info(f"Seeded {total_created} default translations")
            return total_created
            
        except Exception as e:
            logger.error(f"Error seeding default translations: {e}")
            return 0

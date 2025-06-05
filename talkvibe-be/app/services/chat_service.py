"""
Chat service for TalkVibe application.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, desc
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import logging
import uuid

from app.models.chat import Chat, MessageType
from app.models.room import Room
from app.models.user import User
from app.schemas.chat import ChatCreate
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class ChatService:
    """Service class for chat-related operations."""
    
    @staticmethod
    async def send_message(
        db: AsyncSession, 
        chat_data: ChatCreate, 
        user_id: str
    ) -> Optional[Chat]:
        """Send a chat message to a room."""
        try:
            # Verify user is in the room
            room = await db.get(Room, chat_data.room_id)
            if not room:
                logger.warning(f"User {user_id} attempted to send message to non-existent room {chat_data.room_id}")
                return None
            
            user_uuid = uuid.UUID(user_id)
            if user_uuid not in room.participant_ids:
                logger.warning(f"User {user_id} attempted to send message to room {chat_data.room_id} without being a participant")
                return None
            
            # Create chat message
            db_chat = Chat(
                room_id=chat_data.room_id,
                user_id=user_id,
                message=chat_data.message,
                message_type=chat_data.message_type,
                reply_to_id=chat_data.reply_to_id,
                file_url=chat_data.file_url,
                file_name=chat_data.file_name,
                file_size=chat_data.file_size
            )
            
            db.add(db_chat)
            await db.commit()
            await db.refresh(db_chat)
            
            # Send notifications to other participants (for important messages)
            if chat_data.message_type == MessageType.TEXT and len(chat_data.message) > 10:
                notification_service = NotificationService()
                other_participants = [str(pid) for pid in room.participant_ids if str(pid) != user_id]
                
                if other_participants:
                    await notification_service.send_new_message_notification(
                        db, other_participants, str(room.id), room.name, user_id, chat_data.message
                    )
            
            logger.info(f"Message sent by user {user_id} in room {chat_data.room_id}")
            return db_chat
            
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Error sending message: {e}")
            return None
        except Exception as e:
            await db.rollback()
            logger.error(f"Unexpected error sending message: {e}")
            return None
    
    @staticmethod
    async def get_room_messages(
        db: AsyncSession,
        room_id: str,
        user_id: str,
        message_type: Optional[MessageType] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Chat]:
        """Get messages for a room."""
        try:
            # Verify user is in the room
            room = await db.get(Room, room_id)
            if not room:
                return []
            
            user_uuid = uuid.UUID(user_id)
            if user_uuid not in room.participant_ids:
                logger.warning(f"User {user_id} attempted to access messages for room {room_id} without being a participant")
                return []
            
            # Build query
            stmt = select(Chat).where(
                and_(
                    Chat.room_id == room_id,
                    Chat.is_deleted == False
                )
            )
            
            if message_type:
                stmt = stmt.where(Chat.message_type == message_type)
            
            # Order by timestamp (newest first for pagination, but reverse for display)
            stmt = stmt.order_by(desc(Chat.timestamp))
            stmt = stmt.offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            messages = result.scalars().all()
            
            # Reverse to show oldest first
            return list(reversed(messages))
            
        except Exception as e:
            logger.error(f"Error getting room messages: {e}")
            return []
    
    @staticmethod
    async def edit_message(
        db: AsyncSession,
        message_id: str,
        new_message: str,
        user_id: str
    ) -> Optional[Chat]:
        """Edit a chat message (only sender can edit)."""
        try:
            chat = await db.get(Chat, message_id)
            if not chat:
                return None
            
            # Check if user is the sender
            if str(chat.user_id) != user_id:
                logger.warning(f"User {user_id} attempted to edit message {message_id} without permission")
                return None
            
            # Check if message is not too old (e.g., 15 minutes)
            time_diff = datetime.now(timezone.utc) - chat.timestamp
            if time_diff.total_seconds() > 900:  # 15 minutes
                logger.warning(f"User {user_id} attempted to edit old message {message_id}")
                return None
            
            # Update message
            chat.message = new_message
            chat.is_edited = True
            chat.edited_at = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(chat)
            
            logger.info(f"Message {message_id} edited by user {user_id}")
            return chat
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error editing message: {e}")
            return None
    
    @staticmethod
    async def delete_message(
        db: AsyncSession,
        message_id: str,
        user_id: str
    ) -> bool:
        """Delete a chat message (only sender can delete)."""
        try:
            chat = await db.get(Chat, message_id)
            if not chat:
                return False
            
            # Check if user is the sender
            if str(chat.user_id) != user_id:
                logger.warning(f"User {user_id} attempted to delete message {message_id} without permission")
                return False
            
            # Soft delete
            chat.is_deleted = True
            chat.deleted_at = datetime.now(timezone.utc)
            chat.message = "[Message deleted]"
            
            await db.commit()
            
            logger.info(f"Message {message_id} deleted by user {user_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting message: {e}")
            return False
    
    @staticmethod
    async def get_message_with_user_info(db: AsyncSession, message_id: str) -> Optional[dict]:
        """Get message with user information."""
        try:
            # Join chat with user to get user info
            stmt = select(Chat, User).join(User, Chat.user_id == User.id).where(Chat.id == message_id)
            result = await db.execute(stmt)
            row = result.first()
            
            if not row:
                return None
            
            chat, user = row
            
            return {
                "id": chat.id,
                "room_id": chat.room_id,
                "user_id": chat.user_id,
                "message": chat.message,
                "message_type": chat.message_type,
                "file_url": chat.file_url,
                "file_name": chat.file_name,
                "file_size": chat.file_size,
                "is_edited": chat.is_edited,
                "is_deleted": chat.is_deleted,
                "reply_to_id": chat.reply_to_id,
                "timestamp": chat.timestamp,
                "edited_at": chat.edited_at,
                "user_name": user.name,
                "user_avatar": user.avatar_url
            }
            
        except Exception as e:
            logger.error(f"Error getting message with user info: {e}")
            return None
    
    @staticmethod
    async def get_room_messages_with_user_info(
        db: AsyncSession,
        room_id: str,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[dict]:
        """Get room messages with user information."""
        try:
            # Verify user is in the room
            room = await db.get(Room, room_id)
            if not room:
                return []
            
            user_uuid = uuid.UUID(user_id)
            if user_uuid not in room.participant_ids:
                return []
            
            # Join chat with user to get user info
            stmt = select(Chat, User).join(
                User, Chat.user_id == User.id, isouter=True
            ).where(
                and_(
                    Chat.room_id == room_id,
                    Chat.is_deleted == False
                )
            ).order_by(desc(Chat.timestamp)).offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            rows = result.all()
            
            messages = []
            for chat, user in reversed(rows):  # Reverse to show oldest first
                message_data = {
                    "id": chat.id,
                    "room_id": chat.room_id,
                    "user_id": chat.user_id,
                    "message": chat.message,
                    "message_type": chat.message_type,
                    "file_url": chat.file_url,
                    "file_name": chat.file_name,
                    "file_size": chat.file_size,
                    "is_edited": chat.is_edited,
                    "is_deleted": chat.is_deleted,
                    "reply_to_id": chat.reply_to_id,
                    "timestamp": chat.timestamp,
                    "edited_at": chat.edited_at,
                    "user_name": user.name if user else "Unknown User",
                    "user_avatar": user.avatar_url if user else None
                }
                messages.append(message_data)
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting room messages with user info: {e}")
            return []

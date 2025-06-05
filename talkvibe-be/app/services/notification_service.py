"""
Notification service for TalkVibe application.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone
import logging

from app.models.notification import Notification, NotificationType
from app.models.user import User
from app.schemas.notification import NotificationCreate
from app.core.config import settings

logger = logging.getLogger(__name__)

# Firebase imports (optional, install firebase-admin)
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logger.warning("Firebase not available. Install firebase-admin for FCM support.")


class NotificationService:
    """Service class for notification operations."""
    
    def __init__(self):
        self.firebase_app = None
        if FIREBASE_AVAILABLE and settings.FIREBASE_CREDENTIALS_PATH:
            try:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                self.firebase_app = firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {e}")
    
    async def create_notification(
        self,
        db: AsyncSession,
        notification_data: NotificationCreate
    ) -> Optional[Notification]:
        """Create a new notification."""
        try:
            db_notification = Notification(
                user_id=notification_data.user_id,
                type=notification_data.type,
                title=notification_data.title,
                message=notification_data.message,
                room_id=notification_data.room_id,
                sender_id=notification_data.sender_id
            )
            
            db.add(db_notification)
            await db.commit()
            await db.refresh(db_notification)
            
            # Send FCM notification
            await self._send_fcm_notification(db, db_notification)
            
            logger.info(f"Notification created: {db_notification.id}")
            return db_notification
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating notification: {e}")
            return None
    
    async def get_user_notifications(
        self,
        db: AsyncSession,
        user_id: str,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user."""
        try:
            stmt = select(Notification).where(Notification.user_id == user_id)
            
            if is_read is not None:
                stmt = stmt.where(Notification.is_read == is_read)
            
            stmt = stmt.order_by(Notification.created_at.desc())
            stmt = stmt.offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []
    
    async def mark_notifications_read(
        self,
        db: AsyncSession,
        user_id: str,
        notification_ids: List[str]
    ) -> bool:
        """Mark notifications as read."""
        try:
            stmt = update(Notification).where(
                Notification.user_id == user_id,
                Notification.id.in_(notification_ids)
            ).values(
                is_read=True,
                read_at=datetime.now(timezone.utc)
            )
            
            await db.execute(stmt)
            await db.commit()
            
            logger.info(f"Marked {len(notification_ids)} notifications as read for user {user_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error marking notifications as read: {e}")
            return False
    
    async def _send_fcm_notification(
        self,
        db: AsyncSession,
        notification: Notification
    ) -> bool:
        """Send FCM notification to user's device."""
        if not FIREBASE_AVAILABLE or not self.firebase_app:
            logger.warning("Firebase not available, skipping FCM notification")
            return False
        
        try:
            # Get user's FCM token
            user = await db.get(User, notification.user_id)
            if not user or not user.fcm_token:
                logger.warning(f"No FCM token for user {notification.user_id}")
                return False
            
            # Create FCM message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.message
                ),
                data={
                    "notification_id": str(notification.id),
                    "type": notification.type.value,
                    "room_id": str(notification.room_id) if notification.room_id else "",
                    "sender_id": str(notification.sender_id) if notification.sender_id else ""
                },
                token=user.fcm_token
            )
            
            # Send message
            response = messaging.send(message)
            
            # Update notification with FCM message ID
            notification.fcm_message_id = response
            notification.is_sent = True
            notification.sent_at = datetime.now(timezone.utc)
            await db.commit()
            
            logger.info(f"FCM notification sent: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending FCM notification: {e}")
            return False
    
    async def send_room_invite_notification(
        self,
        db: AsyncSession,
        user_id: str,
        room_id: str,
        room_name: str,
        sender_id: str
    ) -> Optional[Notification]:
        """Send room invite notification."""
        notification_data = NotificationCreate(
            user_id=user_id,
            type=NotificationType.ROOM_INVITE,
            title="Room Invitation",
            message=f"You've been invited to join '{room_name}'",
            room_id=room_id,
            sender_id=sender_id
        )
        
        return await self.create_notification(db, notification_data)
    
    async def send_room_started_notification(
        self,
        db: AsyncSession,
        user_ids: List[str],
        room_id: str,
        room_name: str
    ) -> List[Notification]:
        """Send room started notifications to participants."""
        notifications = []
        
        for user_id in user_ids:
            notification_data = NotificationCreate(
                user_id=user_id,
                type=NotificationType.ROOM_STARTED,
                title="Room Started",
                message=f"'{room_name}' has started",
                room_id=room_id
            )
            
            notification = await self.create_notification(db, notification_data)
            if notification:
                notifications.append(notification)
        
        return notifications
    
    async def send_new_message_notification(
        self,
        db: AsyncSession,
        user_ids: List[str],
        room_id: str,
        room_name: str,
        sender_id: str,
        message_preview: str
    ) -> List[Notification]:
        """Send new message notifications."""
        notifications = []
        
        for user_id in user_ids:
            if user_id == sender_id:  # Don't notify sender
                continue
                
            notification_data = NotificationCreate(
                user_id=user_id,
                type=NotificationType.NEW_MESSAGE,
                title=f"New message in {room_name}",
                message=message_preview[:100] + "..." if len(message_preview) > 100 else message_preview,
                room_id=room_id,
                sender_id=sender_id
            )
            
            notification = await self.create_notification(db, notification_data)
            if notification:
                notifications.append(notification)
        
        return notifications

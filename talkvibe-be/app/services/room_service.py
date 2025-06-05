"""
Room service for TalkVibe application.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import logging
import uuid

from app.models.room import Room
from app.models.user import User, EnglishLevel
from app.schemas.room import RoomCreate, RoomUpdate, RoomFilter
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class RoomService:
    """Service class for room-related operations."""
    
    @staticmethod
    async def create_room(db: AsyncSession, room_data: RoomCreate, creator_id: str) -> Optional[Room]:
        """Create a new practice room."""
        try:
            db_room = Room(
                name=room_data.name,
                topic=room_data.topic,
                description=room_data.description,
                max_participants=room_data.max_participants,
                is_public=room_data.is_public,
                creator_id=creator_id,
                participant_ids=[creator_id],  # Creator automatically joins
                allow_recording=room_data.allow_recording,
                require_approval=room_data.require_approval,
                english_level_filter=room_data.english_level_filter
            )
            
            db.add(db_room)
            await db.commit()
            await db.refresh(db_room)
            
            logger.info(f"Room created successfully: {db_room.name} by user {creator_id}")
            return db_room
            
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Error creating room: {e}")
            return None
        except Exception as e:
            await db.rollback()
            logger.error(f"Unexpected error creating room: {e}")
            return None
    
    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: str) -> Optional[Room]:
        """Get room by ID."""
        try:
            result = await db.execute(select(Room).where(Room.id == room_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting room by ID: {e}")
            return None
    
    @staticmethod
    async def update_room(
        db: AsyncSession, 
        room_id: str, 
        room_data: RoomUpdate, 
        user_id: str
    ) -> Optional[Room]:
        """Update room details (only creator can update)."""
        try:
            room = await RoomService.get_room_by_id(db, room_id)
            if not room:
                return None
            
            # Check if user is the creator
            if str(room.creator_id) != user_id:
                logger.warning(f"User {user_id} attempted to update room {room_id} without permission")
                return None
            
            # Update fields
            update_data = room_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(room, field, value)
            
            await db.commit()
            await db.refresh(room)
            
            logger.info(f"Room updated successfully: {room.name}")
            return room
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating room: {e}")
            return None
    
    @staticmethod
    async def delete_room(db: AsyncSession, room_id: str, user_id: str) -> bool:
        """Delete room (only creator can delete)."""
        try:
            room = await RoomService.get_room_by_id(db, room_id)
            if not room:
                return False
            
            # Check if user is the creator
            if str(room.creator_id) != user_id:
                logger.warning(f"User {user_id} attempted to delete room {room_id} without permission")
                return False
            
            await db.delete(room)
            await db.commit()
            
            logger.info(f"Room deleted successfully: {room.name}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting room: {e}")
            return False
    
    @staticmethod
    async def join_room(db: AsyncSession, room_id: str, user_id: str) -> Optional[Room]:
        """Join a practice room."""
        try:
            room = await RoomService.get_room_by_id(db, room_id)
            if not room:
                return None
            
            # Check if room is joinable
            if not room.is_joinable:
                logger.warning(f"User {user_id} attempted to join full/inactive room {room_id}")
                return None
            
            # Check if user is already in room
            if user_id in [str(pid) for pid in room.participant_ids]:
                logger.info(f"User {user_id} already in room {room_id}")
                return room
            
            # Add user to participants
            room.participant_ids = room.participant_ids + [uuid.UUID(user_id)]
            
            # Start room if this is the first join after creation
            if not room.started_at and len(room.participant_ids) > 1:
                room.started_at = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(room)
            
            # Send notifications to other participants
            notification_service = NotificationService()
            other_participants = [str(pid) for pid in room.participant_ids if str(pid) != user_id]
            
            if other_participants:
                await notification_service.send_room_started_notification(
                    db, other_participants, room_id, room.name
                )
            
            logger.info(f"User {user_id} joined room {room_id}")
            return room
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error joining room: {e}")
            return None
    
    @staticmethod
    async def leave_room(db: AsyncSession, room_id: str, user_id: str) -> Optional[Room]:
        """Leave a practice room."""
        try:
            room = await RoomService.get_room_by_id(db, room_id)
            if not room:
                return None
            
            # Check if user is in room
            user_uuid = uuid.UUID(user_id)
            if user_uuid not in room.participant_ids:
                logger.info(f"User {user_id} not in room {room_id}")
                return room
            
            # Remove user from participants
            room.participant_ids = [pid for pid in room.participant_ids if pid != user_uuid]
            
            # End room if no participants left or only creator remains
            if len(room.participant_ids) <= 1:
                room.ended_at = datetime.now(timezone.utc)
                room.is_active = False
            
            await db.commit()
            await db.refresh(room)
            
            logger.info(f"User {user_id} left room {room_id}")
            return room
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error leaving room: {e}")
            return None
    
    @staticmethod
    async def list_rooms(
        db: AsyncSession,
        filters: RoomFilter,
        user_id: Optional[str] = None
    ) -> List[Room]:
        """List rooms with filters."""
        try:
            stmt = select(Room)
            
            # Apply filters
            conditions = []
            
            if filters.is_public is not None:
                conditions.append(Room.is_public == filters.is_public)
            
            if filters.topic:
                conditions.append(Room.topic.ilike(f"%{filters.topic}%"))
            
            if filters.english_level:
                conditions.append(
                    or_(
                        Room.english_level_filter == filters.english_level,
                        Room.english_level_filter.is_(None)
                    )
                )
            
            if filters.creator_id:
                conditions.append(Room.creator_id == filters.creator_id)
            
            if filters.is_active is not None:
                conditions.append(Room.is_active == filters.is_active)
            
            # Only show public rooms or rooms user is part of
            if user_id and filters.is_public is not True:
                conditions.append(
                    or_(
                        Room.is_public == True,
                        Room.creator_id == user_id,
                        Room.participant_ids.contains([uuid.UUID(user_id)])
                    )
                )
            elif not user_id:
                conditions.append(Room.is_public == True)
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            # Order by creation date (newest first)
            stmt = stmt.order_by(Room.created_at.desc())
            
            # Apply pagination
            stmt = stmt.offset(filters.skip).limit(filters.limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error listing rooms: {e}")
            return []
    
    @staticmethod
    async def search_rooms(
        db: AsyncSession,
        query: str,
        english_level: Optional[EnglishLevel] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Room]:
        """Search rooms by name, topic, or description."""
        try:
            stmt = select(Room).where(
                and_(
                    Room.is_public == True,
                    Room.is_active == True,
                    or_(
                        Room.name.ilike(f"%{query}%"),
                        Room.topic.ilike(f"%{query}%"),
                        Room.description.ilike(f"%{query}%")
                    )
                )
            )
            
            if english_level:
                stmt = stmt.where(
                    or_(
                        Room.english_level_filter == english_level,
                        Room.english_level_filter.is_(None)
                    )
                )
            
            stmt = stmt.order_by(Room.created_at.desc())
            stmt = stmt.offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error searching rooms: {e}")
            return []

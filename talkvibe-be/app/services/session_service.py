"""
Session service for TalkVibe application.
"""
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, extract
from datetime import datetime, timezone
import logging
import uuid

from app.models.session import Session
from app.models.room import Room
from app.schemas.session import SessionCreate, SessionFilter, SessionStats

logger = logging.getLogger(__name__)


class SessionService:
    """Service class for session-related operations."""
    
    @staticmethod
    async def create_session(
        db: AsyncSession, 
        session_data: SessionCreate
    ) -> Optional[Session]:
        """Create a practice session record."""
        try:
            # Calculate duration in minutes
            duration = int((session_data.ended_at - session_data.started_at).total_seconds() / 60)
            
            db_session = Session(
                room_id=session_data.room_id,
                user_ids=session_data.user_ids,
                topic=session_data.topic,
                room_name=session_data.room_name,
                duration=duration,
                participant_count=len(session_data.user_ids),
                started_at=session_data.started_at,
                ended_at=session_data.ended_at
            )
            
            db.add(db_session)
            await db.commit()
            await db.refresh(db_session)
            
            logger.info(f"Session created: {db_session.id} for room {session_data.room_id}")
            return db_session
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating session: {e}")
            return None
    
    @staticmethod
    async def get_user_sessions(
        db: AsyncSession,
        user_id: str,
        filters: SessionFilter
    ) -> List[Session]:
        """Get user's practice sessions with filters."""
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Build query
            stmt = select(Session).where(
                Session.user_ids.contains([user_uuid])
            )
            
            # Apply filters
            if filters.room_id:
                stmt = stmt.where(Session.room_id == filters.room_id)
            
            if filters.topic:
                stmt = stmt.where(Session.topic.ilike(f"%{filters.topic}%"))
            
            if filters.date_from:
                stmt = stmt.where(Session.date >= filters.date_from)
            
            if filters.date_to:
                stmt = stmt.where(Session.date <= filters.date_to)
            
            # Order by date (newest first)
            stmt = stmt.order_by(Session.date.desc())
            
            # Apply pagination
            stmt = stmt.offset(filters.skip).limit(filters.limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            return []
    
    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: str) -> SessionStats:
        """Get user's practice statistics."""
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get all user sessions
            sessions_stmt = select(Session).where(
                Session.user_ids.contains([user_uuid])
            ).order_by(Session.date.desc())
            
            sessions_result = await db.execute(sessions_stmt)
            all_sessions = sessions_result.scalars().all()
            
            # Calculate basic stats
            total_sessions = len(all_sessions)
            total_minutes = sum(session.duration for session in all_sessions)
            total_hours = total_minutes / 60.0
            
            average_duration = total_minutes / total_sessions if total_sessions > 0 else 0.0
            
            # Get favorite topics
            topic_counts = {}
            for session in all_sessions:
                topic = session.topic
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            favorite_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            favorite_topics = [topic for topic, count in favorite_topics]
            
            # Get recent sessions (last 10)
            recent_sessions = all_sessions[:10]
            
            # Calculate monthly hours for the last 12 months
            monthly_hours = await SessionService._get_monthly_hours(db, user_id)
            
            return SessionStats(
                total_sessions=total_sessions,
                total_hours=total_hours,
                average_session_duration=average_duration,
                favorite_topics=favorite_topics,
                recent_sessions=recent_sessions,
                monthly_hours=monthly_hours
            )
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return SessionStats(
                total_sessions=0,
                total_hours=0.0,
                average_session_duration=0.0,
                favorite_topics=[],
                recent_sessions=[],
                monthly_hours=[]
            )
    
    @staticmethod
    async def _get_monthly_hours(db: AsyncSession, user_id: str) -> List[Dict]:
        """Get monthly practice hours for the last 12 months."""
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get sessions grouped by month
            stmt = select(
                extract('year', Session.date).label('year'),
                extract('month', Session.date).label('month'),
                func.sum(Session.duration).label('total_minutes')
            ).where(
                Session.user_ids.contains([user_uuid])
            ).group_by(
                extract('year', Session.date),
                extract('month', Session.date)
            ).order_by(
                extract('year', Session.date).desc(),
                extract('month', Session.date).desc()
            ).limit(12)
            
            result = await db.execute(stmt)
            rows = result.all()
            
            monthly_data = []
            for row in rows:
                year, month, total_minutes = row
                hours = (total_minutes or 0) / 60.0
                
                # Format as YYYY-MM
                month_str = f"{int(year)}-{int(month):02d}"
                
                monthly_data.append({
                    "month": month_str,
                    "hours": round(hours, 1)
                })
            
            # Reverse to show oldest first
            return list(reversed(monthly_data))
            
        except Exception as e:
            logger.error(f"Error getting monthly hours: {e}")
            return []
    
    @staticmethod
    async def rate_session(
        db: AsyncSession,
        session_id: str,
        user_id: str,
        audio_quality: Optional[int] = None,
        video_quality: Optional[int] = None,
        overall_rating: Optional[int] = None,
        notes: Optional[str] = None
    ) -> Optional[Session]:
        """Rate a practice session."""
        try:
            session = await db.get(Session, session_id)
            if not session:
                return None
            
            # Check if user was in the session
            user_uuid = uuid.UUID(user_id)
            if user_uuid not in session.user_ids:
                logger.warning(f"User {user_id} attempted to rate session {session_id} without participating")
                return None
            
            # Update ratings
            if audio_quality is not None:
                session.audio_quality = audio_quality
            
            if video_quality is not None:
                session.video_quality = video_quality
            
            if overall_rating is not None:
                session.overall_rating = overall_rating
            
            if notes is not None:
                session.notes = notes
            
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Session {session_id} rated by user {user_id}")
            return session
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error rating session: {e}")
            return None
    
    @staticmethod
    async def end_room_session(
        db: AsyncSession,
        room_id: str,
        participant_ids: List[str]
    ) -> Optional[Session]:
        """End a room session and create session record."""
        try:
            # Get room details
            room = await db.get(Room, room_id)
            if not room or not room.started_at:
                return None
            
            # Create session record
            session_data = SessionCreate(
                room_id=uuid.UUID(room_id),
                user_ids=[uuid.UUID(pid) for pid in participant_ids],
                topic=room.topic,
                room_name=room.name,
                started_at=room.started_at,
                ended_at=datetime.now(timezone.utc)
            )
            
            session = await SessionService.create_session(db, session_data)
            
            # Update room
            room.ended_at = datetime.now(timezone.utc)
            room.is_active = False
            room.session_id = None
            
            await db.commit()
            
            logger.info(f"Room session ended: {room_id}")
            return session
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error ending room session: {e}")
            return None

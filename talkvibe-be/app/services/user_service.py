"""
User service for TalkVibe application.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import logging

from app.models.user import User, EnglishLevel
from app.schemas.user import UserCreate, UserUpdate, OAuthUserCreate
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.core.config import settings

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> Optional[User]:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = await UserService.get_user_by_email(db, user_data.email)
            if existing_user:
                return None
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create user
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                hashed_password=hashed_password,
                english_level=user_data.english_level,
                bio=user_data.bio,
                goals=user_data.goals
            )
            
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            
            logger.info(f"User created successfully: {db_user.email}")
            return db_user
            
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Error creating user: {e}")
            return None
        except Exception as e:
            await db.rollback()
            logger.error(f"Unexpected error creating user: {e}")
            return None
    
    @staticmethod
    async def create_oauth_user(db: AsyncSession, user_data: OAuthUserCreate) -> Optional[User]:
        """Create a new OAuth user."""
        try:
            # Check if user already exists
            existing_user = await UserService.get_user_by_email(db, user_data.email)
            if existing_user:
                # Update OAuth IDs if user exists
                if user_data.google_id:
                    existing_user.google_id = user_data.google_id
                if user_data.facebook_id:
                    existing_user.facebook_id = user_data.facebook_id
                if user_data.avatar_url:
                    existing_user.avatar_url = user_data.avatar_url
                
                await db.commit()
                return existing_user
            
            # Create new OAuth user
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                avatar_url=user_data.avatar_url,
                english_level=user_data.english_level,
                google_id=user_data.google_id,
                facebook_id=user_data.facebook_id,
                is_verified=True  # OAuth users are pre-verified
            )
            
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            
            logger.info(f"OAuth user created successfully: {db_user.email}")
            return db_user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating OAuth user: {e}")
            return None
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = await UserService.get_user_by_email(db, email)
            if not user or not user.hashed_password:
                return None
            
            if not verify_password(password, user.hashed_password):
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            await db.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            result = await db.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user profile."""
        try:
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # Update fields
            update_data = user_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"User updated successfully: {user.email}")
            return user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating user: {e}")
            return None
    
    @staticmethod
    async def search_users(
        db: AsyncSession,
        query: str,
        english_level: Optional[EnglishLevel] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[User]:
        """Search users by name or interests."""
        try:
            stmt = select(User).where(User.is_active == True)
            
            # Add search filters
            if query:
                stmt = stmt.where(
                    User.name.ilike(f"%{query}%") |
                    User.bio.ilike(f"%{query}%") |
                    User.goals.ilike(f"%{query}%")
                )
            
            if english_level:
                stmt = stmt.where(User.english_level == english_level)
            
            stmt = stmt.offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return []
    
    @staticmethod
    async def create_access_token_for_user(user: User) -> dict:
        """Create access token for user."""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user
        }

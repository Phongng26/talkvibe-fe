"""
User API routes for TalkVibe application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, Token, OAuthUserCreate
)
from app.schemas.user import EnglishLevel
from app.services.user_service import UserService
from app.utils.auth import get_current_active_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - **name**: User's full name
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    - **english_level**: beginner, intermediate, or advanced
    - **bio**: Optional user biography
    - **goals**: Optional learning goals
    """
    try:
        # Check if user already exists
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = await UserService.create_user(db, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        logger.info(f"User registered successfully: {user.email}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=Token)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns JWT access token for authenticated requests.
    """
    try:
        # Authenticate user
        user = await UserService.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Create access token
        token_data = await UserService.create_access_token_for_user(user)
        
        logger.info(f"User logged in successfully: {user.email}")
        return token_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout user (invalidate token on client side).
    
    Note: JWT tokens are stateless, so logout is handled client-side.
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile.
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user profile.
    
    - **name**: Updated name
    - **avatar_url**: Profile picture URL
    - **english_level**: Updated English level
    - **bio**: Updated biography
    - **goals**: Updated learning goals
    - **fcm_token**: Firebase Cloud Messaging token for notifications
    """
    try:
        updated_user = await UserService.update_user(db, str(current_user.id), user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update profile"
            )
        
        logger.info(f"User profile updated: {updated_user.email}")
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/search", response_model=List[UserResponse])
async def search_users(
    query: str,
    english_level: Optional[EnglishLevel] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Search users by name, bio, or goals.
    
    - **query**: Search term
    - **english_level**: Filter by English level
    - **skip**: Number of results to skip (pagination)
    - **limit**: Maximum number of results (max 100)
    """
    try:
        if limit > 100:
            limit = 100
        
        users = await UserService.search_users(db, query, english_level, skip, limit)
        
        # Remove current user from results
        users = [user for user in users if user.id != current_user.id]
        
        return users
        
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

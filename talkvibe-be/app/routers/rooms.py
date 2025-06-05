"""
Room API routes for TalkVibe application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.core.database import get_db
from app.schemas.room import (
    RoomCreate, RoomUpdate, RoomResponse, RoomFilter, RoomSearch
)
from app.models.user import User, EnglishLevel
from app.utils.auth import get_current_active_user
from app.services.room_service import RoomService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new practice room.

    - **name**: Room name (3-100 characters)
    - **topic**: Discussion topic
    - **description**: Optional room description
    - **max_participants**: Maximum participants (2-10)
    - **is_public**: Whether room is publicly visible
    - **allow_recording**: Allow session recording
    - **require_approval**: Require approval to join
    - **english_level_filter**: Optional level filter
    """
    try:
        room = await RoomService.create_room(db, room_data, str(current_user.id))
        if not room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create room"
            )

        logger.info(f"Room created by user {current_user.id}: {room.name}")
        return room

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("", response_model=List[RoomResponse])
async def list_rooms(
    is_public: Optional[bool] = Query(None, description="Filter by public/private"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    english_level: Optional[EnglishLevel] = Query(None, description="Filter by English level"),
    skip: int = Query(0, ge=0, description="Number of rooms to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of rooms to return"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List practice rooms with optional filters.

    - **is_public**: Filter by public/private rooms
    - **topic**: Filter by topic keyword
    - **english_level**: Filter by English level requirement
    - **skip**: Pagination offset
    - **limit**: Maximum results (1-100)
    """
    try:
        filters = RoomFilter(
            is_public=is_public,
            topic=topic,
            english_level=english_level,
            skip=skip,
            limit=limit
        )

        rooms = await RoomService.list_rooms(db, filters, str(current_user.id))
        return rooms

    except Exception as e:
        logger.error(f"Error listing rooms: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get room details by ID.
    """
    # Implementation placeholder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: str,
    room_data: RoomUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update room details (only room creator can update).
    """
    # Implementation placeholder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete room (only room creator can delete).
    """
    # Implementation placeholder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.post("/{room_id}/join", response_model=RoomResponse)
async def join_room(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Join a practice room.
    
    Adds current user to room's participant list if room is not full.
    """
    # Implementation placeholder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.post("/{room_id}/leave", response_model=RoomResponse)
async def leave_room(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Leave a practice room.
    
    Removes current user from room's participant list.
    """
    # Implementation placeholder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.get("/search", response_model=List[RoomResponse])
async def search_rooms(
    query: str = Query(..., min_length=2, description="Search query"),
    english_level: Optional[EnglishLevel] = Query(None, description="Filter by English level"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Search rooms by topic, name, or description.
    
    - **query**: Search term (minimum 2 characters)
    - **english_level**: Optional level filter
    - **skip**: Pagination offset
    - **limit**: Maximum results (1-100)
    """
    # Implementation placeholder
    return []

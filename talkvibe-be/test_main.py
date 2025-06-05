"""
Simple TalkVibe FastAPI Application for Testing
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="TalkVibe API",
    version="1.0.0",
    description="TalkVibe - Community platform for English learners to practice speaking together"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models for testing
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    english_level: str = "beginner"
    bio: Optional[str] = None
    goals: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    english_level: str
    bio: Optional[str] = None
    goals: Optional[str] = None
    created_at: datetime
    is_active: bool = True

class RoomCreate(BaseModel):
    name: str
    topic: str
    description: Optional[str] = None
    max_participants: int = 4
    is_public: bool = True

class RoomResponse(BaseModel):
    id: str
    name: str
    topic: str
    description: Optional[str] = None
    max_participants: int
    is_public: bool
    creator_id: str
    participant_count: int
    created_at: datetime
    is_active: bool = True

# In-memory storage for testing
users_db = {}
rooms_db = {}

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TalkVibe API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": "TalkVibe",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# User endpoints
@app.post("/api/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def register_user(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create user
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "english_level": user_data.english_level,
        "bio": user_data.bio,
        "goals": user_data.goals,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    users_db[user_id] = user
    logger.info(f"User registered: {user_data.email}")
    
    return UserResponse(**user)

@app.get("/api/users", response_model=List[UserResponse], tags=["Users"])
async def list_users():
    """List all users."""
    return [UserResponse(**user) for user in users_db.values()]

@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: str):
    """Get user by ID."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**users_db[user_id])

# Room endpoints
@app.post("/api/rooms/create", response_model=RoomResponse, status_code=status.HTTP_201_CREATED, tags=["Rooms"])
async def create_room(room_data: RoomCreate):
    """Create a new practice room."""
    room_id = str(uuid.uuid4())
    creator_id = str(uuid.uuid4())  # Mock creator ID
    
    room = {
        "id": room_id,
        "name": room_data.name,
        "topic": room_data.topic,
        "description": room_data.description,
        "max_participants": room_data.max_participants,
        "is_public": room_data.is_public,
        "creator_id": creator_id,
        "participant_count": 1,  # Creator automatically joins
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    rooms_db[room_id] = room
    logger.info(f"Room created: {room_data.name}")
    
    return RoomResponse(**room)

@app.get("/api/rooms", response_model=List[RoomResponse], tags=["Rooms"])
async def list_rooms():
    """List all rooms."""
    return [RoomResponse(**room) for room in rooms_db.values()]

@app.get("/api/rooms/{room_id}", response_model=RoomResponse, tags=["Rooms"])
async def get_room(room_id: str):
    """Get room by ID."""
    if room_id not in rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return RoomResponse(**rooms_db[room_id])

# Chat endpoint (simple)
@app.post("/api/chats", tags=["Chat"])
async def send_message(room_id: str, message: str):
    """Send a message to a room."""
    if room_id not in rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    chat_message = {
        "id": str(uuid.uuid4()),
        "room_id": room_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": "test-user"
    }
    
    logger.info(f"Message sent to room {room_id}: {message[:50]}...")
    return chat_message

# Notifications endpoint (simple)
@app.get("/api/notifications", tags=["Notifications"])
async def get_notifications():
    """Get user notifications."""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Welcome to TalkVibe!",
            "message": "Start practicing English with other learners",
            "type": "welcome",
            "is_read": False,
            "created_at": datetime.utcnow().isoformat()
        }
    ]

# Sessions endpoint (simple)
@app.get("/api/sessions/stats", tags=["Sessions"])
async def get_session_stats():
    """Get practice statistics."""
    return {
        "total_sessions": 5,
        "total_hours": 12.5,
        "average_session_duration": 2.5,
        "favorite_topics": ["Daily Conversation", "Business English", "Travel"],
        "monthly_hours": [
            {"month": "2024-01", "hours": 8.5},
            {"month": "2024-02", "hours": 4.0}
        ]
    }

# Translations endpoint (simple)
@app.get("/api/content/{language_code}", tags=["Translations"])
async def get_content_by_language(language_code: str):
    """Get translated content for a specific language."""
    content = {
        "en": {
            "welcome_message": "Welcome to TalkVibe!",
            "login_button": "Login",
            "register_button": "Register"
        },
        "vi": {
            "welcome_message": "Chào mừng đến với TalkVibe!",
            "login_button": "Đăng nhập",
            "register_button": "Đăng ký"
        }
    }
    
    return {
        "language_code": language_code,
        "content": content.get(language_code, content["en"]),
        "categories": {
            "ui": content.get(language_code, content["en"])
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

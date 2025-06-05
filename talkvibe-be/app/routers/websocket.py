"""
WebSocket routes for TalkVibe application.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import Dict, List
import json
import logging
import asyncio
from datetime import datetime, timezone

from app.utils.auth import verify_token
from app.core.database import get_db
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    
    def __init__(self):
        # Room ID -> List of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # WebSocket -> User ID mapping
        self.connection_users: Dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Accept WebSocket connection and add to room."""
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        self.connection_users[websocket] = user_id
        
        logger.info(f"User {user_id} connected to room {room_id}")
        
        # Notify other users in room
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }, exclude=websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove WebSocket connection from room."""
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                
                # Clean up empty rooms
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]
        
        user_id = self.connection_users.pop(websocket, None)
        
        if user_id:
            logger.info(f"User {user_id} disconnected from room {room_id}")
            
            # Notify other users in room
            if room_id in self.active_connections:
                asyncio.create_task(self.broadcast_to_room(room_id, {
                    "type": "user_left",
                    "user_id": user_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }))
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket connection."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def broadcast_to_room(self, room_id: str, message: dict, exclude: WebSocket = None):
        """Broadcast message to all connections in a room."""
        if room_id not in self.active_connections:
            return
        
        message_text = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections[room_id]:
            if connection == exclude:
                continue
                
            try:
                await connection.send_text(message_text)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection, room_id)


# Global connection manager
manager = ConnectionManager()


async def get_current_user_websocket(websocket: WebSocket, token: str):
    """Get current user from WebSocket token."""
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        
        token_data = verify_token(token, credentials_exception)
        
        # Get user from database
        async with get_db() as db:
            user = await UserService.get_user_by_id(db, token_data.user_id)
            if not user or not user.is_active:
                raise credentials_exception
            
            return user
            
    except Exception as e:
        logger.error(f"WebSocket authentication error: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None


@router.websocket("/chat/{room_id}")
async def websocket_chat_endpoint(websocket: WebSocket, room_id: str, token: str):
    """
    WebSocket endpoint for real-time chat in rooms.
    
    Query parameters:
    - token: JWT authentication token
    
    Message format:
    ```json
    {
        "type": "chat_message",
        "message": "Hello everyone!",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    ```
    
    Received message types:
    - chat_message: New chat message
    - user_joined: User joined room
    - user_left: User left room
    - typing: User is typing
    - webrtc_signal: WebRTC signaling data
    """
    # Authenticate user
    user = await get_current_user_websocket(websocket, token)
    if not user:
        return
    
    # Connect to room
    await manager.connect(websocket, room_id, str(user.id))
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                # Add user info and timestamp
                message["user_id"] = str(user.id)
                message["user_name"] = user.name
                message["timestamp"] = datetime.now(timezone.utc).isoformat()
                
                # Handle different message types
                if message_type == "chat_message":
                    # Broadcast chat message to room
                    await manager.broadcast_to_room(room_id, message)
                    
                    # TODO: Save message to database
                    logger.info(f"Chat message in room {room_id} from {user.name}: {message.get('message', '')[:50]}")
                
                elif message_type == "typing":
                    # Broadcast typing indicator (don't save to DB)
                    await manager.broadcast_to_room(room_id, message, exclude=websocket)
                
                elif message_type == "webrtc_signal":
                    # Handle WebRTC signaling
                    target_user_id = message.get("target_user_id")
                    if target_user_id:
                        # Send to specific user (implement targeted messaging)
                        await manager.broadcast_to_room(room_id, message)
                    else:
                        # Broadcast to all users in room
                        await manager.broadcast_to_room(room_id, message, exclude=websocket)
                
                else:
                    logger.warning(f"Unknown message type: {message_type}")
                    
            except json.JSONDecodeError:
                logger.error("Invalid JSON received from WebSocket")
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid message format"
                }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, room_id)

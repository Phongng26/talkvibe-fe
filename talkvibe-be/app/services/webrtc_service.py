"""
WebRTC service for TalkVibe application.
"""
from typing import Dict, List, Optional, Any
import json
import logging
import asyncio
from datetime import datetime, timezone

from app.core.config import settings

logger = logging.getLogger(__name__)

# WebRTC imports (optional, install aiortc)
try:
    from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
    from aiortc.contrib.media import MediaPlayer, MediaRecorder
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False
    logger.warning("WebRTC not available. Install aiortc for WebRTC support.")


class WebRTCService:
    """Service class for WebRTC signaling and peer connection management."""
    
    def __init__(self):
        # Room ID -> List of peer connections
        self.room_connections: Dict[str, List[Dict]] = {}
        # Connection ID -> Peer connection info
        self.peer_connections: Dict[str, Dict] = {}
        
        # STUN/TURN server configuration
        self.ice_servers = [
            {"urls": settings.STUN_SERVER}
        ]
        
        if settings.TURN_SERVER and settings.TURN_USERNAME and settings.TURN_PASSWORD:
            self.ice_servers.append({
                "urls": settings.TURN_SERVER,
                "username": settings.TURN_USERNAME,
                "credential": settings.TURN_PASSWORD
            })
    
    async def create_peer_connection(
        self,
        room_id: str,
        user_id: str,
        connection_id: str
    ) -> Optional[Dict]:
        """Create a new WebRTC peer connection."""
        if not WEBRTC_AVAILABLE:
            logger.error("WebRTC not available")
            return None
        
        try:
            # Create RTCPeerConnection with ICE servers
            pc = RTCPeerConnection(configuration={
                "iceServers": self.ice_servers
            })
            
            # Store connection info
            connection_info = {
                "id": connection_id,
                "room_id": room_id,
                "user_id": user_id,
                "peer_connection": pc,
                "created_at": datetime.now(timezone.utc),
                "is_connected": False
            }
            
            # Add to room connections
            if room_id not in self.room_connections:
                self.room_connections[room_id] = []
            
            self.room_connections[room_id].append(connection_info)
            self.peer_connections[connection_id] = connection_info
            
            # Set up event handlers
            await self._setup_peer_connection_handlers(pc, connection_id)
            
            logger.info(f"Peer connection created: {connection_id} for user {user_id} in room {room_id}")
            
            return {
                "connection_id": connection_id,
                "ice_servers": self.ice_servers,
                "status": "created"
            }
            
        except Exception as e:
            logger.error(f"Error creating peer connection: {e}")
            return None
    
    async def _setup_peer_connection_handlers(self, pc: Any, connection_id: str):
        """Set up event handlers for peer connection."""
        
        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"Connection {connection_id} state: {pc.connectionState}")
            
            if connection_id in self.peer_connections:
                self.peer_connections[connection_id]["is_connected"] = (
                    pc.connectionState == "connected"
                )
            
            if pc.connectionState == "closed":
                await self.close_peer_connection(connection_id)
        
        @pc.on("icecandidate")
        async def on_icecandidate(candidate):
            if candidate:
                logger.debug(f"ICE candidate for {connection_id}: {candidate}")
        
        @pc.on("track")
        async def on_track(track):
            logger.info(f"Track received for {connection_id}: {track.kind}")
            
            # Handle incoming media track
            if track.kind == "audio":
                logger.info(f"Audio track received from {connection_id}")
            elif track.kind == "video":
                logger.info(f"Video track received from {connection_id}")
    
    async def handle_offer(
        self,
        connection_id: str,
        offer: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Handle WebRTC offer."""
        if not WEBRTC_AVAILABLE:
            return None
        
        try:
            if connection_id not in self.peer_connections:
                logger.error(f"Connection {connection_id} not found")
                return None
            
            connection_info = self.peer_connections[connection_id]
            pc = connection_info["peer_connection"]
            
            # Set remote description
            await pc.setRemoteDescription(RTCSessionDescription(
                sdp=offer["sdp"],
                type=offer["type"]
            ))
            
            # Create answer
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            
            logger.info(f"Answer created for connection {connection_id}")
            
            return {
                "type": answer.type,
                "sdp": answer.sdp
            }
            
        except Exception as e:
            logger.error(f"Error handling offer: {e}")
            return None
    
    async def handle_answer(
        self,
        connection_id: str,
        answer: Dict[str, Any]
    ) -> bool:
        """Handle WebRTC answer."""
        if not WEBRTC_AVAILABLE:
            return False
        
        try:
            if connection_id not in self.peer_connections:
                logger.error(f"Connection {connection_id} not found")
                return False
            
            connection_info = self.peer_connections[connection_id]
            pc = connection_info["peer_connection"]
            
            # Set remote description
            await pc.setRemoteDescription(RTCSessionDescription(
                sdp=answer["sdp"],
                type=answer["type"]
            ))
            
            logger.info(f"Answer handled for connection {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error handling answer: {e}")
            return False
    
    async def handle_ice_candidate(
        self,
        connection_id: str,
        candidate: Dict[str, Any]
    ) -> bool:
        """Handle ICE candidate."""
        if not WEBRTC_AVAILABLE:
            return False
        
        try:
            if connection_id not in self.peer_connections:
                logger.error(f"Connection {connection_id} not found")
                return False
            
            connection_info = self.peer_connections[connection_id]
            pc = connection_info["peer_connection"]
            
            # Add ICE candidate
            ice_candidate = RTCIceCandidate(
                candidate=candidate["candidate"],
                sdpMid=candidate.get("sdpMid"),
                sdpMLineIndex=candidate.get("sdpMLineIndex")
            )
            
            await pc.addIceCandidate(ice_candidate)
            
            logger.debug(f"ICE candidate added for connection {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error handling ICE candidate: {e}")
            return False
    
    async def close_peer_connection(self, connection_id: str) -> bool:
        """Close a peer connection."""
        try:
            if connection_id not in self.peer_connections:
                return False
            
            connection_info = self.peer_connections[connection_id]
            room_id = connection_info["room_id"]
            
            # Close peer connection
            if WEBRTC_AVAILABLE:
                pc = connection_info["peer_connection"]
                await pc.close()
            
            # Remove from room connections
            if room_id in self.room_connections:
                self.room_connections[room_id] = [
                    conn for conn in self.room_connections[room_id]
                    if conn["id"] != connection_id
                ]
                
                # Clean up empty rooms
                if not self.room_connections[room_id]:
                    del self.room_connections[room_id]
            
            # Remove from peer connections
            del self.peer_connections[connection_id]
            
            logger.info(f"Peer connection closed: {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error closing peer connection: {e}")
            return False
    
    def get_room_connections(self, room_id: str) -> List[Dict]:
        """Get all connections for a room."""
        if room_id not in self.room_connections:
            return []
        
        return [
            {
                "connection_id": conn["id"],
                "user_id": conn["user_id"],
                "is_connected": conn["is_connected"],
                "created_at": conn["created_at"].isoformat()
            }
            for conn in self.room_connections[room_id]
        ]
    
    def get_connection_stats(self, connection_id: str) -> Optional[Dict]:
        """Get connection statistics."""
        if connection_id not in self.peer_connections:
            return None
        
        connection_info = self.peer_connections[connection_id]
        
        return {
            "connection_id": connection_id,
            "room_id": connection_info["room_id"],
            "user_id": connection_info["user_id"],
            "is_connected": connection_info["is_connected"],
            "created_at": connection_info["created_at"].isoformat()
        }
    
    async def cleanup_room(self, room_id: str) -> int:
        """Clean up all connections for a room."""
        if room_id not in self.room_connections:
            return 0
        
        connections = self.room_connections[room_id].copy()
        closed_count = 0
        
        for connection in connections:
            if await self.close_peer_connection(connection["id"]):
                closed_count += 1
        
        logger.info(f"Cleaned up {closed_count} connections for room {room_id}")
        return closed_count


# Global WebRTC service instance
webrtc_service = WebRTCService()


import React, { useState, useRef, useEffect } from 'react';
import { Camera, CameraOff, Mic, MicOff, Users, MessageSquare, Settings, Phone, X } from 'lucide-react';
import ChatBox from '../chat/ChatBox';

interface RoomViewProps {
  roomId: string;
  roomName: string;
  onLeave: () => void;
}

const RoomView: React.FC<RoomViewProps> = ({ roomId, roomName, onLeave }) => {
  const [isCameraOn, setIsCameraOn] = useState(true);
  const [isMicOn, setIsMicOn] = useState(true);
  const [showChat, setShowChat] = useState(true);
  const [participants, setParticipants] = useState([
    { id: '1', name: 'You', isLocal: true, stream: null },
    { id: '2', name: 'Sarah Johnson', isLocal: false, stream: null },
    { id: '3', name: 'Mike Chen', isLocal: false, stream: null },
    { id: '4', name: 'Emma Wilson', isLocal: false, stream: null }
  ]);

  const localVideoRef = useRef<HTMLVideoElement>(null);
  const [localStream, setLocalStream] = useState<MediaStream | null>(null);

  useEffect(() => {
    // Initialize local media stream
    const initializeMedia = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });
        setLocalStream(stream);
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error('Error accessing media devices:', error);
      }
    };

    initializeMedia();

    // Cleanup on unmount
    return () => {
      if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const toggleCamera = () => {
    if (localStream) {
      const videoTrack = localStream.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled;
        setIsCameraOn(videoTrack.enabled);
      }
    }
  };

  const toggleMic = () => {
    if (localStream) {
      const audioTrack = localStream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        setIsMicOn(audioTrack.enabled);
      }
    }
  };

  const handleLeave = () => {
    if (localStream) {
      localStream.getTracks().forEach(track => track.stop());
    }
    onLeave();
  };

  return (
    <div className="fixed inset-0 bg-gray-900 z-50 flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 p-4 flex items-center justify-between">
        <div>
          <h2 className="text-white text-xl font-semibold">{roomName}</h2>
          <p className="text-gray-300 text-sm">{participants.length} participants</p>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setShowChat(!showChat)}
            className={`p-2 rounded-lg transition-colors ${
              showChat ? 'bg-blue-600 text-white' : 'text-gray-300 hover:text-white'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
          </button>
          <button className="text-gray-300 hover:text-white p-2">
            <Settings className="w-5 h-5" />
          </button>
          <button
            onClick={handleLeave}
            className="bg-red-600 hover:bg-red-700 text-white p-2 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Video Grid */}
        <div className={`flex-1 p-4 ${showChat ? 'pr-0' : ''}`}>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 h-full">
            {participants.map((participant) => (
              <div
                key={participant.id}
                className="relative bg-gray-800 rounded-lg overflow-hidden aspect-video"
              >
                {participant.isLocal ? (
                  <video
                    ref={localVideoRef}
                    autoPlay
                    muted
                    playsInline
                    className={`w-full h-full object-cover ${!isCameraOn ? 'hidden' : ''}`}
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center">
                      <span className="text-2xl font-bold text-gray-800">
                        {participant.name.charAt(0)}
                      </span>
                    </div>
                  </div>
                )}
                
                {/* Video Overlay */}
                <div className="absolute inset-0 bg-black bg-opacity-20"></div>
                
                {/* Participant Info */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-white font-medium text-sm">
                      {participant.name}
                    </span>
                    <div className="flex items-center space-x-1">
                      {participant.isLocal && !isMicOn && (
                        <MicOff className="w-4 h-4 text-red-400" />
                      )}
                      {participant.isLocal && !isCameraOn && (
                        <CameraOff className="w-4 h-4 text-red-400" />
                      )}
                    </div>
                  </div>
                </div>

                {/* Camera Off State */}
                {participant.isLocal && !isCameraOn && (
                  <div className="absolute inset-0 bg-gray-700 flex items-center justify-center">
                    <div className="text-center">
                      <CameraOff className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                      <p className="text-gray-300 text-sm">Camera is off</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Chat Panel */}
        {showChat && (
          <div className="w-80 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700">
            <ChatBox roomId={roomId} />
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="bg-gray-800 p-4">
        <div className="flex items-center justify-center space-x-4">
          <button
            onClick={toggleMic}
            className={`p-3 rounded-full transition-colors ${
              isMicOn
                ? 'bg-gray-600 hover:bg-gray-700 text-white'
                : 'bg-red-600 hover:bg-red-700 text-white'
            }`}
          >
            {isMicOn ? <Mic className="w-6 h-6" /> : <MicOff className="w-6 h-6" />}
          </button>

          <button
            onClick={toggleCamera}
            className={`p-3 rounded-full transition-colors ${
              isCameraOn
                ? 'bg-gray-600 hover:bg-gray-700 text-white'
                : 'bg-red-600 hover:bg-red-700 text-white'
            }`}
          >
            {isCameraOn ? <Camera className="w-6 h-6" /> : <CameraOff className="w-6 h-6" />}
          </button>

          <button
            onClick={handleLeave}
            className="p-3 rounded-full bg-red-600 hover:bg-red-700 text-white transition-colors"
          >
            <Phone className="w-6 h-6 transform rotate-[135deg]" />
          </button>

          <button className="p-3 rounded-full bg-gray-600 hover:bg-gray-700 text-white transition-colors">
            <Users className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RoomView;


import React from 'react';
import { Users, Globe, Lock, Star } from 'lucide-react';

interface Room {
  id: string;
  name: string;
  topic: string;
  participantCount: number;
  maxParticipants: number;
  level: string;
  isPublic: boolean;
  host: string;
  description: string;
  tags: string[];
}

interface RoomCardProps {
  room: Room;
}

const RoomCard: React.FC<RoomCardProps> = ({ room }) => {
  const occupancyPercentage = (room.participantCount / room.maxParticipants) * 100;
  
  const getOccupancyColor = () => {
    if (occupancyPercentage < 50) return 'text-green-500';
    if (occupancyPercentage < 80) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getLevelColor = () => {
    switch (room.level) {
      case 'Beginner': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'Advanced': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default: return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-1">
              {room.name}
            </h3>
            <div className="flex items-center space-x-2 mb-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor()}`}>
                {room.level}
              </span>
              <span className="text-sm text-gray-500 dark:text-gray-400">•</span>
              <span className="text-sm text-gray-600 dark:text-gray-300">{room.topic}</span>
            </div>
          </div>
          <div className="flex items-center space-x-1">
            {room.isPublic ? (
              <Globe className="w-5 h-5 text-green-500" />
            ) : (
              <Lock className="w-5 h-5 text-gray-400" />
            )}
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
          {room.description}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-1 mb-4">
          {room.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs rounded-md"
            >
              {tag}
            </span>
          ))}
          {room.tags.length > 3 && (
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-md">
              +{room.tags.length - 3}
            </span>
          )}
        </div>

        {/* Participants */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Users className={`w-4 h-4 ${getOccupancyColor()}`} />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {room.participantCount}/{room.maxParticipants}
            </span>
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Host: {room.host}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              occupancyPercentage < 50 ? 'bg-green-500' :
              occupancyPercentage < 80 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${occupancyPercentage}%` }}
          ></div>
        </div>

        {/* Join Button */}
        <button
          className={`w-full py-2 rounded-lg font-medium transition-colors duration-200 ${
            room.participantCount >= room.maxParticipants
              ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
          disabled={room.participantCount >= room.maxParticipants}
        >
          {room.participantCount >= room.maxParticipants ? 'Room Full' : 'Join Room'}
        </button>
      </div>
    </div>
  );
};

export default RoomCard;

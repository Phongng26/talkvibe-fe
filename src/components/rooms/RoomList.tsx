
import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import RoomCard from './RoomCard';
import SearchBar from '../search/SearchBar';

const RoomList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    level: '',
    topic: '',
    type: ''
  });

  // Mock room data
  const rooms = [
    {
      id: '1',
      name: 'Business English Practice',
      topic: 'Business',
      participantCount: 8,
      maxParticipants: 12,
      level: 'Intermediate',
      isPublic: true,
      host: 'Sarah Johnson',
      description: 'Practice professional English skills and business communication.',
      tags: ['Business', 'Professional', 'Networking']
    },
    {
      id: '2',
      name: 'Casual Conversation',
      topic: 'General',
      participantCount: 15,
      maxParticipants: 20,
      level: 'All Levels',
      isPublic: true,
      host: 'Mike Chen',
      description: 'Friendly chat about daily life, hobbies, and current events.',
      tags: ['Casual', 'Daily Life', 'Fun']
    },
    {
      id: '3',
      name: 'IELTS Speaking Prep',
      topic: 'Test Preparation',
      participantCount: 6,
      maxParticipants: 8,
      level: 'Advanced',
      isPublic: true,
      host: 'Emma Wilson',
      description: 'Intensive IELTS speaking practice with feedback and tips.',
      tags: ['IELTS', 'Test Prep', 'Speaking']
    },
    {
      id: '4',
      name: 'Travel Stories',
      topic: 'Travel',
      participantCount: 12,
      maxParticipants: 15,
      level: 'Beginner',
      isPublic: true,
      host: 'David Garcia',
      description: 'Share travel experiences and learn travel-related vocabulary.',
      tags: ['Travel', 'Stories', 'Culture']
    },
    {
      id: '5',
      name: 'Tech Talk',
      topic: 'Technology',
      participantCount: 9,
      maxParticipants: 12,
      level: 'Intermediate',
      isPublic: true,
      host: 'Lisa Park',
      description: 'Discuss latest technology trends and IT vocabulary.',
      tags: ['Technology', 'IT', 'Innovation']
    },
    {
      id: '6',
      name: 'Movie Discussion',
      topic: 'Entertainment',
      participantCount: 18,
      maxParticipants: 25,
      level: 'All Levels',
      isPublic: true,
      host: 'Tom Anderson',
      description: 'Talk about your favorite movies and TV shows.',
      tags: ['Movies', 'Entertainment', 'Culture']
    }
  ];

  const filteredRooms = rooms.filter(room => {
    const matchesSearch = room.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         room.topic.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         room.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesLevel = !filters.level || room.level === filters.level || room.level === 'All Levels';
    const matchesTopic = !filters.topic || room.topic === filters.topic;
    const matchesType = !filters.type || (filters.type === 'public' && room.isPublic);

    return matchesSearch && matchesLevel && matchesTopic && matchesType;
  });

  return (
    <div className="space-y-6">
      <SearchBar 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filters={filters}
        onFiltersChange={setFilters}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRooms.map(room => (
          <RoomCard key={room.id} room={room} />
        ))}
      </div>

      {filteredRooms.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Search className="w-16 h-16 mx-auto" />
          </div>
          <h3 className="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-2">
            No rooms found
          </h3>
          <p className="text-gray-500 dark:text-gray-400">
            Try adjusting your search terms or filters
          </p>
        </div>
      )}
    </div>
  );
};

export default RoomList;

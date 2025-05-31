
import React from 'react';
import { Star, Clock, Users, Award } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const ProfileCard = () => {
  const { user } = useAuth();

  if (!user) return null;

  const getLevelColor = () => {
    switch (user.level) {
      case 'Beginner': return 'text-green-600 bg-green-100 dark:bg-green-900 dark:text-green-300';
      case 'Intermediate': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-300';
      case 'Advanced': return 'text-red-600 bg-red-100 dark:bg-red-900 dark:text-red-300';
      default: return 'text-blue-600 bg-blue-100 dark:bg-blue-900 dark:text-blue-300';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center space-x-4 mb-6">
        <img
          src={user.avatar}
          alt={user.name}
          className="w-20 h-20 rounded-full object-cover ring-4 ring-blue-500"
        />
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {user.name}
          </h2>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getLevelColor()}`}>
            {user.level}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">
          <Clock className="w-6 h-6 text-blue-600 dark:text-blue-400 mx-auto mb-2" />
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {user.practiceHours}
          </div>
          <div className="text-sm text-blue-600 dark:text-blue-400">Practice Hours</div>
        </div>

        <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 text-center">
          <Users className="w-6 h-6 text-green-600 dark:text-green-400 mx-auto mb-2" />
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
            15
          </div>
          <div className="text-sm text-green-600 dark:text-green-400">Sessions</div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
          <Award className="w-5 h-5 mr-2 text-orange-500" />
          Achievements
        </h3>
        <div className="flex flex-wrap gap-2">
          {user.achievements.map((achievement, index) => (
            <span
              key={index}
              className="inline-block bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-3 py-1 rounded-full text-sm font-medium"
            >
              {achievement}
            </span>
          ))}
        </div>
      </div>

      <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors duration-200">
        Edit Profile
      </button>
    </div>
  );
};

export default ProfileCard;

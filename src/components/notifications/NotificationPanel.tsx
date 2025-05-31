
import React from 'react';
import { Clock, Users, MessageSquare, Star, X } from 'lucide-react';

const NotificationPanel = () => {
  const notifications = [
    {
      id: '1',
      type: 'invite',
      title: 'Room Invitation',
      message: 'Sarah invited you to join "Business English Practice"',
      time: '5 minutes ago',
      unread: true,
      icon: Users,
      color: 'text-blue-500'
    },
    {
      id: '2',
      type: 'message',
      title: 'New Message',
      message: 'You have a new message from Mike Chen',
      time: '1 hour ago',
      unread: true,
      icon: MessageSquare,
      color: 'text-green-500'
    },
    {
      id: '3',
      type: 'achievement',
      title: 'Achievement Unlocked!',
      message: 'You completed 10 practice sessions!',
      time: '2 hours ago',
      unread: false,
      icon: Star,
      color: 'text-orange-500'
    },
    {
      id: '4',
      type: 'reminder',
      title: 'Session Reminder',
      message: 'Your scheduled session starts in 30 minutes',
      time: '3 hours ago',
      unread: false,
      icon: Clock,
      color: 'text-purple-500'
    }
  ];

  return (
    <div className="absolute right-0 top-full mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Notifications
          </h3>
          <button className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">
            Mark all read
          </button>
        </div>
      </div>

      {/* Notifications List */}
      <div className="max-h-96 overflow-y-auto">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={`p-4 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer ${
              notification.unread ? 'bg-blue-50 dark:bg-blue-900/20' : ''
            }`}
          >
            <div className="flex items-start space-x-3">
              <div className={`p-2 rounded-full bg-gray-100 dark:bg-gray-700 ${notification.color}`}>
                <notification.icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {notification.title}
                  </p>
                  {notification.unread && (
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  )}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                  {notification.message}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {notification.time}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-4 text-center border-t border-gray-200 dark:border-gray-700">
        <button className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium">
          View All Notifications
        </button>
      </div>
    </div>
  );
};

export default NotificationPanel;

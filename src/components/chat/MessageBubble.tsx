
import React from 'react';

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
  isOwn: boolean;
}

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex ${message.isOwn ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs lg:max-w-md ${message.isOwn ? 'order-2' : 'order-1'}`}>
        {!message.isOwn && (
          <div className="text-xs text-gray-600 dark:text-gray-400 mb-1 px-2">
            {message.sender}
          </div>
        )}
        <div
          className={`px-4 py-2 rounded-2xl ${
            message.isOwn
              ? 'bg-blue-600 text-white rounded-br-md'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-bl-md'
          }`}
        >
          <p className="text-sm">{message.content}</p>
          <div
            className={`text-xs mt-1 ${
              message.isOwn ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'
            }`}
          >
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;

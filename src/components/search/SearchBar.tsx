
import React from 'react';
import { Search, Filter } from 'lucide-react';

interface SearchBarProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  filters: {
    level: string;
    topic: string;
    type: string;
  };
  onFiltersChange: (filters: any) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  searchTerm,
  onSearchChange,
  filters,
  onFiltersChange
}) => {
  const levels = ['', 'Beginner', 'Intermediate', 'Advanced', 'All Levels'];
  const topics = ['', 'Business', 'General', 'Travel', 'Technology', 'Entertainment', 'Test Preparation'];
  const types = ['', 'public', 'private'];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 space-y-4">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search rooms by name, topic, or description..."
          className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <div className="flex items-center space-x-2">
          <Filter className="w-5 h-5 text-gray-500" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Filters:</span>
        </div>

        <select
          value={filters.level}
          onChange={(e) => onFiltersChange({ ...filters, level: e.target.value })}
          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">All Levels</option>
          {levels.slice(1).map(level => (
            <option key={level} value={level}>{level}</option>
          ))}
        </select>

        <select
          value={filters.topic}
          onChange={(e) => onFiltersChange({ ...filters, topic: e.target.value })}
          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">All Topics</option>
          {topics.slice(1).map(topic => (
            <option key={topic} value={topic}>{topic}</option>
          ))}
        </select>

        <select
          value={filters.type}
          onChange={(e) => onFiltersChange({ ...filters, type: e.target.value })}
          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">All Types</option>
          <option value="public">Public Only</option>
          <option value="private">Private Only</option>
        </select>

        {/* Clear Filters */}
        {(filters.level || filters.topic || filters.type || searchTerm) && (
          <button
            onClick={() => {
              onSearchChange('');
              onFiltersChange({ level: '', topic: '', type: '' });
            }}
            className="px-3 py-2 text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
          >
            Clear All
          </button>
        )}
      </div>
    </div>
  );
};

export default SearchBar;

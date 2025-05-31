
import React, { useState } from 'react';
import { Users, Clock, Globe } from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';
import RoomList from '../rooms/RoomList';
import CreateRoomModal from '../rooms/CreateRoomModal';

const RoomsSection = () => {
  const { t } = useLanguage();
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <>
      <section id="rooms" className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              {t('rooms.title')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Join active practice rooms or create your own. Connect with learners who share your interests and goals.
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
            >
              {t('rooms.create')}
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl p-6 text-center">
              <Users className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">250+</h3>
              <p>Active Rooms</p>
            </div>
            <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl p-6 text-center">
              <Clock className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">24/7</h3>
              <p>Always Available</p>
            </div>
            <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-xl p-6 text-center">
              <Globe className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">100+</h3>
              <p>Countries</p>
            </div>
          </div>

          <RoomList />
        </div>
      </section>

      {showCreateModal && (
        <CreateRoomModal onClose={() => setShowCreateModal(false)} />
      )}
    </>
  );
};

export default RoomsSection;

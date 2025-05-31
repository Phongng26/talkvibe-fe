
import React, { useState } from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { useAuth } from '../../contexts/AuthContext';
import AuthModal from '../auth/AuthModal';

const HeroSection = () => {
  const { t } = useLanguage();
  const { isAuthenticated } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  return (
    <>
      <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                {t('hero.title')}
              </h1>
              <p className="text-xl md:text-2xl text-blue-100 leading-relaxed">
                {t('hero.subtitle')}
              </p>
              <div className="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex">
                {!isAuthenticated && (
                  <button
                    onClick={() => setShowAuthModal(true)}
                    className="w-full sm:w-auto bg-orange-500 hover:bg-orange-600 text-white font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
                  >
                    {t('hero.cta')}
                  </button>
                )}
                <button className="w-full sm:w-auto bg-transparent border-2 border-white text-white hover:bg-white hover:text-blue-700 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300">
                  Watch Demo
                </button>
              </div>
              <div className="flex items-center space-x-8 pt-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-400">50K+</div>
                  <div className="text-blue-200">Active Learners</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400">100+</div>
                  <div className="text-blue-200">Countries</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400">24/7</div>
                  <div className="text-blue-200">Practice Sessions</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="w-12 h-12 bg-orange-500 rounded-full mx-auto mb-2 flex items-center justify-center">
                      <span className="text-white font-bold">🎯</span>
                    </div>
                    <div className="text-sm">Goal Setting</div>
                  </div>
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="w-12 h-12 bg-green-500 rounded-full mx-auto mb-2 flex items-center justify-center">
                      <span className="text-white font-bold">💬</span>
                    </div>
                    <div className="text-sm">Live Practice</div>
                  </div>
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="w-12 h-12 bg-purple-500 rounded-full mx-auto mb-2 flex items-center justify-center">
                      <span className="text-white font-bold">📊</span>
                    </div>
                    <div className="text-sm">Progress Tracking</div>
                  </div>
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="w-12 h-12 bg-blue-500 rounded-full mx-auto mb-2 flex items-center justify-center">
                      <span className="text-white font-bold">🌍</span>
                    </div>
                    <div className="text-sm">Global Community</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {showAuthModal && (
        <AuthModal
          mode="register"
          onClose={() => setShowAuthModal(false)}
          onSwitchMode={() => {}}
        />
      )}
    </>
  );
};

export default HeroSection;

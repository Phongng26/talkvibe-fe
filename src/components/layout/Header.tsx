
import React, { useState } from 'react';
import { Bell, Moon, Sun, Globe, Menu, X } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import AuthModal from '../auth/AuthModal';
import NotificationPanel from '../notifications/NotificationPanel';

const Header = () => {
  const { isDark, toggleTheme } = useTheme();
  const { user, logout, isAuthenticated } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const handleAuthClick = (mode: 'login' | 'register') => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const navItems = [
    { key: 'nav.home', href: '#' },
    { key: 'nav.rooms', href: '#rooms' },
    { key: 'nav.profile', href: '#profile' },
  ];

  return (
    <>
      <header className="bg-white dark:bg-gray-800 shadow-lg transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  EnglishConnect
                </h1>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navItems.map((item) => (
                  <a
                    key={item.key}
                    href={item.href}
                    className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    {t(item.key)}
                  </a>
                ))}
              </div>
            </nav>

            {/* Right side controls */}
            <div className="flex items-center space-x-4">
              {/* Language Switcher */}
              <div className="relative">
                <button
                  onClick={() => setLanguage(language === 'en' ? 'vi' : 'en')}
                  className="flex items-center text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200"
                >
                  <Globe className="w-5 h-5" />
                  <span className="ml-1 text-sm">{language.toUpperCase()}</span>
                </button>
              </div>

              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200"
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>

              {/* Notifications */}
              {isAuthenticated && (
                <div className="relative">
                  <button
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="relative text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200"
                  >
                    <Bell className="w-5 h-5" />
                    <span className="absolute -top-1 -right-1 bg-orange-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
                      3
                    </span>
                  </button>
                  {showNotifications && <NotificationPanel />}
                </div>
              )}

              {/* Auth Buttons */}
              {isAuthenticated ? (
                <div className="flex items-center space-x-3">
                  <img
                    src={user?.avatar}
                    alt={user?.name}
                    className="w-8 h-8 rounded-full"
                  />
                  <span className="hidden md:block text-gray-700 dark:text-gray-300">
                    {user?.name}
                  </span>
                  <button
                    onClick={logout}
                    className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    {t('auth.logout')}
                  </button>
                </div>
              ) : (
                <div className="hidden md:flex space-x-2">
                  <button
                    onClick={() => handleAuthClick('login')}
                    className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    {t('auth.login')}
                  </button>
                  <button
                    onClick={() => handleAuthClick('register')}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    {t('auth.register')}
                  </button>
                </div>
              )}

              {/* Mobile menu button */}
              <button
                onClick={() => setShowMobileMenu(!showMobileMenu)}
                className="md:hidden text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
              >
                {showMobileMenu ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {showMobileMenu && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-50 dark:bg-gray-700 rounded-lg mt-2">
                {navItems.map((item) => (
                  <a
                    key={item.key}
                    href={item.href}
                    className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 block px-3 py-2 rounded-md text-base font-medium"
                  >
                    {t(item.key)}
                  </a>
                ))}
                {!isAuthenticated && (
                  <div className="pt-2 space-y-2">
                    <button
                      onClick={() => handleAuthClick('login')}
                      className="w-full text-left text-blue-600 dark:text-blue-400 px-3 py-2 rounded-md text-base font-medium"
                    >
                      {t('auth.login')}
                    </button>
                    <button
                      onClick={() => handleAuthClick('register')}
                      className="w-full text-left bg-blue-600 text-white px-3 py-2 rounded-md text-base font-medium"
                    >
                      {t('auth.register')}
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </header>

      {showAuthModal && (
        <AuthModal
          mode={authMode}
          onClose={() => setShowAuthModal(false)}
          onSwitchMode={setAuthMode}
        />
      )}
    </>
  );
};

export default Header;

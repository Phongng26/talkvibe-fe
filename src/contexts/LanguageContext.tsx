
import React, { createContext, useContext, useState } from 'react';

interface LanguageContextType {
  language: string;
  setLanguage: (lang: string) => void;
  t: (key: string) => string;
}

const translations = {
  en: {
    'nav.home': 'Home',
    'nav.rooms': 'Rooms',
    'nav.profile': 'Profile',
    'nav.notifications': 'Notifications',
    'nav.settings': 'Settings',
    'auth.login': 'Login',
    'auth.register': 'Register',
    'auth.logout': 'Logout',
    'hero.title': 'Practice English Together',
    'hero.subtitle': 'Join our global community and improve your English speaking skills through real conversations',
    'hero.cta': 'Start Learning Now',
    'rooms.title': 'Practice Rooms',
    'rooms.create': 'Create Room',
    'profile.level': 'Level',
    'profile.hours': 'Practice Hours'
  },
  vi: {
    'nav.home': 'Trang chủ',
    'nav.rooms': 'Phòng học',
    'nav.profile': 'Hồ sơ',
    'nav.notifications': 'Thông báo',
    'nav.settings': 'Cài đặt',
    'auth.login': 'Đăng nhập',
    'auth.register': 'Đăng ký',
    'auth.logout': 'Đăng xuất',
    'hero.title': 'Luyện tập tiếng Anh cùng nhau',
    'hero.subtitle': 'Tham gia cộng đồng toàn cầu và cải thiện kỹ năng nói tiếng Anh qua các cuộc trò chuyện thực tế',
    'hero.cta': 'Bắt đầu học ngay',
    'rooms.title': 'Phòng luyện tập',
    'rooms.create': 'Tạo phòng',
    'profile.level': 'Trình độ',
    'profile.hours': 'Giờ luyện tập'
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState('en');

  const t = (key: string): string => {
    return translations[language as keyof typeof translations]?.[key as keyof typeof translations.en] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

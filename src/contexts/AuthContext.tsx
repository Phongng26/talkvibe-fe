
import React, { createContext, useContext, useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  level: string;
  practiceHours: number;
  achievements: string[];
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    // Mock login - replace with actual API call
    console.log('Login attempt:', email, password);
    const mockUser: User = {
      id: '1',
      name: 'John Doe',
      email: email,
      avatar: '/placeholder.svg',
      level: 'Intermediate',
      practiceHours: 48,
      achievements: ['First Session', 'Week Streak', '10 Hours']
    };
    setUser(mockUser);
  };

  const register = async (name: string, email: string, password: string) => {
    // Mock registration - replace with actual API call
    console.log('Register attempt:', name, email, password);
    const mockUser: User = {
      id: '1',
      name: name,
      email: email,
      avatar: '/placeholder.svg',
      level: 'Beginner',
      practiceHours: 0,
      achievements: []
    };
    setUser(mockUser);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      user,
      login,
      register,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};


import React from 'react';
import HeroSection from '../sections/HeroSection';
import FeaturesSection from '../sections/FeaturesSection';
import RoomsSection from '../sections/RoomsSection';
import StatsSection from '../sections/StatsSection';

const HomePage = () => {
  return (
    <div className="space-y-0">
      <HeroSection />
      <FeaturesSection />
      <RoomsSection />
      <StatsSection />
    </div>
  );
};

export default HomePage;

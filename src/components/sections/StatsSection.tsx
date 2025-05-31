
import React from 'react';

const StatsSection = () => {
  const stats = [
    { number: '50,000+', label: 'Active Learners', description: 'Join our growing community' },
    { number: '1M+', label: 'Practice Sessions', description: 'Hours of conversation practice' },
    { number: '150+', label: 'Countries', description: 'Global reach and diversity' },
    { number: '98%', label: 'Satisfaction Rate', description: 'Learners love our platform' }
  ];

  return (
    <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-700 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Trusted by Learners Worldwide
          </h2>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Join thousands of learners who have improved their English with our platform.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-orange-400 mb-2">
                {stat.number}
              </div>
              <div className="text-xl font-semibold mb-2">
                {stat.label}
              </div>
              <div className="text-blue-200">
                {stat.description}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;

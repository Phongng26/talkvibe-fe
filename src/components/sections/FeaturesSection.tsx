
import React from 'react';
import { Camera, MessageSquare, Users, Settings } from 'lucide-react';

const FeaturesSection = () => {
  const features = [
    {
      icon: Camera,
      title: 'Video Practice Rooms',
      description: 'Join live video sessions with learners from around the world. Practice speaking in a supportive environment.',
      color: 'bg-blue-500'
    },
    {
      icon: MessageSquare,
      title: 'Real-time Chat',
      description: 'Communicate through text when speaking feels challenging. Share resources and tips with fellow learners.',
      color: 'bg-green-500'
    },
    {
      icon: Users,
      title: 'Community Matching',
      description: 'Get matched with learners at your level. Find practice partners based on your interests and goals.',
      color: 'bg-orange-500'
    },
    {
      icon: Settings,
      title: 'Progress Tracking',
      description: 'Monitor your improvement with detailed analytics. Set goals and celebrate your achievements.',
      color: 'bg-purple-500'
    }
  ];

  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Why Choose EnglishConnect?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Experience the most effective way to improve your English through real conversations and community support.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
            >
              <div className={`${feature.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;

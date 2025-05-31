
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 dark:bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-blue-400">EnglishConnect</h3>
            <p className="text-gray-300 text-sm">
              Practice English with native speakers and learners from around the world.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-md font-semibold">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Home</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Practice Rooms</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Community</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Resources</a></li>
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h4 className="text-md font-semibold">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Help Center</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Contact Us</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Terms of Service</a></li>
              <li><a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Privacy Policy</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-4">
            <h4 className="text-md font-semibold">Contact</h4>
            <div className="text-sm text-gray-300 space-y-2">
              <p>Email: hello@englishconnect.com</p>
              <p>Phone: +1 (555) 123-4567</p>
              <div className="flex space-x-4 pt-2">
                <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Facebook</a>
                <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Twitter</a>
                <a href="#" className="text-gray-300 hover:text-blue-400 transition-colors">Instagram</a>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-sm text-gray-400">
            © 2024 EnglishConnect. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

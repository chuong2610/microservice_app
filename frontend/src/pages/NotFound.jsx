import React from 'react';
import { Link } from 'react-router-dom';
import { Home, ArrowLeft, Search, AlertCircle } from 'lucide-react';
import { getAppConfig } from '../config/appConfig';

const NotFound = () => {
  const appConfig = getAppConfig();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        {/* 404 Icon */}
        <div className="mb-8">
          <div className="mx-auto w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mb-4">
            <AlertCircle className="w-12 h-12 text-red-600" />
          </div>
          <h1 className="text-6xl font-bold text-gray-900 mb-2">404</h1>
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
        </div>

        {/* Error Message */}
        <div className="mb-8">
          <p className="text-gray-600 text-lg mb-4">
            Sorry, the page you're looking for doesn't exist or is still under development.
          </p>
          <p className="text-gray-500 text-sm">
            The URL may be incorrect, or the page may have been moved or deleted.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="space-y-4">
          <Link
            to="/"
            className={`w-full btn-primary ${appConfig.theme.primary} inline-flex items-center justify-center py-3 px-6 text-base font-medium rounded-lg transition-colors duration-200`}
          >
            <Home className="w-5 h-5 mr-2" />
            Go to Homepage
          </Link>
          
          <Link
            to="/items"
            className="w-full bg-white border border-gray-300 text-gray-700 font-medium py-3 px-6 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200 inline-flex items-center justify-center"
          >
            <Search className="w-5 h-5 mr-2" />
            Browse Items
          </Link>

          <button
            onClick={() => window.history.back()}
            className="w-full text-gray-600 hover:text-gray-800 font-medium py-3 px-6 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200 inline-flex items-center justify-center"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Go Back
          </button>
        </div>

        {/* Additional Help */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-gray-500 text-sm mb-4">
            Need help? Here are some popular pages:
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <Link to="/" className="text-blue-600 hover:text-blue-800 transition-colors">
              Home
            </Link>
            <Link to="/items" className="text-blue-600 hover:text-blue-800 transition-colors">
              Items
            </Link>
            <Link to="/users" className="text-blue-600 hover:text-blue-800 transition-colors">
              Authors
            </Link>
            <Link to="/profile" className="text-blue-600 hover:text-blue-800 transition-colors">
              Profile
            </Link>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8">
          <p className="text-xs text-gray-400">
            © 2024 {appConfig.name}. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotFound;

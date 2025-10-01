import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { User, LogOut, Plus, ChevronDown } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { getAppConfig } from '../config/appConfig';
import defaultAvatar from '../imgs/PDZ.jpg';

const UserMenu = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);
  const appConfig = getAppConfig();

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = async () => {
    await logout();
    setIsOpen(false);
  };

  if (!isAuthenticated || !user) {
    return null;
  }

  const userName = user.sub?.full_name || user.full_name || user.email || 'User';
  const userAvatar = user.sub?.avatar_url || user.avatar_url || defaultAvatar;

  return (
    <div className="relative" ref={menuRef}>
      {/* User Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 text-gray-700 hover:text-gray-900 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg p-2"
      >
        <img
          src={userAvatar}
          alt={userName}
          className="w-8 h-8 rounded-full object-cover border-2 border-gray-200"
          onError={(e) => { e.target.src = defaultAvatar; }}
        />
        <div className="hidden md:block text-left">
          <div className="text-sm font-medium">{userName}</div>
          <div className="text-xs text-gray-500">{user.sub?.role || user.role || 'user'}</div>
        </div>
        <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
          {/* User Info Header */}
          <div className="px-4 py-3 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <img
                src={userAvatar}
                alt={userName}
                className="w-10 h-10 rounded-full object-cover"
                onError={(e) => { e.target.src = defaultAvatar; }}
              />
              <div>
                <div className="font-medium text-gray-900">{userName}</div>
                <div className="text-sm text-gray-500">{user.sub?.email || user.email}</div>
                <div className="text-xs text-gray-400 capitalize">{user.sub?.role || user.role || 'user'}</div>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-1">
            <Link
              to="/profile"
              onClick={() => setIsOpen(false)}
              className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
            >
              <User className="w-4 h-4 mr-3" />
              My Profile
            </Link>
            
            <Link
              to="/create"
              onClick={() => setIsOpen(false)}
              className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
            >
              <Plus className="w-4 h-4 mr-3" />
              Create Item
            </Link>

          </div>

          {/* Logout */}
          <div className="border-t border-gray-100 py-1">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200"
            >
              <LogOut className="w-4 h-4 mr-3" />
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserMenu;

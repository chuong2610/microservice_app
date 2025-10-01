import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { RefreshCw, LogOut, AlertTriangle } from 'lucide-react';

const AuthStatus = () => {
  const { isAuthenticated, user, logout } = useAuth();

  // Don't show anything if not authenticated
  if (!isAuthenticated) return null;

  const handleRefresh = () => {
    console.log('Manual refresh requested');
    window.location.reload();
  };

  const handleLogout = () => {
    console.log('Manual logout requested');
    logout();
  };

  return (
    <div className="fixed bottom-4 right-4 bg-white border border-gray-200 rounded-lg shadow-lg p-3 max-w-sm z-50">
      <div className="flex items-center gap-2 mb-2">
        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
        <span className="text-sm font-medium text-gray-700">
          Signed in as {user?.email || user?.full_name || 'User'}
        </span>
      </div>
      
      <div className="flex gap-2">
        <button
          onClick={handleRefresh}
          className="flex items-center gap-1 px-2 py-1 text-xs bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
          title="Refresh page"
        >
          <RefreshCw size={12} />
          Refresh
        </button>
        
        <button
          onClick={handleLogout}
          className="flex items-center gap-1 px-2 py-1 text-xs bg-red-50 text-red-600 rounded hover:bg-red-100 transition-colors"
          title="Sign out"
        >
          <LogOut size={12} />
          Sign Out
        </button>
      </div>
      
      <div className="mt-2 text-xs text-gray-500">
        <AlertTriangle size={10} className="inline mr-1" />
        If you experience issues, try refreshing or signing out and back in.
      </div>
    </div>
  );
};

export default AuthStatus;


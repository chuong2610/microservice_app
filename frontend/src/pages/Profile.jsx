import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { User, Mail, Calendar, Edit, FileText, Eye } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { userService } from '../services/userService';
import { itemService } from '../services/itemService';
import { getAppConfig } from '../config/appConfig';
import ProfileAnalytics from '../components/ProfileAnalytics';
import defaultImage from '../imgs/PDZ.jpg';

const Profile = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user: authUser, loading: authLoading } = useAuth();
  const [user, setUser] = useState(null);
  const [userItems, setUserItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [itemsLoading, setItemsLoading] = useState(true);
  const appConfig = getAppConfig();

  useEffect(() => {
    const fetchUserProfile = async () => {
      if (!isAuthenticated) {
        navigate('/login');
        return;
      }

      if (!authUser) {
        setLoading(false);
        return;
      }

      try {
        // Get user ID from auth context
        const userId = authUser.sub?.id || authUser.user_id || authUser.id;
        console.log('Profile: Auth user data:', authUser);
        console.log('Profile: Extracted user ID:', userId);

        if (userId) {
          // Fetch full user details
          const userResponse = await userService.getUserById(userId);
          console.log('Profile: User service response:', userResponse);
          
          if (userResponse.status_code === 200 && userResponse.data) {
            setUser(userResponse.data);
            // Fetch user's items
            fetchUserItems(userId);
          } else {
            console.error('Failed to fetch user details:', userResponse);
            // Fallback: use auth user data
            setUser(authUser);
            fetchUserItems(userId);
          }
        } else {
          console.error('No user ID found in auth data');
          // Fallback: use auth user data
          setUser(authUser);
          // Still try to fetch items with fallback ID
          const fallbackUserId = authUser.id || authUser.email;
          if (fallbackUserId) {
            fetchUserItems(fallbackUserId);
          }
        }
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
        // Fallback: use auth user data
        setUser(authUser);
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading) {
      fetchUserProfile();
    }
  }, [isAuthenticated, authUser, authLoading, navigate]);

  const fetchUserItems = async (userId) => {
    try {
      const response = await itemService.getItemsByAuthor(userId, 1, 10);
      setUserItems(response.data?.items || []);
    } catch (error) {
      console.error('Failed to fetch user items:', error);
      setUserItems([]);
    } finally {
      setItemsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getRoleColor = (role) => {
    switch (role?.toLowerCase()) {
      case 'admin':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'writer':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'user':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-48 bg-gray-200 rounded-lg mb-8"></div>
          <div className="h-64 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Authentication Required</h2>
          <p className="mt-2 text-gray-600">Please log in to view your profile.</p>
          <Link
            to="/login"
            className={`mt-4 inline-block btn-primary ${appConfig.theme.primary}`}
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  // Use authUser as fallback if user is null
  const displayUser = user || authUser;
  
  if (!displayUser) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">User data not available</h2>
          <p className="mt-2 text-gray-600">Unable to load profile data.</p>
          <Link
            to="/login"
            className={`mt-4 inline-block btn-primary ${appConfig.theme.primary}`}
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
        <div className="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6">
          {/* Avatar */}
          <div className="flex-shrink-0">
            {(displayUser.avatar_url || displayUser.sub?.avatar_url) ? (
              <img
                className="h-24 w-24 rounded-full object-cover ring-4 ring-gray-100"
                src={displayUser.avatar_url || displayUser.sub?.avatar_url}
                alt={displayUser.full_name || displayUser.sub?.full_name}
                onError={(e) => { e.target.src = defaultImage; }}
              />
            ) : (
              <div className="h-24 w-24 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center ring-4 ring-gray-100">
                <User className="h-12 w-12 text-white" />
              </div>
            )}
          </div>

          {/* User Info */}
          <div className="flex-grow">
            <div className="flex items-center space-x-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">
                {displayUser.full_name || displayUser.sub?.full_name || 'User'}
              </h1>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getRoleColor(displayUser.role || displayUser.sub?.role)}`}>
                {displayUser.role || displayUser.sub?.role || 'user'}
              </span>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center text-gray-600">
                <Mail className="w-4 h-4 mr-2" />
                {displayUser.email || displayUser.sub?.email}
              </div>
              {(displayUser.created_at || displayUser.sub?.created_at) && (
                <div className="flex items-center text-gray-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  Member since {formatDate(displayUser.created_at || displayUser.sub?.created_at)}
                </div>
              )}
            </div>
          </div>

          {/* Edit Button */}
          <div>
            <Link
              to="/profile/edit"
              className="btn-secondary inline-flex items-center"
            >
              <Edit className="w-4 h-4 mr-2" />
              Edit Profile
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className={`p-3 rounded-lg ${appConfig.theme.primary} mr-4`}>
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{userItems.length}</p>
              <p className="text-gray-600">Items Published</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className={`p-3 rounded-lg ${appConfig.theme.primary} mr-4`}>
              <Eye className="w-6 h-6 text-white" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">--</p>
              <p className="text-gray-600">Total Views</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className={`p-3 rounded-lg ${appConfig.theme.primary} mr-4`}>
              <User className="w-6 h-6 text-white" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">--</p>
              <p className="text-gray-600">Followers</p>
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Section */}
      <ProfileAnalytics userItems={userItems} user={displayUser} />

      {/* My Articles Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">My Items</h2>
          <Link
            to="/create"
            className={`btn-primary ${appConfig.theme.primary} text-sm`}
          >
            Create New Item
          </Link>
        </div>

        {itemsLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, index) => (
              <div key={index} className="animate-pulse">
                <div className="h-24 bg-gray-200 rounded-lg"></div>
              </div>
            ))}
          </div>
        ) : userItems.length > 0 ? (
          <div className="space-y-4">
            {userItems.map((item) => (
              <div
                key={item.id}
                className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all"
              >
                {/* Thumbnail */}
                <div className="flex-shrink-0">
                  <img
                    src={item.images && item.images.length > 0 ? item.images[0] : defaultImage}
                    alt={item.title}
                    className="w-20 h-20 object-cover rounded-lg"
                    onError={(e) => { e.target.src = defaultImage; }}
                  />
                </div>

                {/* Content */}
                <div className="flex-grow min-w-0">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1 truncate">
                    <Link
                      to={`/items/${item.id}`}
                      className="hover:text-gray-700 transition-colors"
                    >
                      {item.title}
                    </Link>
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-2 mb-2">
                    {item.abstract}
                  </p>
                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span className="flex items-center">
                      <Calendar className="w-3 h-3 mr-1" />
                      {formatDate(item.created_at || item.createdAt)}
                    </span>
                    {item.category && (
                      <span className={`px-2 py-1 rounded-full ${appConfig.theme.accent} bg-opacity-10`}>
                        {item.category}
                      </span>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex-shrink-0 flex flex-col space-y-2">
                  <Link
                    to={`/items/${item.id}`}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    View
                  </Link>
                  <Link
                    to={`/items/${item.id}/edit`}
                    className="text-sm text-gray-600 hover:text-gray-800"
                  >
                    Edit
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No items yet
            </h3>
            <p className="text-gray-600 mb-6">
              Start sharing your knowledge by creating your first item.
            </p>
            <Link
              to="/create"
              className={`btn-primary ${appConfig.theme.primary} inline-flex items-center`}
            >
              <FileText className="w-4 h-4 mr-2" />
              Create Your First Item
            </Link>
          </div>
        )}

        {userItems.length > 0 && (
          <div className="mt-6 text-center">
            <Link
              to={`/author/${user.id}`}
              className={`text-sm ${appConfig.theme.accent} hover:opacity-80`}
            >
              View all items →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;

import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { User, Mail, Calendar, FileText, ArrowLeft, MapPin, Globe } from 'lucide-react';
import { userService } from '../services/userService';
import { itemService } from '../services/itemService';
import { getAppConfig } from '../config/appConfig';
import ItemCard from '../components/ItemCard';
import Pagination from '../components/Pagination';
import defaultImage from '../imgs/PDZ.jpg';

const AuthorProfile = () => {
  const { authorId } = useParams();
  const [author, setAuthor] = useState(null);
  const [authorItems, setAuthorItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [itemsLoading, setItemsLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalItems, setTotalItems] = useState(0);
  const hasFetched = useRef(false);
  const currentAuthorId = useRef('');
  const appConfig = getAppConfig();
  const pageSize = 12;

  useEffect(() => {
    const fetchAuthorProfile = async () => {
      if (currentAuthorId.current !== authorId) {
        hasFetched.current = false;
        currentAuthorId.current = authorId;
      }
      
      if (hasFetched.current) return;
      hasFetched.current = true;

      setLoading(true);
      setError('');

      try {
        // Fetch author details
        const authorResponse = await userService.getUserById(authorId);
        if (authorResponse.status_code === 200 && authorResponse.data) {
          setAuthor(authorResponse.data);
        } else {
          setError('Author not found');
          setLoading(false);
          return;
        }

        // Fetch author's items
        const itemsResponse = await itemService.getItemsByAuthor(authorId, currentPage, pageSize);
        if (itemsResponse.status_code === 200 && itemsResponse.data) {
          setAuthorItems(itemsResponse.data.items || []);
          setTotalPages(itemsResponse.data.total_pages || 0);
          setTotalItems(itemsResponse.data.total_items || 0);
        }
      } catch (err) {
        console.error('Error fetching author profile:', err);
        setError('Failed to load author profile');
      } finally {
        setLoading(false);
        setItemsLoading(false);
      }
    };

    if (authorId) {
      fetchAuthorProfile();
    }
  }, [authorId, currentPage]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    hasFetched.current = false; // Allow refetch for new page
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
        <div className="text-red-600 mb-4">
          <h2 className="text-2xl font-bold">{error}</h2>
        </div>
        <Link to="/users" className="btn-primary">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Users
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <div className="mb-6">
        <Link
          to="/users"
          className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors duration-200"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Users
        </Link>
      </div>

      {/* Author Profile Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
        <div className="flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-8">
          {/* Avatar */}
          <div className="flex-shrink-0">
            <img
              src={author?.avatar_url || defaultImage}
              alt={author?.full_name || 'Author'}
              className="w-32 h-32 rounded-full object-cover border-4 border-gray-200"
              onError={(e) => { e.target.src = defaultImage; }}
            />
          </div>

          {/* Author Info */}
          <div className="flex-1">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  {author?.full_name || 'Unknown Author'}
                </h1>
                <div className="flex items-center space-x-4 mb-4">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getRoleColor(author?.role)}`}>
                    <User className="w-4 h-4 mr-1" />
                    {author?.role || 'user'}
                  </span>
                  {author?.is_active === false && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800 border-yellow-200">
                      Inactive
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Contact Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="flex items-center text-gray-600">
                <Mail className="w-5 h-5 mr-3" />
                <span>{author?.email}</span>
              </div>
              {author?.created_at && (
                <div className="flex items-center text-gray-600">
                  <Calendar className="w-5 h-5 mr-3" />
                  <span>Member since {formatDate(author.created_at)}</span>
                </div>
              )}
            </div>

            {/* Bio */}
            {author?.bio && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">About</h3>
                <p className="text-gray-700 leading-relaxed">{author.bio}</p>
              </div>
            )}

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-6 border-t border-gray-200">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{authorItems.length}</div>
                <div className="text-sm text-gray-600">Items</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {authorItems.reduce((sum, item) => sum + (item.views || 0), 0).toLocaleString()}
                </div>
                <div className="text-sm text-gray-600">Total Views</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {authorItems.filter(item => item.status === 'published').length}
                </div>
                <div className="text-sm text-gray-600">Published</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Author's Articles */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            Items by {author?.full_name || 'this Author'}
          </h2>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <FileText className="w-4 h-4" />
            <span>{authorItems.length} items</span>
          </div>
        </div>

        {itemsLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        ) : authorItems.length > 0 ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {authorItems.map((item) => (
                <ItemCard key={item.id} item={item} />
              ))}
            </div>
            
            {totalPages > 1 && (
              <div className="mt-8">
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  totalItems={totalItems}
                  itemsPerPage={pageSize}
                  onPageChange={handlePageChange}
                />
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No items yet</h3>
            <p className="text-gray-500">
              {author?.full_name || 'This author'} hasn't published any items yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthorProfile;

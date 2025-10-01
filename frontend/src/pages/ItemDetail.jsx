import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Calendar, User, Tag, Edit, Trash2, ArrowLeft } from 'lucide-react';
import { itemService } from '../services/itemService';
import { authService } from '../services/authService';
import { getAppConfig } from '../config/appConfig';
import ContentViewer from '../components/ContentViewer';
import defaultImage from '../imgs/PDZ.jpg';

const ItemDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const hasFetched = useRef(false);
  const currentId = useRef(null);
  const hasTrackedView = useRef(false);
  const appConfig = getAppConfig();
  const isAuthenticated = authService.isAuthenticated();

  useEffect(() => {
    const fetchItem = async () => {
      // Reset if ID changed
      if (currentId.current !== id) {
        hasFetched.current = false;
        hasTrackedView.current = false;
        currentId.current = id;
      }
      
      if (hasFetched.current) return;
      hasFetched.current = true;
      
      try {
        const response = await itemService.getItemById(id);
        setItem(response.data);
        
        // Track view only once per item visit
        if (!hasTrackedView.current && response.data) {
          hasTrackedView.current = true;
          // Track view asynchronously without waiting for response
          itemService.incrementViews(id).catch(error => {
            console.warn('Failed to track view:', error);
          });
        }
      } catch (error) {
        console.error('Failed to fetch item:', error);
        setError('Item not found');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchItem();
    }
  }, [id]);

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return;
    }

    try {
      await itemService.deleteItem(id);
      navigate('/items');
    } catch (error) {
      console.error('Failed to delete item:', error);
      alert('Failed to delete item. Please try again.');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderMetaFields = () => {
    // Get meta field names from config (VITE_META_FIELDS)
    const configMetaFields = appConfig.metaFieldNames || [];
    
    if (configMetaFields.length === 0) {
      return null; // No meta fields configured
    }

    return (
      <div className="bg-gray-50 rounded-lg p-6 mb-8 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
          Additional Information
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {configMetaFields.map((fieldName) => {
            let value = null;
            
            // First, check if the field exists in meta_field
            if (item.meta_field && item.meta_field.hasOwnProperty(fieldName)) {
              value = item.meta_field[fieldName];
            }
            // If not found in meta_field, check directly in the item
            else if (item.hasOwnProperty(fieldName)) {
              value = item[fieldName];
            }
            
            // Determine display value
            const displayValue = value === null || value === undefined || value === '' 
              ? 'Empty value' 
              : (typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value));

            return (
              <div key={fieldName} className="flex justify-between py-2 border-b border-gray-200 last:border-b-0">
                <span className="font-medium text-gray-700 capitalize">
                  {fieldName.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                </span>
                <span className={`text-right ml-4 ${displayValue === 'Empty value' ? 'text-gray-400 italic' : 'text-gray-600'}`}>
                  {displayValue}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-300 rounded mb-4"></div>
          <div className="h-64 bg-gray-300 rounded mb-6"></div>
          <div className="h-4 bg-gray-300 rounded mb-2"></div>
          <div className="h-4 bg-gray-300 rounded mb-2"></div>
          <div className="h-4 bg-gray-300 rounded"></div>
        </div>
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {error || 'Item not found'}
          </h1>
          <Link
            to="/items"
            className={`btn-primary ${appConfig.theme.primary} inline-flex items-center`}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Items
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <div className="mb-6">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors duration-200"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back
        </button>
      </div>

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-8">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <Tag className="w-4 h-4 mr-2 text-gray-400" />
            <span className={`text-sm font-medium ${appConfig.theme.accent}`}>
              {item.category}
            </span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {item.title}
          </h1>
          <div className="flex items-center text-sm text-gray-500 space-x-6">
            <div className="flex items-center">
              <User className="w-4 h-4 mr-1" />
              <Link 
                to={`/author/${item.author_id}`}
                className="text-blue-600 hover:text-blue-800 hover:underline transition-colors font-medium"
              >
                {item.author_name || `Author ${item.author_id?.slice(0, 8)}`}
              </Link>
            </div>
            <div className="flex items-center">
              <Calendar className="w-4 h-4 mr-1" />
              <span>{formatDate(item.created_at || item.createdAt)}</span>
            </div>
          </div>
        </div>

        {/* Actions */}
        {isAuthenticated && (
          <div className="flex items-center space-x-3 mt-4 sm:mt-0">
            <Link
              to={`/items/${id}/edit`}
              className="btn-secondary inline-flex items-center"
            >
              <Edit className="w-4 h-4 mr-2" />
              Edit
            </Link>
            <button
              onClick={handleDelete}
              className="btn-secondary text-red-600 hover:text-red-700 inline-flex items-center"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Delete
            </button>
          </div>
        )}
      </div>

      {/* Images */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {item.images && item.images.length > 0 ? (
            item.images.map((image, index) => (
              <img
                key={index}
                src={image}
                alt={`${item.title} - Image ${index + 1}`}
                className="w-full h-64 object-cover rounded-lg"
                onError={(e) => {
                  e.target.src = defaultImage;
                }}
              />
            ))
          ) : (
            <img
              src={defaultImage}
              alt={item.title}
              className="w-full h-64 object-cover rounded-lg"
            />
          )}
        </div>
      </div>

      {/* Abstract */}
      {item.abstract && (
        <div className="bg-blue-50 border-l-4 border-blue-400 p-6 mb-8">
          <div className="text-blue-800 font-medium">Abstract</div>
          <div className="text-blue-700 mt-2">{item.abstract}</div>
        </div>
      )}

      {/* Meta Fields */}
      {renderMetaFields()}

      {/* Content */}
      <div className="mb-8">
        <ContentViewer content={item.content} title="Article Content" />
      </div>

      {/* Tags */}
      {item.tags && item.tags.length > 0 && (
        <div className="mt-8 pt-8 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {item.tags.map((tag, index) => (
              <span
                key={index}
                className="inline-block px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors duration-200"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-12 pt-8 border-t border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-gray-500">
          <div>
            Status: <span className="font-medium capitalize">{item.status || 'published'}</span>
          </div>
          <div>
            Last updated: {formatDate(item.updated_at || item.updatedAt || item.created_at || item.createdAt)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItemDetail;


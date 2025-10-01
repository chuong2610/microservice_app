import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Save, X, Plus } from 'lucide-react';
import { itemService } from '../services/itemService';
import { getAppConfig } from '../config/appConfig';
import { useAuth } from '../hooks/useAuth';
import { authService } from '../services/authService';
import MetaFieldForm from '../components/MetaFieldForm';

const CreateItem = () => {
  const navigate = useNavigate();
  const appConfig = getAppConfig();
  const { isAuthenticated, user, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    abstract: '',
    content: '',
    category: '',
    tags: '',
    images: [''],
    status: 'draft',
    author_id: ''
  });
  const [metaFields, setMetaFields] = useState({});

  useEffect(() => {
    // Check authentication and get user info
    const checkAuth = async () => {
      if (!isAuthenticated) {
        navigate('/login');
        return;
      }

      try {
        const token = authService.getCurrentToken();
        if (token) {
          const response = await authService.decodeToken(token);
          if (response.status_code === 200 && response.data) {
            setCurrentUser(response.data);
            setFormData(prev => ({
              ...prev,
              author_id: response.data.sub?.id || response.data.user_id || ''
            }));
          } else {
            navigate('/login');
          }
        } else {
          navigate('/login');
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        navigate('/login');
      }
    };

    if (!authLoading) {
      checkAuth();
    }
  }, [isAuthenticated, authLoading, navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (index, value) => {
    const newImages = [...formData.images];
    newImages[index] = value;
    setFormData(prev => ({
      ...prev,
      images: newImages
    }));
  };

  const addImageField = () => {
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, '']
    }));
  };

  const removeImageField = (index) => {
    if (formData.images.length > 1) {
      const newImages = formData.images.filter((_, i) => i !== index);
      setFormData(prev => ({
        ...prev,
        images: newImages
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.author_id) {
      alert('User authentication required. Please log in again.');
      navigate('/login');
      return;
    }

    setLoading(true);

    try {
      // Process form data
      const itemData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
        images: formData.images.filter(img => img.trim()),
        meta_field: metaFields
      };

      console.log('Creating item with data:', itemData);
      const response = await itemService.createItem(itemData);
      
      if (response.status_code === 200 && response.data) {
        navigate(`/items/${response.data.id}`);
      } else {
        throw new Error(response.message || 'Failed to create item');
      }
    } catch (error) {
      console.error('Failed to create item:', error);
      alert(error.message || 'Failed to create item. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Show loading while checking authentication
  if (authLoading || (!currentUser && isAuthenticated)) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Create New {appConfig.id === 'blog' ? 'Article' : 'Item'}
        </h1>
        <p className="mt-2 text-gray-600">
          Fill in the details below to create a new {appConfig.id === 'blog' ? 'article' : 'item'}.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Basic Information</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Title */}
            <div className="md:col-span-2">
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="input-field"
                placeholder="Enter a compelling title"
                required
              />
            </div>

            {/* Category */}
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                Category <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className="input-field"
                placeholder="e.g., Technology, Fashion, Food"
                required
              />
            </div>

            {/* Status */}
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="input-field"
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>

            {/* Abstract */}
            <div className="md:col-span-2">
              <label htmlFor="abstract" className="block text-sm font-medium text-gray-700 mb-2">
                Abstract <span className="text-red-500">*</span>
              </label>
              <textarea
                id="abstract"
                name="abstract"
                value={formData.abstract}
                onChange={handleInputChange}
                rows={3}
                className="input-field"
                placeholder="Brief description or summary"
                required
              />
            </div>

            {/* Tags */}
            <div className="md:col-span-2">
              <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
                Tags
              </label>
              <input
                type="text"
                id="tags"
                name="tags"
                value={formData.tags}
                onChange={handleInputChange}
                className="input-field"
                placeholder="Enter tags separated by commas (e.g., react, javascript, tutorial)"
              />
            </div>
          </div>
        </div>

        {/* Images */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Images</h2>
            <button
              type="button"
              onClick={addImageField}
              className="btn-secondary inline-flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Image
            </button>
          </div>

          <div className="space-y-4">
            {formData.images.map((image, index) => (
              <div key={index} className="flex items-center space-x-3">
                <input
                  type="url"
                  value={image}
                  onChange={(e) => handleImageChange(index, e.target.value)}
                  className="input-field flex-1"
                  placeholder="Enter image URL"
                />
                {formData.images.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeImageField(index)}
                    className="p-2 text-red-600 hover:text-red-700"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Content</h2>
          <div>
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
              Content <span className="text-red-500">*</span>
            </label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleInputChange}
              rows={12}
              className="input-field"
              placeholder="Write your content here..."
              required
            />
          </div>
        </div>

        {/* Meta Fields */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <MetaFieldForm
            metaFields={metaFields}
            onChange={setMetaFields}
          />
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className={`btn-primary ${appConfig.theme.primary} inline-flex items-center`}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Creating...
              </>
            ) : (
              <>
                <Save className="w-4 h-4 mr-2" />
                Create {appConfig.id === 'blog' ? 'Article' : 'Item'}
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateItem;


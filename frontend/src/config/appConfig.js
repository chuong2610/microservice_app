// App configuration based on environment
const appConfigs = {
  blog: {
    id: 'blog',
    name: 'Blog Platform',
    metaFields: [
      { name: 'excerpt', type: 'textarea', label: 'Excerpt', required: false },
      { name: 'readTime', type: 'number', label: 'Read Time (minutes)', required: false },
      { name: 'featured', type: 'boolean', label: 'Featured Article', required: false }
    ],
    theme: {
      primary: 'bg-blue-600 hover:bg-blue-700',
      secondary: 'bg-gray-100 hover:bg-gray-200',
      accent: 'text-blue-600'
    }
  },
  ecommerce: {
    id: 'ecommerce',
    name: 'E-Commerce Platform',
    metaFields: [
      { name: 'price', type: 'number', label: 'Price ($)', required: true, step: '0.01' },
      { name: 'place', type: 'text', label: 'Location', required: false },
      { name: 'ratings', type: 'number', label: 'Ratings (1-5)', required: false, min: 1, max: 5, step: '0.1' },
      { name: 'brand', type: 'text', label: 'Brand', required: false },
      { name: 'availability', type: 'select', label: 'Availability', required: true, options: ['In Stock', 'Out of Stock', 'Pre-order'] },
      { name: 'discount', type: 'number', label: 'Discount (%)', required: false, min: 0, max: 100 }
    ],
    theme: {
      primary: 'bg-green-600 hover:bg-green-700',
      secondary: 'bg-gray-100 hover:bg-gray-200',
      accent: 'text-green-600'
    }
  }
};

// Get current app configuration
const getAppConfig = () => {
  const appType = import.meta.env.VITE_APP_CONFIG || 'blog';
  const envAppId = import.meta.env.VITE_APP_ID;
  const envAppName = import.meta.env.VITE_APP_NAME;
  const envMetaFields = import.meta.env.VITE_META_FIELDS;
  
  const config = appConfigs[appType] || appConfigs.blog;
  
  // Parse meta fields from environment if provided
  let metaFieldNames = [];
  if (envMetaFields) {
    try {
      metaFieldNames = JSON.parse(envMetaFields);
    } catch (error) {
      console.warn('Failed to parse VITE_META_FIELDS:', error);
      metaFieldNames = [];
    }
  }
  
  // Build final config
  const finalConfig = { ...config };
  
  // Override with environment variables if provided
  if (envAppId && typeof envAppId === 'string') {
    finalConfig.id = envAppId;
  }
  
  if (envAppName && typeof envAppName === 'string') {
    finalConfig.name = envAppName;
  }
  
  if (metaFieldNames.length > 0) {
    finalConfig.metaFieldNames = metaFieldNames;
  }
  
  return finalConfig;
};

// API Configuration
export const apiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 0, // No timeout - wait indefinitely for search results
  headers: {
    'Content-Type': 'application/json',
  }
};

export { appConfigs, getAppConfig };

import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { getAppConfig } from '../config/appConfig';
import { itemService } from '../services/itemService';
import ItemCard from '../components/ItemCard';

const Home = () => {
  const [featuredItems, setFeaturedItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const hasFetched = useRef(false);
  const appConfig = getAppConfig();

  useEffect(() => {
    const fetchFeaturedItems = async () => {
      if (hasFetched.current) return;
      hasFetched.current = true;
      
      try {
        const response = await itemService.getItems(1, 6);
        setFeaturedItems(response.data?.items || []);
      } catch (error) {
        console.error('Failed to fetch featured items:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedItems();
  }, []);


  return (
    <div>
      {/* Hero Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              Welcome to{' '}
              <span className={appConfig.theme.accent}>
                {appConfig.name}
              </span>
            </h1>
            <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-500">
              {appConfig.id === 'blog' 
                ? 'Discover amazing items, insights, and stories from our community of writers.'
                : 'Explore our curated collection of products and find exactly what you need.'
              }
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <Link
                to="/items"
                className={`btn-primary ${appConfig.theme.primary} flex items-center`}
              >
                Explore Items
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/create"
                className="btn-secondary"
              >
                Create New Item
              </Link>
            </div>
          </div>
        </div>
      </div>


      {/* Featured Items Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">
              Featured Items
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              {appConfig.id === 'blog' 
                ? 'Stay updated with our latest blog posts and insights'
                : 'Check out our most popular and trending products'
              }
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="card animate-pulse">
                  <div className="h-48 bg-gray-300"></div>
                  <div className="p-6">
                    <div className="h-4 bg-gray-300 rounded mb-2"></div>
                    <div className="h-6 bg-gray-300 rounded mb-2"></div>
                    <div className="h-4 bg-gray-300 rounded mb-4"></div>
                    <div className="h-4 bg-gray-300 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : featuredItems.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredItems.map((item) => (
                <ItemCard key={item.id} item={item} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 text-lg">
                No items available yet.
              </div>
              <Link
                to="/create"
                className={`mt-4 inline-flex items-center btn-primary ${appConfig.theme.primary}`}
              >
                Create the First Item
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </div>
          )}

          {featuredItems.length > 0 && (
            <div className="text-center mt-12">
              <Link
                to="/items"
                className={`btn-primary ${appConfig.theme.primary} inline-flex items-center`}
              >
                View All Items
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;

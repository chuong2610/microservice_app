import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { Filter, Grid, List, Search, X } from 'lucide-react';
import { itemService } from '../services/itemService';
import { searchService } from '../services/searchService';
import { getAppConfig } from '../config/appConfig';
import ItemCard from '../components/ItemCard';
import Pagination from '../components/Pagination';

const ItemList = () => {
  const { category, authorId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  // Initialize current page from URL to avoid initial fetch for page 1
  const [currentPage, setCurrentPage] = useState(() => {
    const page = parseInt(searchParams.get('page'));
    return Number.isNaN(page) || page <= 0 ? 1 : page;
  });
  const [totalPages, setTotalPages] = useState(0);
  const [totalItems, setTotalItems] = useState(0);
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('newest');
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  
  const appConfig = getAppConfig();
  const pageSize = 12;

  // Sync state if URL param changes (e.g., browser navigation)
  useEffect(() => {
    const pageFromUrl = parseInt(searchParams.get('page'));
    const normalized = Number.isNaN(pageFromUrl) || pageFromUrl <= 0 ? 1 : pageFromUrl;
    if (normalized !== currentPage) {
      setCurrentPage(normalized);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  const fetchItems = async (page = 1) => {
    setLoading(true);
    try {
      let response;
      
      if (isSearching && searchQuery.trim()) {
        // Use search items API
        response = await searchService.searchItems(searchQuery, {
          k: pageSize * 5, // Get more results for better pagination
          pageIndex: page - 1,
          pageSize: pageSize
        });
        
        if (response && response.results) {
          const searchResults = response.results || [];
          const pagination = response.pagination || {};
          
          // Fetch full item details for each search result
          let processedItems = [];
          if (searchResults.length > 0) {
            try {
              const itemIds = searchResults.map(item => item.id || item.doc?.id);
              const itemDetailsPromises = itemIds.map(id => 
                itemService.getItemById(id).catch(error => {
                  console.warn(`Failed to fetch item ${id}:`, error);
                  return null;
                })
              );
              const itemDetails = await Promise.all(itemDetailsPromises);
              processedItems = itemDetails
                .filter(response => response && response.status_code === 200)
                .map((response, index) => {
                  const originalSearchResult = searchResults[index];
                  return {
                    ...response.data, // Full item data
                    _score: originalSearchResult?._final || originalSearchResult?._bm25 || 0
                  };
                });
            } catch (error) {
              console.error('Failed to fetch item details:', error);
              // Fallback to search results data
              processedItems = searchResults.map(item => ({
                ...item.doc,
                id: item.doc?.id || item.id,
                _score: item._final || item._bm25 || 0
              }));
            }
          }
          
          setItems(processedItems);
          setTotalPages(pagination.total_pages || Math.ceil(processedItems.length / pageSize));
          setTotalItems(pagination.total_results || processedItems.length);
        } else {
          setItems([]);
          setTotalPages(0);
          setTotalItems(0);
        }
      } else {
        // Use regular item service
        if (category) {
          response = await itemService.getItemsByCategory(category, page, pageSize);
        } else if (authorId) {
          response = await itemService.getItemsByAuthor(authorId, page, pageSize);
        } else {
          response = await itemService.getItems(page, pageSize);
        }

        if (response.data) {
          setItems(response.data.items || []);
          setTotalPages(response.data.total_pages || 0);
          setTotalItems(response.data.total_items || 0);
        }
      }
    } catch (error) {
      console.error('Failed to fetch items:', error);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setIsSearching(true);
      setCurrentPage(1);
      fetchItems(1);
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    setIsSearching(false);
    setCurrentPage(1);
    fetchItems(1);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  useEffect(() => {
    let isCancelled = false;
    const run = async () => {
      setLoading(true);
      try {
        await fetchItems(currentPage);
      } finally {
        if (!isCancelled) setLoading(false);
      }
    };
    run();
    return () => {
      isCancelled = true;
    };
  }, [category, authorId, currentPage]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    setSearchParams({ page: page.toString() });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getPageTitle = () => {
    if (category) return `Items in "${category}"`;
    if (authorId) return `Items by Author`;
    return 'All Items';
  };

  const sortItems = (items, sortBy) => {
    const sortedItems = [...items];
    switch (sortBy) {
      case 'newest':
        return sortedItems.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      case 'oldest':
        return sortedItems.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
      case 'title':
        return sortedItems.sort((a, b) => a.title.localeCompare(b.title));
      default:
        return sortedItems;
    }
  };

  const sortedItems = sortItems(items, sortBy);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {getPageTitle()}
          </h1>
          <p className="mt-2 text-gray-600">
            {totalItems} {totalItems === 1 ? 'item' : 'items'} found
          </p>
        </div>

        {/* Controls */}
        <div className="mt-4 sm:mt-0 flex items-center space-x-4">
          {/* Search */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center">
              <button
                onClick={handleSearch}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                type="button"
              >
                <Search className="h-5 w-5" />
              </button>
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search items..."
              className="block w-64 pl-10 pr-10 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            {searchQuery && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <button
                  onClick={clearSearch}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            )}
          </div>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="input-field w-auto"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="title">Title A-Z</option>
          </select>

          {/* View Mode */}
          <div className="flex items-center border border-gray-300 rounded-lg">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 ${
                viewMode === 'grid'
                  ? `${appConfig.theme.primary} text-white`
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 ${
                viewMode === 'list'
                  ? `${appConfig.theme.primary} text-white`
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8' : 'space-y-6'}>
          {[...Array(pageSize)].map((_, index) => (
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
      )}

      {/* Items Grid/List */}
      {!loading && sortedItems.length > 0 && (
        <div className={
          viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'
            : 'space-y-6'
        }>
          {sortedItems.map((item) => (
            <ItemCard key={item.id} item={item} />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && sortedItems.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-lg mb-4">
            No items found
          </div>
          <p className="text-gray-500 mb-6">
            {category 
              ? `No items found in the "${category}" category.`
              : authorId
              ? 'This author hasn\'t published any items yet.'
              : 'No items have been created yet.'
            }
          </p>
        </div>
      )}

      {/* Pagination */}
      {!loading && totalPages > 1 && (
        <div className="mt-12">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalItems}
            itemsPerPage={pageSize}
            onPageChange={handlePageChange}
          />
        </div>
      )}
    </div>
  );
};

export default ItemList;

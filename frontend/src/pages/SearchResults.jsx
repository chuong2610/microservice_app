import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, ArrowLeft, Grid, List } from 'lucide-react';
import { searchService } from '../services/searchService';
import { itemService } from '../services/itemService';
import { getAppConfig } from '../config/appConfig';
import ItemCard from '../components/ItemCard';
import Pagination from '../components/Pagination';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [results, setResults] = useState({ items: [], authors: [] });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('items');
  const [viewMode, setViewMode] = useState('grid');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalResults, setTotalResults] = useState(0);
  const hasFetched = useRef(false);
  const currentQuery = useRef('');
  const currentPageRef = useRef(1);
  const appConfig = getAppConfig();
  const pageSize = 12;

  useEffect(() => {
    const fetchSearchResults = async () => {
      if (!query.trim()) {
        setResults({ items: [], authors: [] });
        setLoading(false);
        return;
      }

      // Check if we should skip this request
      const searchKey = `${query}-${currentPage}`;
      if (currentQuery.current === query && currentPageRef.current === currentPage && hasFetched.current) {
        console.log('Skipping duplicate search for:', query, 'page:', currentPage);
        return;
      }

      // Reset if query or page changed
      if (currentQuery.current !== query || currentPageRef.current !== currentPage) {
        hasFetched.current = false;
        currentQuery.current = query;
        currentPageRef.current = currentPage;
      }

      if (hasFetched.current) {
        console.log('Already fetched for:', query, 'page:', currentPage);
        return;
      }
      
      hasFetched.current = true;
      setLoading(true);
      // Reset results while loading to prevent showing stale data
      setResults({ items: [], authors: [] });
      setTotalPages(0);
      setTotalResults(0);
      
      try {
        console.log('Starting search for:', query);
        const response = await searchService.searchAll(query, { 
          k: 50, 
          pageIndex: currentPage - 1, 
          pageSize: pageSize 
        });
        
        console.log('Search completed, response:', response);
        
        // Parse the response structure: {item: {...}, author: {...}}
        if (response) {
          const itemsData = response.item || {};
          const authorsData = response.author || {};
          
          const items = itemsData.results || [];
          const authors = authorsData.results || [];
          
          // Extract item IDs and fetch full details
          const itemIds = items.map(item => item.id || item.doc?.id);
          
          // Fetch full item details
          let processedItems = [];
          if (itemIds.length > 0) {
            try {
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
                  const originalSearchResult = items[index];
                  return {
                    ...response.data,
                    // Add search metadata
                    _score: originalSearchResult?._final || originalSearchResult?._bm25 || 0
                  };
                });
            } catch (error) {
              console.error('Failed to fetch item details:', error);
              // Fallback to search results data
              processedItems = items.map(item => ({
                ...item.doc,
                id: item.doc?.id || item.id,
                _score: item._final || item._bm25 || 0
              }));
            }
          }
          
          const processedAuthors = authors.map(author => ({
            ...author.doc,
            id: author.doc?.id || author.id,
            name: author.doc?.full_name || author.doc?.name,
            // Add search metadata if needed
            _score: author._final || author._bm25 || 0
          }));
          
          setResults({
            items: processedItems,
            authors: processedAuthors
          });
          
          // Use pagination info from the API response
          const itemsPagination = itemsData.pagination || {};
          const totalItemsCount = itemsPagination.total_results || 0;
          const totalItemsPages = itemsPagination.total_pages || 0;
          
          // Set pagination based on items (since that's usually the main search target)
          setTotalPages(totalItemsPages);
          setTotalResults(totalItemsCount);
          
          console.log('Search results set:', {
            items: processedItems.length,
            authors: processedAuthors.length,
            processedItems,
            processedAuthors
          });
        }
      } catch (error) {
        console.error('Search failed:', error);
        setResults({ items: [], authors: [] });
        setTotalPages(0);
        setTotalResults(0);
      } finally {
        setLoading(false);
      }
    };

    fetchSearchResults();
  }, [query, currentPage]);

  const handlePageChange = (page) => {
    // Reset fetch guard when page changes
    hasFetched.current = false;
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderItems = () => {
    if (loading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[...Array(6)].map((_, index) => (
            <div key={index} className="card animate-pulse">
              <div className="h-48 bg-gray-300"></div>
              <div className="p-6">
                <div className="h-4 bg-gray-300 rounded mb-2"></div>
                <div className="h-6 bg-gray-300 rounded mb-2"></div>
                <div className="h-4 bg-gray-300 rounded mb-4"></div>
              </div>
            </div>
          ))}
        </div>
      );
    }

    if (results.items.length === 0) {
      return (
        <div className="text-center py-12">
          <Search className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No items found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Try adjusting your search terms or browse all items.
          </p>
          <div className="mt-6">
            <Link
              to="/items"
              className={`btn-primary ${appConfig.theme.primary} inline-flex items-center`}
            >
              Browse All Items
            </Link>
          </div>
        </div>
      );
    }

    const gridClass = viewMode === 'grid' 
      ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'
      : 'space-y-6';

    return (
      <div className={gridClass}>
        {results.items.map((item) => (
          <ItemCard key={item.id} item={item} />
        ))}
      </div>
    );
  };

  const renderAuthors = () => {
    if (loading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, index) => (
            <div key={index} className="card animate-pulse">
              <div className="p-6">
                <div className="h-6 bg-gray-300 rounded mb-2"></div>
                <div className="h-4 bg-gray-300 rounded mb-4"></div>
                <div className="h-4 bg-gray-300 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      );
    }

    if (results.authors.length === 0) {
      return (
        <div className="text-center py-12">
          <Search className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No authors found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Try adjusting your search terms.
          </p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.authors.map((author, index) => (
          <div key={index} className="card">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                <Link
                  to={`/author/${author.id}`}
                  className="hover:text-gray-700 transition-colors"
                >
                  {author.name || `Author ${author.id?.slice(0, 8)}`}
                </Link>
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {author.bio || 'No bio available'}
              </p>
              <div className="text-xs text-gray-500">
                Items: {author.item_count || 0}
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <div className="mb-6">
        <Link
          to="/"
          className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors duration-200"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Home
        </Link>
      </div>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Search Results
        </h1>
        <p className="text-gray-600">
          Results for: <span className="font-medium">"{query}"</span>
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('items')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'items'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Items ({loading ? '...' : results.items.length})
          </button>
          <button
            onClick={() => setActiveTab('authors')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'authors'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Authors ({loading ? '...' : results.authors.length})
          </button>
        </nav>
      </div>

      {/* View Controls (only for items) */}
      {activeTab === 'items' && !loading && results.items.length > 0 && (
        <div className="flex items-center justify-between mb-6">
          <div className="text-sm text-gray-500">
            {totalResults > 0 ? (
              <>
                Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, totalResults)} of {totalResults} results
              </>
            ) : (
              `${results.items.length} items found`
            )}
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md ${
                viewMode === 'grid'
                  ? 'bg-gray-200 text-gray-900'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-md ${
                viewMode === 'list'
                  ? 'bg-gray-200 text-gray-900'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      <div className="mb-8">
        {activeTab === 'items' ? renderItems() : renderAuthors()}
      </div>

      {/* Pagination (only for items) */}
      {activeTab === 'items' && !loading && totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          totalItems={totalResults}
          itemsPerPage={pageSize}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};

export default SearchResults;

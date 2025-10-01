import api from './api';

export const searchService = {
  // Search all (items and authors)
  async searchAll(query, options = {}) {
    const { k = 10, pageIndex, pageSize } = options;
    const params = { q: query, k };
    
    if (pageIndex !== undefined) params.page_index = pageIndex;
    if (pageSize !== undefined) params.page_size = pageSize;
    
    const response = await api.get('/search', { params });
    return response;
  },

  // Search items only
  async searchItems(query, options = {}) {
    const { k = 10, pageIndex, pageSize } = options;
    const params = { q: query, k };
    
    if (pageIndex !== undefined) params.page_index = pageIndex;
    if (pageSize !== undefined) params.page_size = pageSize;
    
    const response = await api.get('/search/items', { params });
    return response;
  },

  // Search authors only
  async searchAuthors(query, options = {}) {
    const { k = 10, pageIndex, pageSize } = options;
    const params = { q: query, k };
    
    if (pageIndex !== undefined) params.page_index = pageIndex;
    if (pageSize !== undefined) params.page_size = pageSize;
    
    const response = await api.get('/search/authors', { params });
    return response;
  }
};

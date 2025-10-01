import api from './api';
import { requestCache } from '../utils/requestCache';

export const itemService = {
  // Get paginated items
  async getItems(pageNumber = 1, pageSize = 10) {
    const key = requestCache.createKey('/items', { page_number: pageNumber, page_size: pageSize });
    return requestCache.getOrCreateRequest(key, () =>
      api.get('/items', {
        params: { page_number: pageNumber, page_size: pageSize }
      })
    );
  },

  // Get item by ID
  async getItemById(itemId) {
    const key = requestCache.createKey(`/items/${itemId}`, {});
    return requestCache.getOrCreateRequest(key, () =>
      api.get(`/items/${itemId}`)
    );
  },

  // Get items by author
  async getItemsByAuthor(authorId, pageNumber = 1, pageSize = 10) {
    const key = requestCache.createKey(`/items/author/${authorId}`, { page_number: pageNumber, page_size: pageSize });
    return requestCache.getOrCreateRequest(key, () =>
      api.get(`/items/author/${authorId}`, {
        params: { page_number: pageNumber, page_size: pageSize }
      })
    );
  },

  // Get items by category
  async getItemsByCategory(category, pageNumber = 1, pageSize = 10) {
    const key = requestCache.createKey(`/items/category/${category}`, { page_number: pageNumber, page_size: pageSize });
    return requestCache.getOrCreateRequest(key, () =>
      api.get(`/items/category/${category}`, {
        params: { page_number: pageNumber, page_size: pageSize }
      })
    );
  },

  // Create new item
  async createItem(itemData) {
    const response = await api.post('/items', itemData);
    return response;
  },

  // Update item
  async updateItem(itemId, updateData) {
    const response = await api.put(`/items/${itemId}`, updateData);
    return response;
  },

  // Delete item
  async deleteItem(itemId) {
    const response = await api.delete(`/items/${itemId}`);
    return response;
  },

  // Increment item views
  async incrementViews(itemId) {
    const response = await api.post(`/items/${itemId}/view`);
    return response;
  }
};


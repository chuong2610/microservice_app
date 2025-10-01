import api from './api';

export const userService = {
  // Get user by ID
  async getUserById(userId) {
    const response = await api.get(`/users/${userId}`);
    return response;
  },

  // Get paginated users
  async getUsers(pageNumber = 1, pageSize = 10) {
    const response = await api.get('/users', {
      params: { page_number: pageNumber, page_size: pageSize }
    });
    return response;
  },

  // Create user
  async createUser(userData) {
    const response = await api.post('/users', userData);
    return response;
  },

  // Update user
  async updateUser(userId, updateData) {
    const response = await api.put(`/users/${userId}`, updateData);
    return response;
  },

  // Deactivate user
  async deactivateUser(userId) {
    const response = await api.put(`/users/${userId}/deactivate`);
    return response;
  },

  // Activate user
  async activateUser(userId) {
    const response = await api.put(`/users/${userId}/activate`);
    return response;
  },

  // Delete user
  async deleteUser(userId) {
    const response = await api.delete(`/users/${userId}`);
    return response;
  }
};



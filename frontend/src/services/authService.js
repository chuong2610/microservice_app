import api from './api';

export const authService = {
  // Login
  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    if (response.status_code === 200 && response.data?.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
    }
    return response;
  },

  // Register
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response;
  },

  // Google login
  async loginWithGoogle(idToken) {
    const response = await api.post('/auth/login/google', { id_token: idToken });
    if (response.status_code === 200 && response.data?.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
    }
    return response;
  },

  // Refresh token
  async refreshToken(userId, refreshToken) {
    const response = await api.post('/auth/refresh', { 
      user_id: userId, 
      refresh_token: refreshToken 
    });
    if (response.status_code === 200 && response.data?.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
    }
    return response;
  },

  // Decode token
  async decodeToken(token) {
    const response = await api.post('/auth/decode-token', { token });
    return response;
  },

  // Logout
  async logout(userId) {
    const response = await api.post('/auth/logout', null, {
      params: { user_id: userId }
    });
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
    return response;
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },

  // Get current user token
  getCurrentToken() {
    return localStorage.getItem('authToken');
  }
};

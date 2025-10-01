import axios from 'axios';
import { apiConfig, getAppConfig } from '../config/appConfig';

// Create axios instance
const api = axios.create({
  baseURL: apiConfig.baseURL,
  timeout: apiConfig.timeout,
  headers: apiConfig.headers
});

// Request interceptor to add app_id header
api.interceptors.request.use(
  (config) => {
    const appConfig = getAppConfig();
    config.headers['app_id'] = appConfig.id;
    
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Backend returns BaseResponse format: { status_code, data, message }
    // Return the whole response for status checking, but make data easily accessible
    return response.data;
  },
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401) {
      console.log('401 Unauthorized error:', error.config?.url);
      
      // Define public endpoints that should NEVER cause logout
      const publicEndpoints = [
        '/auth/decode-token',
        '/users/',           // User profile viewing
        '/items/',           // Item viewing  
        '/search/',          // Search functionality
        '/auth/login',       // Login endpoint
        '/auth/register',    // Register endpoint
        '/auth/refresh'      // Refresh token endpoint
      ];
      
      // Check if this is a public endpoint
      const isPublicEndpoint = publicEndpoints.some(endpoint => 
        error.config?.url?.includes(endpoint)
      );
      
      if (isPublicEndpoint) {
        console.log('401 error on public endpoint - this is normal, not forcing logout');
        return Promise.reject(error.response?.data || error.message);
      }
      
      // For protected endpoints, try refresh only once
      if (!originalRequest._retry) {
        originalRequest._retry = true;
        
        const refreshToken = localStorage.getItem('refreshToken');
        const currentToken = localStorage.getItem('authToken');
        
        if (refreshToken && currentToken) {
          try {
            console.log('Attempting token refresh for protected endpoint...');
            
            // Extract user ID from current token
            let userId = null;
            try {
              const payload = JSON.parse(atob(currentToken.split('.')[1]));
              userId = payload.sub || payload.user_id || payload.id;
            } catch (e) {
              console.warn('Could not extract user_id from token');
            }
            
            if (userId) {
              // Import authService dynamically to avoid circular dependency
              const { authService } = await import('./authService');
              const refreshResponse = await authService.refreshToken(userId, refreshToken);
              
              if (refreshResponse.status_code === 200) {
                console.log('Token refreshed successfully, retrying request');
                // Update the authorization header and retry
                originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access_token}`;
                return api(originalRequest);
              }
            }
          } catch (refreshError) {
            console.log('Token refresh failed:', refreshError);
          }
        }
        
        // Only force logout if we're on a protected endpoint AND refresh failed
        console.warn('Authentication failed on protected endpoint, but NOT forcing logout');
        console.warn('User must manually logout or login again');
        
        // Don't automatically redirect - let the user handle it
        // This prevents unexpected logouts
      }
    }
    
    return Promise.reject(error.response?.data || error.message);
  }
);

export default api;

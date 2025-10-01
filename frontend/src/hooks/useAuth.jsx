import { useState, useEffect, createContext, useContext, useRef } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const hasCheckedAuth = useRef(false);

  useEffect(() => {
    const checkAuth = () => {
      if (hasCheckedAuth.current) return;
      hasCheckedAuth.current = true;
      
      console.log('Checking authentication state...');
      
      // Simply check if tokens exist in localStorage
      const token = authService.getCurrentToken();
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (token) {
        console.log('Token found, setting authenticated state');
        setIsAuthenticated(true);
        
        // Try to extract user info from token without validation
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          console.log('User info extracted from token:', payload);
          setUser(payload);
        } catch (e) {
          console.warn('Could not extract user info from token, using minimal user data');
          // Set minimal user data to prevent issues
          setUser({ id: 'unknown', email: 'unknown', role: 'user' });
        }
      } else {
        console.log('No token found, user not authenticated');
        setIsAuthenticated(false);
        setUser(null);
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    const response = await authService.login(email, password);
    if (response.status_code === 200) {
      console.log('Login successful, setting auth state');
      setIsAuthenticated(true);
      
      // Use user data from login response or extract from token
      if (response.data.user) {
        console.log('Using user data from login response');
        setUser(response.data.user);
      } else if (response.data.access_token) {
        console.log('Extracting user data from access token');
        try {
          const payload = JSON.parse(atob(response.data.access_token.split('.')[1]));
          setUser(payload);
        } catch (error) {
          console.warn('Could not extract user from token, using minimal data');
          setUser({ id: email, email: email, role: 'user' });
        }
      } else {
        console.warn('No user data or token in login response');
        setUser({ id: email, email: email, role: 'user' });
      }
    }
    return response;
  };

  const logout = async () => {
    console.log('Explicit logout requested by user');
    try {
      if (user?.user_id || user?.id) {
        const userId = user.user_id || user.id;
        console.log('Calling logout API for user:', userId);
        await authService.logout(userId);
      }
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear local state regardless of API call result
      console.log('Clearing authentication state and tokens');
      setIsAuthenticated(false);
      setUser(null);
      localStorage.removeItem('authToken');
      localStorage.removeItem('refreshToken');
    }
  };
  
  // Force logout function for emergency cases only
  const forceLogout = (reason = 'Unknown') => {
    console.warn('Force logout triggered:', reason);
    setIsAuthenticated(false);
    setUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    forceLogout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

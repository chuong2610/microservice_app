// Token expiration test utility
import { authService } from '../services/authService';

export const testTokenExpiration = async () => {
  console.log('=== Token Expiration Test ===');
  
  const token = authService.getCurrentToken();
  if (!token) {
    console.log('No token found');
    return;
  }
  
  console.log('Current token:', token.substring(0, 20) + '...');
  
  try {
    // Decode the token to check expiration
    const response = await authService.decodeToken(token);
    
    if (response.status_code === 200) {
      const payload = response.data;
      const exp = payload.exp;
      const now = Math.floor(Date.now() / 1000);
      const timeLeft = exp - now;
      
      console.log('Token payload:', payload);
      console.log('Token expires at:', new Date(exp * 1000).toLocaleString());
      console.log('Current time:', new Date(now * 1000).toLocaleString());
      console.log('Time left (seconds):', timeLeft);
      console.log('Time left (minutes):', Math.floor(timeLeft / 60));
      
      if (timeLeft <= 0) {
        console.log('❌ Token is EXPIRED');
      } else if (timeLeft < 300) { // Less than 5 minutes
        console.log('⚠️ Token expires soon');
      } else {
        console.log('✅ Token is valid');
      }
    } else {
      console.log('❌ Failed to decode token:', response.message);
    }
  } catch (error) {
    console.log('❌ Error checking token:', error);
  }
};

// Auto-run test in development
if (import.meta.env.DEV) {
  // Test token every 5 minutes in development
  setInterval(testTokenExpiration, 5 * 60 * 1000);
}


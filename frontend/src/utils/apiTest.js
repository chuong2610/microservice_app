import { authService } from '../services/authService';
import { itemService } from '../services/itemService';
import { searchService } from '../services/searchService';
import { userService } from '../services/userService';

export const testApiConnections = async () => {
  console.log('🔍 Testing API Connections...\n');

  const results = {
    auth: { status: '❌', error: null },
    items: { status: '❌', error: null },
    search: { status: '❌', error: null },
    users: { status: '❌', error: null }
  };

  // Test Auth Service Health
  try {
    console.log('Testing Auth Service...');
    const response = await fetch('http://localhost:8000/auth/health');
    if (response.ok) {
      results.auth.status = '✅';
      console.log('✅ Auth Service: Connected');
    } else {
      results.auth.error = `HTTP ${response.status}`;
      console.log('❌ Auth Service: Failed');
    }
  } catch (error) {
    results.auth.error = error.message;
    console.log('❌ Auth Service: Connection failed');
  }

  // Test Items Service
  try {
    console.log('Testing Items Service...');
    const response = await itemService.getItems(1, 5);
    if (response.status_code === 200) {
      results.items.status = '✅';
      console.log('✅ Items Service: Connected');
    } else {
      results.items.error = response.message;
      console.log('❌ Items Service: Failed');
    }
  } catch (error) {
    results.items.error = error.message || error;
    console.log('❌ Items Service: Connection failed');
  }

  // Test Search Service
  try {
    console.log('Testing Search Service...');
    const response = await searchService.searchAll('test', { k: 1 });
    results.search.status = '✅';
    console.log('✅ Search Service: Connected');
  } catch (error) {
    results.search.error = error.message || error;
    console.log('❌ Search Service: Connection failed');
  }

  // Test Users Service
  try {
    console.log('Testing Users Service...');
    const response = await userService.getUsers(1, 5);
    if (response.status_code === 200) {
      results.users.status = '✅';
      console.log('✅ Users Service: Connected');
    } else {
      results.users.error = response.message;
      console.log('❌ Users Service: Failed');
    }
  } catch (error) {
    results.users.error = error.message || error;
    console.log('❌ Users Service: Connection failed');
  }

  console.log('\n📊 API Connection Summary:');
  console.log(`Auth Service: ${results.auth.status}`);
  console.log(`Items Service: ${results.items.status}`);
  console.log(`Search Service: ${results.search.status}`);
  console.log(`Users Service: ${results.users.status}`);

  return results;
};

// Test individual service
export const testService = async (serviceName) => {
  switch (serviceName) {
    case 'auth':
      try {
        const response = await fetch('http://localhost:8000/auth/health');
        return { success: response.ok, status: response.status };
      } catch (error) {
        return { success: false, error: error.message };
      }

    case 'items':
      try {
        const response = await itemService.getItems(1, 1);
        return { success: response.status_code === 200, data: response };
      } catch (error) {
        return { success: false, error: error.message || error };
      }

    case 'search':
      try {
        const response = await searchService.searchAll('test', { k: 1 });
        return { success: true, data: response };
      } catch (error) {
        return { success: false, error: error.message || error };
      }

    case 'users':
      try {
        const response = await userService.getUsers(1, 1);
        return { success: response.status_code === 200, data: response };
      } catch (error) {
        return { success: false, error: error.message || error };
      }

    default:
      return { success: false, error: 'Unknown service' };
  }
};



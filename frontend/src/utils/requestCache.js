// Request deduplication utility to prevent duplicate API calls in StrictMode
class RequestCache {
  constructor() {
    this.cache = new Map();
    this.timeouts = new Map();
  }

  // Create a unique key for the request
  createKey(url, params = {}) {
    const sortedParams = Object.keys(params)
      .sort()
      .map(key => `${key}=${params[key]}`)
      .join('&');
    return `${url}?${sortedParams}`;
  }

  // Check if request is already in progress
  isInProgress(key) {
    return this.cache.has(key);
  }

  // Add request to cache
  addRequest(key, promise) {
    this.cache.set(key, promise);
    
    // Auto-cleanup after 5 seconds
    const timeout = setTimeout(() => {
      this.cache.delete(key);
      this.timeouts.delete(key);
    }, 5000);
    
    this.timeouts.set(key, timeout);

    // Cleanup when promise resolves/rejects
    promise.finally(() => {
      const timeout = this.timeouts.get(key);
      if (timeout) {
        clearTimeout(timeout);
        this.timeouts.delete(key);
      }
      this.cache.delete(key);
    });

    return promise;
  }

  // Get existing request or create new one
  getOrCreateRequest(key, requestFn) {
    if (this.isInProgress(key)) {
      console.log(`[RequestCache] Returning cached request for: ${key}`);
      return this.cache.get(key);
    }

    console.log(`[RequestCache] Creating new request for: ${key}`);
    const promise = requestFn();
    return this.addRequest(key, promise);
  }
}

export const requestCache = new RequestCache();

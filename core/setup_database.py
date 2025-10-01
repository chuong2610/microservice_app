#!/usr/bin/env python3
"""
Database setup script for Core service
Run this to initialize Cosmos DB database and containers
"""

from azure.cosmos import CosmosClient, exceptions
from settings import settings
import json

def setup_database():
    """Initialize Cosmos DB database and containers with sample data"""
    
    print("🔧 Setting up Cosmos DB...")
    print(f"Endpoint: {settings.COSMOS_ENDPOINT}")
    print(f"Database: {settings.COSMOS_DB_NAME}")
    print(f"Container: {settings.COSMOS_CONTAINER_ITEMS}")
    
    try:
        # Create client
        client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
        
        # Create database
        database = client.create_database_if_not_exists(id=settings.COSMOS_DB_NAME)
        print(f"✅ Database '{settings.COSMOS_DB_NAME}' ready")
        
        # Create container
        container = database.create_container_if_not_exists(
            id=settings.COSMOS_CONTAINER_ITEMS,
            partition_key="/id",
            offer_throughput=400
        )
        print(f"✅ Container '{settings.COSMOS_CONTAINER_ITEMS}' ready")
        
        # Add sample data
        sample_items = [
            {
                "id": "sample-blog-1",
                "title": "Welcome to Our Blog Platform",
                "abstract": "This is a sample blog post to test the system",
                "content": "Welcome to our amazing blog platform! This is a sample post to demonstrate the features.",
                "images": ["https://via.placeholder.com/600x300"],
                "tags": ["welcome", "blog", "sample"],
                "category": "General",
                "meta_field": {
                    "excerpt": "A warm welcome to our platform",
                    "readTime": "2",
                    "featured": True,
                    "publishedAt": "2024-01-01T00:00:00Z"
                },
                "status": "published",
                "author_id": "admin",
                "app_id": "blog",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            },
            {
                "id": "sample-ecommerce-1", 
                "title": "Premium Wireless Headphones",
                "abstract": "High-quality wireless headphones with noise cancellation",
                "content": "Experience crystal clear audio with our premium wireless headphones featuring active noise cancellation.",
                "images": ["https://via.placeholder.com/600x300"],
                "tags": ["electronics", "headphones", "wireless"],
                "category": "Electronics",
                "meta_field": {
                    "price": "199.99",
                    "place": "New York",
                    "ratings": "4.5",
                    "brand": "TechCorp",
                    "availability": "In Stock",
                    "discount": "10"
                },
                "status": "published",
                "author_id": "seller1",
                "app_id": "ecommerce",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            }
        ]
        
        # Insert sample data
        for item in sample_items:
            try:
                container.create_item(body=item)
                print(f"✅ Added sample item: {item['title']}")
            except exceptions.CosmosResourceExistsError:
                print(f"⚠️  Item already exists: {item['title']}")
            except Exception as e:
                print(f"❌ Failed to add item {item['title']}: {e}")
        
        print("🎉 Database setup completed successfully!")
        return True
        
    except exceptions.CosmosHttpResponseError as e:
        print(f"❌ Cosmos DB HTTP error: {e}")
        print(f"Status code: {e.status_code}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_connection():
    """Test database connection and query"""
    print("\n🔍 Testing database connection...")
    
    try:
        from db.database import container
        
        # Test query
        query = "SELECT * FROM c WHERE c.status != 'deleted' OFFSET 0 LIMIT 5"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        print(f"✅ Connection successful! Found {len(items)} items")
        for item in items:
            print(f"  - {item.get('title', 'No title')} ({item.get('app_id', 'No app_id')})")
        
        return True
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database setup...\n")
    
    # Setup database
    if setup_database():
        # Test connection
        test_connection()
    else:
        print("❌ Database setup failed!")
        exit(1)



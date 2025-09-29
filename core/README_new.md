# Core Service

A microservice for managing core items/content in the microservice architecture.

## Features

- **Item Management**: Complete CRUD operations for items
- **Author-based Filtering**: Get items by author
- **Category-based Filtering**: Get items by category  
- **Pagination Support**: Configurable pagination for listings
- **Redis Caching**: Performance optimization through caching
- **Input Validation**: Comprehensive request validation

## API Endpoints

### Items
- `GET /api/v1/items` - Get paginated list of items
- `GET /api/v1/items/{item_id}` - Get item by ID
- `GET /api/v1/items/author/{author_id}` - Get items by author
- `GET /api/v1/items/category/{category}` - Get items by category
- `POST /api/v1/items` - Create new item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

### Health Check
- `GET /health` - Service health check

## Item Model

```python
class Item(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    category: str
    status: str
    created_at: datetime
    updated_at: datetime
```

## Environment Variables

Required environment variables:

```
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_SSL=false

# Cosmos DB Configuration
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DB_NAME=your_database_name
COSMOS_CONTAINER_ITEMS=items
COSMOS_CONTAINER_AUTHORS=authors

# Azure Search Configuration
AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_SEARCH_KEY=your_search_key
SEARCH_ITEM_INDEX_NAME=items-index
SEARCH_AUTHOR_INDEX_NAME=authors-index
```

## Running the Service

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Docker
```bash
docker build -t core-service .
docker run -p 8001:8001 core-service
```

## Architecture

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Azure Cosmos DB**: Database
- **Redis**: Caching
- **Azure Search**: Search functionality
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic
- **Factory Pattern**: Dependency injection

## Port

This service runs on port **8001** by default.

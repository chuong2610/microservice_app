# E-commerce Service

A microservice for managing e-commerce operations (cart, orders, reviews) in the microservice architecture.

## Features

- **Shopping Cart**: Cart management functionality (planned)
- **Order Management**: Order processing and tracking (planned)
- **Review System**: Product/service reviews (planned)
- **Microservice Ready**: Designed for microservice communication

## API Endpoints

### Cart (Planned)
- `GET /api/v1/cart` - Get user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{item_id}` - Update cart item
- `DELETE /api/v1/cart/items/{item_id}` - Remove item from cart
- `DELETE /api/v1/cart` - Clear cart

### Orders (Planned)
- `GET /api/v1/orders` - Get user's orders
- `GET /api/v1/orders/{order_id}` - Get specific order
- `POST /api/v1/orders` - Create new order
- `PUT /api/v1/orders/{order_id}/status` - Update order status

### Reviews (Planned)
- `GET /api/v1/reviews` - Get reviews
- `GET /api/v1/reviews/item/{item_id}` - Get reviews for item
- `POST /api/v1/reviews` - Create review
- `PUT /api/v1/reviews/{review_id}` - Update review
- `DELETE /api/v1/reviews/{review_id}` - Delete review

### Health Check
- `GET /health` - Service health check

## Data Models (Planned)

### Cart Model
```python
class CartItem(BaseModel):
    id: str
    user_id: str
    item_id: str
    quantity: int
    price: float
    added_at: datetime
```

### Order Model
```python
class Order(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
```

### Review Model
```python
class Review(BaseModel):
    id: str
    user_id: str
    item_id: str
    rating: int
    comment: str
    created_at: datetime
```

## Environment Variables

Required environment variables (when implemented):

```
# Database Configuration
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DB_NAME=your_database_name
COSMOS_CONTAINER_CART=cart
COSMOS_CONTAINER_ORDERS=orders
COSMOS_CONTAINER_REVIEWS=reviews

# Redis Configuration (for caching)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_SSL=false

# Payment Gateway (future)
PAYMENT_GATEWAY_URL=your_payment_gateway
PAYMENT_GATEWAY_KEY=your_payment_key
```

## Running the Service

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8004
```

### Docker
```bash
docker build -t ecommerce-service .
docker run -p 8004:8004 ecommerce-service
```

## Architecture

- **FastAPI**: Web framework
- **Pydantic**: Data validation (when implemented)
- **Azure Cosmos DB**: Database (when implemented)
- **Redis**: Caching (when implemented)
- **Repository Pattern**: Data access abstraction (when implemented)
- **Service Layer**: Business logic (when implemented)

## Port

This service runs on port **8004** by default.

## Status

This service is currently a **placeholder** with basic endpoints returning "Not implemented yet" messages. The actual e-commerce functionality needs to be implemented based on business requirements.

## Integration

When implemented, this service will integrate with:
- **User Service**: For user authentication and profiles
- **Core Service**: For item information
- **Authentication Service**: For token validation
- **Payment Gateways**: For order processing

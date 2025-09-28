# User Service

A microservice for managing users in the microservice architecture.

## Features

- **User Management**: Complete CRUD operations for users
- **Password Security**: BCrypt password hashing for stored passwords
- **Input Validation**: Comprehensive Pydantic validation
- **Caching**: Redis caching for performance
- **Soft Delete**: Deactivate/activate users
- **Simple & Clean**: Focused on user data management only
- **Email Lookup**: Find users by email address
- **Pagination**: Configurable pagination for user listings

## API Endpoints

### Users Management
- `GET /api/v1/users` - Get paginated list of users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users` - Create new user (with hashed password)
- `PUT /api/v1/users/{user_id}` - Update user information (role changes, profile updates)
- `PUT /api/v1/users/{user_id}/activate` - Activate user
- `PUT /api/v1/users/{user_id}/deactivate` - Deactivate user (soft delete)
- `DELETE /api/v1/users/{user_id}` - Delete user (hard delete)

### Health Check
- `GET /health` - Service health check

## Note

**Authentication functionality** (login, register, JWT tokens) has been moved to the dedicated **Authentication Service** (port 8002). This service focuses purely on user data management.

## User Model

```python
class User(BaseModel):
    id: str
    full_name: str = Field(..., max_length=100)
    email: EmailStr
    password: str
    avatar_url: Optional[str] = None
    role: Optional[str] = "user"
    is_active: Optional[bool] = True
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
COSMOS_CONTAINER_USERS=users

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Optional Configuration
USER_CACHE_TTL=300
MIN_PASSWORD_LENGTH=8
MAX_PASSWORD_LENGTH=128
REQUIRE_EMAIL_VERIFICATION=false
```

## Running the Service

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Docker
```bash
docker build -t user-service .
docker run -p 8000:8000 user-service
```

## Architecture

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Azure Cosmos DB**: Database
- **Redis**: Caching
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic
- **Factory Pattern**: Dependency injection


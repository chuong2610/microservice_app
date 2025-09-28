# Authentication Service

A microservice for handling user authentication and token management in the microservice architecture.

## Features

- **User Registration**: Register new users with validation
- **User Authentication**: Login with email/password
- **JWT Token Management**: Access & refresh token generation/validation
- **Password Security**: BCrypt password hashing
- **Token Storage**: Redis-based refresh token management
- **Token Refresh**: Refresh expired access tokens
- **User Logout**: Token revocation and cleanup
- **Microservice Ready**: Designed for microservice communication

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login with email/password
- `POST /api/v1/auth/logout` - User logout (revoke tokens)
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/decode-token` - Decode and validate JWT token
- `GET /health` - Service health check

## Request/Response Schemas

### Register Request
```python
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str  # min 8 characters
    avatar_url: Optional[str] = None
```

### Login Request
```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

### Token Response
```python
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
```

## Environment Variables

Required environment variables:

```
# Cosmos DB Configuration
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DB_NAME=your_database_name
COSMOS_CONTAINER_USERS=users

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_SSL=false

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Running the Service

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### Docker
```bash
docker build -t authentication-service .
docker run -p 8002:8002 authentication-service
```

## Architecture

- **FastAPI**: Web framework
- **JWT**: Token-based authentication
- **Redis**: Token storage and caching
- **Service Layer**: Authentication business logic
- **Factory Pattern**: Dependency injection

## Port

This service runs on port **8002** by default.

## Integration

This service is designed to work with other microservices:
- **User Service**: Validates user credentials
- **Other Services**: Validates tokens for protected endpoints

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # -------------------
    # Redis Configuration
    # -------------------
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

    # -------------------
    # Cosmos DB Configuration
    # -------------------
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "https://localhost:8081")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "cosmos-key")
    COSMOS_DB_NAME: str = os.getenv("COSMOS_DB_NAME", "microservicedb")
    COSMOS_CONTAINER_USERS: str = os.getenv("COSMOS_CONTAINER_USERS", "users")

    # -------------------
    # User Service Configuration
    # -------------------
    # Default pagination settings
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "10"))
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))
    
    # Cache settings
    USER_CACHE_TTL: int = int(os.getenv("USER_CACHE_TTL", "300"))  # 5 minutes
    
    # Password requirements
    MIN_PASSWORD_LENGTH: int = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))
    MAX_PASSWORD_LENGTH: int = int(os.getenv("MAX_PASSWORD_LENGTH", "128"))
    
    # User validation
    MAX_FULL_NAME_LENGTH: int = int(os.getenv("MAX_FULL_NAME_LENGTH", "100"))
    
    # Note: Authentication configurations moved to authentication service
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-use-openssl-rand-hex-32")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()
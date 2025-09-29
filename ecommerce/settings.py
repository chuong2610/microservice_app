from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Basic configuration for ecommerce service
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "ecommerce-service")
    
    # Database configuration (when implemented)
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "https://localhost:8081")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "cosmos-key")
    COSMOS_DB_NAME: str = os.getenv("COSMOS_DB_NAME", "microservicedb")
    COSMOS_CONTAINER_CART: str = os.getenv("COSMOS_CONTAINER_CART", "cart")
    COSMOS_CONTAINER_ORDERS: str = os.getenv("COSMOS_CONTAINER_ORDERS", "orders")
    COSMOS_CONTAINER_REVIEWS: str = os.getenv("COSMOS_CONTAINER_REVIEWS", "reviews")

    # Redis configuration (when implemented)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()

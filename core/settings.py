from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # -------------------
    # Redis
    # -------------------
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

    # -------------------
    # Cosmos DB
    # -------------------
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "https://localhost:8081")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "cosmos-key")
    COSMOS_DB_NAME: str = os.getenv("COSMOS_DB_NAME", "microservicedb")
    COSMOS_CONTAINER_ITEMS: str = os.getenv("COSMOS_CONTAINER_ITEMS", "items")
    COSMOS_CONTAINER_AUTHORS: str = os.getenv("COSMOS_CONTAINER_AUTHORS", "authors")

    

    AUTHENTICATION_SERVICE_URL: str = os.getenv("AUTHENTICATION_SERVICE_URL", "http://localhost:8001")

    # Azure Blob Storage
    AZURE_STORAGE_ACCOUNT_NAME: str = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "")
    AZURE_STORAGE_ACCOUNT_KEY: str = os.getenv("AZURE_STORAGE_ACCOUNT_KEY", "")
    AZURE_STORAGE_CONTAINER_NAME: str = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()
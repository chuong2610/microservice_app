from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Cosmos DB Configuration
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "https://localhost:8081")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "cosmos-key")
    COSMOS_DB_NAME: str = os.getenv("COSMOS_DB_NAME", "authdb")
    COSMOS_CONTAINER_USERS: str = os.getenv("COSMOS_CONTAINER_USERS", "users")

    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

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
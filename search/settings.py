from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
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

    # -------------------
    # Azure Search
    # -------------------
    AZURE_SEARCH_ENDPOINT: str = os.getenv("AZURE_SEARCH_ENDPOINT", "https://your-search-service.search.windows.net")
    AZURE_SEARCH_KEY: str = os.getenv("AZURE_SEARCH_KEY", "your-search-key")
    SEARCH_ITEM_INDEX_NAME: str = os.getenv("SEARCH_ITEM_INDEX_NAME", "items-index")
    SEARCH_AUTHOR_INDEX_NAME: str = os.getenv("SEARCH_AUTHOR_INDEX_NAME", "authors-index")

    # -------------------
    # Weights
    # -------------------
    WEIGHT_SEMANTIC: float = float(os.getenv("WEIGHT_SEMANTIC", "0.3"))
    WEIGHT_BM25: float = float(os.getenv("WEIGHT_BM25", "0.3"))
    WEIGHT_VECTOR: float = float(os.getenv("WEIGHT_VECTOR", "0.2"))
    WEIGHT_BUSINESS: float = float(os.getenv("WEIGHT_BUSINESS", "0.2"))

    AUTHORS_WEIGHT_SEMANTIC: float = float(os.getenv("AUTHORS_WEIGHT_SEMANTIC", "0.4"))
    AUTHORS_WEIGHT_BM25: float = float(os.getenv("AUTHORS_WEIGHT_BM25", "0.3"))
    AUTHORS_WEIGHT_VECTOR: float = float(os.getenv("AUTHORS_WEIGHT_VECTOR", "0.2"))
    AUTHORS_WEIGHT_BUSINESS: float = float(os.getenv("AUTHORS_WEIGHT_BUSINESS", "0.1"))

    # -------------------
    # Freshness
    # -------------------
    FRESHNESS_HALFLIFE_DAYS: int = int(os.getenv("FRESHNESS_HALFLIFE_DAYS", "30"))
    FRESHNESS_WINDOW_DAYS: int = int(os.getenv("FRESHNESS_WINDOW_DAYS", "90"))

    # -------------------
    # LLM / OpenAI
    # -------------------
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    AZURE_OPENAI_CHAT_MODEL: str = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-35-turbo")
    AZURE_OPENAI_EMBED_MODEL: str = os.getenv("AZURE_OPENAI_EMBED_MODEL", "text-embedding-ada-002")
    EMBED_MODEL_DIMENSION: int = int(os.getenv("EMBED_MODEL_DIMENSION", "1536"))
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "your-azure-openai-key")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-key")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")

    # -------------------
    # Ollama
    # -------------------
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_EMBED_MODEL: str = os.getenv("OLLAMA_EMBED_MODEL", "llama2")
    OLLAMA_CHAT_MODEL: str = os.getenv("OLLAMA_CHAT_MODEL", "llama2")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()
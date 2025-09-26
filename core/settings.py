from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis
    # -------------------
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SSL: bool

    # -------------------
    # Cosmos DB
    # -------------------
    COSMOS_ENDPOINT: str
    COSMOS_KEY: str
    COSMOS_DB_NAME: str
    COSMOS_CONTAINER_NAME: str
    COSMOS_CONTAINER_ITEMS: str
    COSMOS_CONTAINER_AUTHORS: str

    # -------------------
    # Azure Search
    # -------------------
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_KEY: str
    SEARCH_ITEM_INDEX_NAME: str
    SEARCH_AUTHOR_INDEX_NAME: str

    # -------------------
    # Weights
    # -------------------
    WEIGHT_SEMANTIC: float
    WEIGHT_BM25: float
    WEIGHT_VECTOR: float
    WEIGHT_BUSINESS: float

    AUTHORS_WEIGHT_SEMANTIC: float
    AUTHORS_WEIGHT_BM25: float
    AUTHORS_WEIGHT_VECTOR: float
    AUTHORS_WEIGHT_BUSINESS: float

    # -------------------
    # Freshness
    # -------------------
    FRESHNESS_HALFLIFE_DAYS: int
    FRESHNESS_WINDOW_DAYS: int

    # -------------------
    # LLM / OpenAI
    # -------------------
    LLM_PROVIDER: str
    AZURE_OPENAI_CHAT_MODEL: str
    AZURE_OPENAI_EMBED_MODEL: str
    EMBED_MODEL_DIMENSION: int
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str

    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str
    OPENAI_EMBED_MODEL: str

    # -------------------
    # Ollama
    # -------------------
    OLLAMA_BASE_URL: str
    OLLAMA_EMBED_MODEL: str
    OLLAMA_CHAT_MODEL: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
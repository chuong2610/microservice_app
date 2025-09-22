from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COSMOS_ENDPOINT = "COSMOS_ENDPOINT"
    COSMOS_KEY = "COSMOS_KEY"
    COSMOS_DB_NAME =  "authdb"
    COSMOS_CONTAINER_NAME = "users"

    REDIS_HOST = "localhost"
    REDIS_PORT = 6380

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
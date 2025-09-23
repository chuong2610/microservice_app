from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COSMOS_ENDPOINT: str = "COSMOS_ENDPOINT"
    COSMOS_KEY: str = "COSMOS_KEY"
    COSMOS_DB_NAME: str = "authdb"
    COSMOS_CONTAINER_NAME: str = "users"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380
    REDIS_PASSWORD: str = ""
    REDIS_SSL: bool = False

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
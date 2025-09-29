from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    COSMOS_ENDPOINT: str
    COSMOS_KEY: str
    COSMOS_DB_NAME: str
    COSMOS_CONTAINER_ORDERS: str
    COSMOS_CONTAINER_CARTS: str
    COSMOS_CONTAINER_REVIEWS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
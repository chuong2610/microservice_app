from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COSMOS_ENDPOINT: str = "COSMOS_ENDPOINT"
    COSMOS_KEY: str = "COSMOS_KEY"
    COSMOS_DB_NAME: str = "authdb"
    COSMOS_CONTAINER_NAME: str = "items"

    


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

     # Auth0 Configuration
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_AUDIENCE: str
    AUTH0_CALLBACK_URL: str

    # JWT Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int

    # API Configuration
    API_TITLE: str
    API_VERSION: str
    API_PREFIX: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

"""
Configuration settings for RealityCheck API
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "RealityCheck Agent System"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8001
    
    # AI Services
    google_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    comet_api_key: Optional[str] = None
    comet_workspace: Optional[str] = None
    
    # Echo AI Monetization
    echo_api_key: Optional[str] = None
    echo_client_id: Optional[str] = None
    echo_client_secret: Optional[str] = None
    echo_merchant_id: Optional[str] = None
    echo_project_name: str = "RealityCheck Financial Assistant"
    echo_environment: str = "development"
    
    # Backend URLs
    backend_base_url: str = "http://localhost:8000"
    plan_endpoint: str = "/plan"
    transactions_endpoint: str = "/transactions"
    remittance_endpoint: str = "/remittance"
    search_endpoint: str = "/search"
    
    # Voice Configuration
    default_voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    voice_output_dir: str = "voice_outputs"
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Auth0 Configuration
    AUTH0_DOMAIN: Optional[str] = None
    AUTH0_CLIENT_ID: Optional[str] = None
    AUTH0_CLIENT_SECRET: Optional[str] = None
    AUTH0_AUDIENCE: Optional[str] = None
    AUTH0_CALLBACK_URL: Optional[str] = None

    # JWT Configuration
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Nessie API Configuration
    NESSIE_API_KEY: Optional[str] = None
    NESSIE_BASE_URL: Optional[str] = None

    # API Configuration (for FastAPI)
    API_TITLE: str = "RealityCheck API"
    API_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from .env

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Global settings instance for backward compatibility
settings = get_settings()

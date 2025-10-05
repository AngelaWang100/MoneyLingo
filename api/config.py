"""
Configuration settings for RealityCheck API
"""
import os
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
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
    
    # Backend URLs
    backend_base_url: str = "http://localhost:8000"
    plan_endpoint: str = "/plan"
    transactions_endpoint: str = "/transactions"
    
    # Voice Configuration
    default_voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    voice_output_dir: str = "voice_outputs"
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

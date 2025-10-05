"""
Voice synthesis models
"""
from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    """Request model for translation with voice"""
    content: str = Field(..., description="Content to translate")
    language: str = Field(..., description="Target language")
    user_level: str = Field(default="beginner", description="User experience level")

class VoiceRequest(BaseModel):
    """Request model for voice synthesis"""
    text: str = Field(..., description="Text to synthesize")
    language: str = Field(default="en", description="Language code")
    voice_id: Optional[str] = Field(None, description="Specific voice ID")

class VoiceResponse(BaseModel):
    """Response model for voice synthesis"""
    success: bool
    filepath: Optional[str] = None
    filename: Optional[str] = None
    voice_id: Optional[str] = None
    text_length: Optional[int] = None
    language: Optional[str] = None
    error: Optional[str] = None

class AutoLanguageVoiceRequest(BaseModel):
    """Request model for auto-language voice processing"""
    content: str = Field(..., description="Content to process")
    language: str = Field(default="auto", description="Language preference")
    user_level: str = Field(default="beginner", description="User experience level")

class VoiceStatusResponse(BaseModel):
    """Response model for voice service status"""
    service_available: bool
    voices_count: Optional[int] = None
    supported_languages: Optional[list] = None
    error: Optional[str] = None

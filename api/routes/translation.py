"""
Translation routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from api.models.voice import TranslationRequest, VoiceResponse
from api.dependencies import get_orchestrator, get_observer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=VoiceResponse, status_code=status.HTTP_200_OK)
async def translate_content(
    request: TranslationRequest,
    orchestrator = Depends(get_orchestrator),
    observer = Depends(get_observer)
) -> VoiceResponse:
    """Translate financial content"""
    try:
        observer.log_agent_start("translation_agent", request.dict())
        
        input_data = {
            "content": request.content,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await orchestrator.translation_agent.process(input_data)
        
        observer.log_agent_end("translation_agent", result, result.get("success", False))
        
        return VoiceResponse(
            success=result.get("success", False),
            filepath=result.get("filepath"),
            filename=result.get("filename"),
            voice_id=result.get("voice_id"),
            text_length=result.get("text_length"),
            language=result.get("language"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        observer.log_error("translation_agent", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )

@router.get("/languages")
async def get_supported_languages() -> Dict[str, Any]:
    """Get list of supported languages"""
    return {
        "success": True,
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "ar", "name": "Arabic"},
            {"code": "hi", "name": "Hindi"},
            {"code": "ru", "name": "Russian"}
        ]
    }

@router.get("/detect")
async def detect_language(text: str) -> Dict[str, Any]:
    """Detect language of input text"""
    try:
        # Simple language detection logic
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'por favor', 'dinero', 'ahorro']):
            return {"language": "es", "confidence": 0.8}
        
        # French indicators
        if any(word in text_lower for word in ['bonjour', 'merci', 'argent', 'épargne']):
            return {"language": "fr", "confidence": 0.8}
        
        # German indicators
        if any(word in text_lower for word in ['hallo', 'danke', 'geld', 'sparen']):
            return {"language": "de", "confidence": 0.8}
        
        # Default to English
        return {"language": "en", "confidence": 0.6}
        
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Language detection failed: {str(e)}"
        )

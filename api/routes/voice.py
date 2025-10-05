"""
Voice synthesis routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from api.models.voice import (
    TranslationRequest, VoiceRequest, VoiceResponse, 
    AutoLanguageVoiceRequest, VoiceStatusResponse
)
from api.dependencies import (
    get_voice_translation_agent, get_auto_language_voice_agent, 
    get_voice_service, get_observer
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/translate", response_model=VoiceResponse, status_code=status.HTTP_200_OK)
async def translate_with_voice(
    request: TranslationRequest,
    voice_translation_agent = Depends(get_voice_translation_agent),
    observer = Depends(get_observer)
) -> VoiceResponse:
    """Translate content with voice synthesis"""
    try:
        observer.log_agent_start("voice_translation_agent", request.dict())
        
        input_data = {
            "content": request.content,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await voice_translation_agent.process_with_voice(
            input_data, 
            language=request.language.lower()
        )
        
        observer.log_agent_end("voice_translation_agent", result, result.get("success", False))
        
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
        logger.error(f"Voice translation failed: {e}")
        observer.log_error("voice_translation_agent", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice translation failed: {str(e)}"
        )

@router.post("/synthesize", response_model=VoiceResponse, status_code=status.HTTP_200_OK)
async def synthesize_voice(
    request: VoiceRequest,
    voice_service = Depends(get_voice_service)
) -> VoiceResponse:
    """Synthesize voice from text"""
    try:
        result = voice_service.synthesize_speech(
            text=request.text,
            voice_id=request.voice_id,
            language=request.language
        )
        
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
        logger.error(f"Voice synthesis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice synthesis failed: {str(e)}"
        )

@router.post("/auto-language", response_model=VoiceResponse, status_code=status.HTTP_200_OK)
async def auto_language_voice(
    request: AutoLanguageVoiceRequest,
    auto_language_agent = Depends(get_auto_language_voice_agent),
    observer = Depends(get_observer)
) -> VoiceResponse:
    """Process voice with automatic language detection"""
    try:
        observer.log_agent_start("auto_language_voice_agent", request.dict())
        
        input_data = {
            "content": request.content,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await auto_language_agent.process_with_voice(input_data)
        
        observer.log_agent_end("auto_language_voice_agent", result, result.get("success", False))
        
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
        logger.error(f"Auto-language voice processing failed: {e}")
        observer.log_error("auto_language_voice_agent", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auto-language voice processing failed: {str(e)}"
        )

@router.get("/status", response_model=VoiceStatusResponse, status_code=status.HTTP_200_OK)
async def get_voice_status(
    voice_translation_agent = Depends(get_voice_translation_agent)
) -> VoiceStatusResponse:
    """Get voice service status"""
    try:
        status_info = voice_translation_agent.get_voice_status()
        
        return VoiceStatusResponse(
            service_available=status_info.get("service_available", False),
            voices_count=status_info.get("voices_count"),
            supported_languages=status_info.get("supported_languages"),
            error=status_info.get("error")
        )
        
    except Exception as e:
        logger.error(f"Voice status check failed: {e}")
        return VoiceStatusResponse(
            service_available=False,
            error=str(e)
        )

@router.get("/voices")
async def get_available_voices(
    voice_service = Depends(get_voice_service)
) -> Dict[str, Any]:
    """Get list of available voices"""
    try:
        return voice_service.get_available_voices()
    except Exception as e:
        logger.error(f"Voice list retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice list retrieval failed: {str(e)}"
        )

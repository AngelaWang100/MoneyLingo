"""
Dependency injection for API components
"""
from functools import lru_cache
import logging
from agents.orchestrator import AgentOrchestrator
from agents.voice_translation_agent import VoiceTranslationAgent
from agents.auto_language_voice_agent import AutoLanguageVoiceAgent
from voice.elevenlabs_service import ElevenLabsVoiceService
from observability.comet_integration import CometObserver
from monetization.monetization_service import RealityCheckMonetization

logger = logging.getLogger(__name__)

@lru_cache()
def get_orchestrator() -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    return AgentOrchestrator()

@lru_cache()
def get_voice_translation_agent() -> VoiceTranslationAgent:
    """Get voice translation agent instance"""
    return VoiceTranslationAgent()

@lru_cache()
def get_auto_language_voice_agent() -> AutoLanguageVoiceAgent:
    """Get auto language voice agent instance"""
    return AutoLanguageVoiceAgent()

@lru_cache()
def get_voice_service() -> ElevenLabsVoiceService:
    """Get ElevenLabs voice service instance"""
    return ElevenLabsVoiceService()

@lru_cache()
def get_observer() -> CometObserver:
    """Get Comet observer instance"""
    return CometObserver()

@lru_cache()
def get_monetization_service() -> RealityCheckMonetization:
    """Get monetization service instance"""
    return RealityCheckMonetization()
"""
Dependency injection for API components
"""
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache()
def get_orchestrator():
    """Get the agent orchestrator instance"""
    from agents.orchestrator import AgentOrchestrator
    return AgentOrchestrator()

@lru_cache()
def get_observer():
    """Get the comet observer instance"""
    from observability.comet_integration import CometObserver
    return CometObserver()

@lru_cache()
def get_voice_translation_agent():
    """Get the voice translation agent instance"""
    from agents.voice_translation_agent import VoiceTranslationAgent
    return VoiceTranslationAgent()

@lru_cache()
def get_auto_language_voice_agent():
    """Get the auto language voice agent instance"""
    from agents.auto_language_voice_agent import AutoLanguageVoiceAgent
    return AutoLanguageVoiceAgent()

@lru_cache()
def get_voice_service():
    """Get the voice service instance"""
    from voice.elevenlabs_service import ElevenLabsVoiceService
    return ElevenLabsVoiceService()
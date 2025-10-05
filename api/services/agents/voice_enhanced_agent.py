"""
Voice-enhanced base agent with ElevenLabs integration
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
import os
from .base_agent import BaseAgent
from voice.elevenlabs_service import ElevenLabsVoiceService

class VoiceEnhancedAgent(BaseAgent):
    """Base class for voice-enhanced agents with ElevenLabs integration"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.voice_service = ElevenLabsVoiceService()
        self.voice_enabled = self.voice_service.client is not None
        
        if self.voice_enabled:
            self.logger.info(f"Voice synthesis enabled for {name}")
        else:
            self.logger.warning(f"Voice synthesis disabled for {name} - ElevenLabs API key not found")
    
    async def process_with_voice(self, input_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        """Process input and generate voice response"""
        try:
            # Process with regular agent logic
            result = await self.process(input_data)
            
            # Add voice synthesis if successful
            if result.get("success") and self.voice_enabled:
                voice_result = await self._generate_voice_response(result, language)
                result["voice"] = voice_result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Voice-enhanced processing failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    async def _generate_voice_response(self, agent_result: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        """Generate voice response for agent result"""
        try:
            # Extract text content for voice synthesis
            text_content = self._extract_text_for_voice(agent_result)
            
            if not text_content:
                return {"voice_enabled": False, "reason": "No text content to synthesize"}
            
            # Generate voice
            voice_result = self.voice_service.create_agent_voice_response(
                agent_name=self.name,
                text=text_content,
                language=language
            )
            
            return voice_result
            
        except Exception as e:
            self.logger.error(f"Voice generation failed: {e}")
            return {"voice_enabled": False, "error": str(e)}
    
    def _extract_text_for_voice(self, agent_result: Dict[str, Any]) -> str:
        """Extract text content from agent result for voice synthesis"""
        # Try different possible text fields
        text_fields = [
            "translated_content",
            "ai_recommendations", 
            "ai_analysis",
            "content",
            "response",
            "message"
        ]
        
        for field in text_fields:
            if field in agent_result and agent_result[field]:
                text = str(agent_result[field])
                # Limit text length for voice synthesis
                if len(text) > 1000:
                    text = text[:1000] + "..."
                return text
        
        return "I've processed your request successfully."
    
    async def create_multilingual_voice_response(self, text: str, languages: list) -> Dict[str, Any]:
        """Create voice responses in multiple languages"""
        if not self.voice_enabled:
            return {"voice_enabled": False, "reason": "ElevenLabs not available"}
        
        try:
            result = self.voice_service.create_multilingual_response(text, languages)
            return result
        except Exception as e:
            self.logger.error(f"Multilingual voice response failed: {e}")
            return {"voice_enabled": False, "error": str(e)}
    
    def get_voice_status(self) -> Dict[str, Any]:
        """Get voice service status"""
        return {
            "voice_enabled": self.voice_enabled,
            "agent": self.name,
            "available_voices": self.voice_service.get_available_voices() if self.voice_enabled else None
        }

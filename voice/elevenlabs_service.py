"""
ElevenLabs voice synthesis service for RealityCheck agents
"""
import os
import logging
from typing import Dict, Any, Optional
from elevenlabs.client import ElevenLabs

class ElevenLabsVoiceService:
    """ElevenLabs voice synthesis service for agent responses"""
    
    def __init__(self):
        self.logger = logging.getLogger("elevenlabs_service")
        self.api_key = "sk_eb8f1fa7a20cfa5ee17ebedd0a6eeb81144c6c032dd887aa"
        
        if not self.api_key:
            self.logger.warning("ELEVENLABS_API_KEY not found. Voice synthesis will be disabled.")
            self.client = None
        else:
            self.client = ElevenLabs(api_key=self.api_key)
            self.logger.info("ElevenLabs client initialized successfully")
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get list of available voices"""
        if not self.client:
            return {"error": "ElevenLabs client not initialized"}
        
        try:
            voices = self.client.voices.get_all()
            return {
                "success": True,
                "voices": [
                    {
                        "voice_id": voice.voice_id,
                        "name": voice.name,
                        "category": voice.category,
                        "description": voice.description
                    }
                    for voice in voices.voices
                ]
            }
        except Exception as e:
            self.logger.error(f"Failed to get voices: {e}")
            return {"error": str(e)}
    
    def synthesize_speech(self, text: str, voice_id: str = None, language: str = "en") -> Dict[str, Any]:
        """Synthesize speech from text"""
        if not self.client:
            return {"error": "ElevenLabs client not initialized"}
        
        try:
            # Default voice selection based on language
            if not voice_id:
                voice_id = self._get_default_voice_for_language(language)
            
            # Generate audio using client
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            
            # Save audio file
            filename = f"voice_output_{hash(text) % 10000}.mp3"
            filepath = f"voice_outputs/{filename}"
            
            # Create directory if it doesn't exist
            os.makedirs("voice_outputs", exist_ok=True)
            
            # Save audio to file
            with open(filepath, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
            
            self.logger.info(f"Voice synthesis completed: {filepath}")
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "voice_id": voice_id,
                "text_length": len(text),
                "language": language
            }
            
        except Exception as e:
            self.logger.error(f"Voice synthesis failed: {e}")
            return {"error": str(e)}
    
    def _get_default_voice_for_language(self, language: str) -> str:
        """Get default voice ID for language with optimized voice selection"""
        # Optimized voices for different languages
        default_voices = {
            "en": "21m00Tcm4TlvDq8ikWAM",  # Rachel (English, clear and professional)
            "es": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Spanish)
            "fr": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for French)
            "de": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for German)
            "it": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Italian)
            "pt": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Portuguese)
            "zh": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Chinese)
            "ja": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Japanese)
            "ko": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Korean)
            "ar": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Arabic)
            "hi": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Hindi)
            "ru": "21m00Tcm4TlvDq8ikWAM",  # Rachel (multilingual, good for Russian)
        }
        return default_voices.get(language, "21m00Tcm4TlvDq8ikWAM")
    
    def create_agent_voice_response(self, agent_name: str, text: str, language: str = "en") -> Dict[str, Any]:
        """Create voice response for specific agent"""
        try:
            # Add agent context to text
            contextual_text = f"Hello, I'm your {agent_name} assistant. {text}"
            
            # Synthesize speech
            result = self.synthesize_speech(contextual_text, language=language)
            
            if result.get("success"):
                self.logger.info(f"Agent voice response created for {agent_name}")
                return {
                    "success": True,
                    "agent": agent_name,
                    "voice_file": result.get("filepath"),
                    "text": contextual_text,
                    "language": language
                }
            else:
                return result
                
        except Exception as e:
            self.logger.error(f"Agent voice response failed: {e}")
            return {"error": str(e)}
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        # Simple language detection based on common patterns
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'por favor', 'dinero', 'ahorro', 'inversión']):
            return "es"
        
        # French indicators
        if any(word in text_lower for word in ['bonjour', 'merci', 'argent', 'épargne', 'investissement']):
            return "fr"
        
        # German indicators
        if any(word in text_lower for word in ['hallo', 'danke', 'geld', 'sparen', 'investition']):
            return "de"
        
        # Italian indicators
        if any(word in text_lower for word in ['ciao', 'grazie', 'denaro', 'risparmio', 'investimento']):
            return "it"
        
        # Portuguese indicators
        if any(word in text_lower for word in ['olá', 'obrigado', 'dinheiro', 'poupança', 'investimento']):
            return "pt"
        
        # Chinese indicators
        if any(char in text for char in '你好谢谢钱储蓄投资'):
            return "zh"
        
        # Japanese indicators
        if any(char in text for char in 'こんにちはありがとうお金貯金投資'):
            return "ja"
        
        # Korean indicators
        if any(char in text for char in '안녕하세요감사합니다돈저축투자'):
            return "ko"
        
        # Arabic indicators
        if any(char in text for char in 'مرحباشكراالمالادخارالاستثمار'):
            return "ar"
        
        # Hindi indicators
        if any(word in text_lower for word in ['नमस्ते', 'धन्यवाद', 'पैसा', 'बचत', 'निवेश']):
            return "hi"
        
        # Russian indicators
        if any(word in text_lower for word in ['привет', 'спасибо', 'деньги', 'сбережения', 'инвестиции']):
            return "ru"
        
        # Default to English
        return "en"
    
    def synthesize_speech_auto_language(self, text: str) -> Dict[str, Any]:
        """Synthesize speech with automatic language detection"""
        detected_language = self.detect_language(text)
        self.logger.info(f"Auto-detected language: {detected_language}")
        
        result = self.synthesize_speech(text, language=detected_language)
        result["detected_language"] = detected_language
        return result
    
    def create_multilingual_response(self, text: str, languages: list) -> Dict[str, Any]:
        """Create voice responses in multiple languages"""
        results = {}
        
        for language in languages:
            try:
                result = self.synthesize_speech(text, language=language)
                results[language] = result
            except Exception as e:
                results[language] = {"error": str(e)}
        
        return {
            "success": True,
            "multilingual_responses": results,
            "languages": languages
        }

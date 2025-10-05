"""
Voice-enhanced translation agent with ElevenLabs integration
"""
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from .voice_enhanced_agent import VoiceEnhancedAgent

class VoiceTranslationAgent(VoiceEnhancedAgent):
    """Voice-enhanced translation agent with multilingual voice synthesis"""
    
    def __init__(self):
        super().__init__(
            name="voice_translation_agent",
            description="Translates financial content with natural voice synthesis in multiple languages"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key="AIzaSyBvkcT0-wLuIgIENqPIHJKs2X5Br-ckJKs",
            temperature=0.3
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate and explain financial content with voice synthesis"""
        try:
            content = input_data.get("content", "")
            target_language = input_data.get("language", "English")
            user_level = input_data.get("user_level", "beginner")
            
            # Create system prompt for translation and explanation
            system_prompt = f"""
            You are a financial translation and explanation expert. Your task is to:
            1. Translate the provided financial content to {target_language}
            2. Explain complex financial concepts in simple terms appropriate for a {user_level} level
            3. Maintain accuracy while making content accessible
            4. Include relevant examples when helpful
            
            Always provide both the translation and a clear explanation.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Please translate and explain this financial content: {content}")
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Log the translation decision
            self.log_decision(
                decision=f"Translated to {target_language} for {user_level} level",
                context={"content_length": len(content), "target_language": target_language},
                confidence=0.9
            )
            
            return {
                "translated_content": response.content,
                "language": target_language,
                "user_level": user_level,
                "agent": self.name,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Voice translation failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    async def process_with_multilingual_voice(self, input_data: Dict[str, Any], languages: list = None) -> Dict[str, Any]:
        """Process translation with voice synthesis in multiple languages"""
        try:
            # Get translation result
            result = await self.process(input_data)
            
            if not result.get("success"):
                return result
            
            # Add multilingual voice synthesis
            if self.voice_enabled and languages:
                target_language = result.get("language", "English")
                translated_text = result.get("translated_content", "")
                
                # Create voice responses in multiple languages
                voice_result = await self.create_multilingual_voice_response(translated_text, languages)
                result["multilingual_voice"] = voice_result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Multilingual voice translation failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }

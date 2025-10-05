"""
Auto-language detection voice agent for RealityCheck
Automatically detects user language and responds in the same language
"""
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from .voice_enhanced_agent import VoiceEnhancedAgent

class AutoLanguageVoiceAgent(VoiceEnhancedAgent):
    """Agent that automatically detects user language and responds in the same language"""
    
    def __init__(self):
        super().__init__(
            name="auto_language_voice_agent",
            description="Automatically detects user language and provides voice responses in the same language"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        )
    
    def detect_user_language(self, input_text: str) -> str:
        """Detect the language of the user's input"""
        return self.voice_service.detect_language(input_text)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input with automatic language detection"""
        try:
            user_input = input_data.get("content", "")
            user_language = self.detect_user_language(user_input)
            
            # Create system prompt that adapts to the detected language
            system_prompt = f"""
            You are a multilingual financial assistant. The user is speaking in {user_language}.
            Respond in the same language ({user_language}) and provide helpful financial guidance.
            
            Your response should be:
            1. In the same language as the user ({user_language})
            2. Professional and helpful
            3. Focused on financial topics
            4. Clear and easy to understand
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Log the language detection decision
            self.log_decision(
                decision=f"Detected language: {user_language}",
                context={"user_input": user_input, "detected_language": user_language},
                confidence=0.9
            )
            
            return {
                "translated_content": response.content,
                "detected_language": user_language,
                "user_input": user_input,
                "agent": self.name,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Auto-language voice agent failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    async def process_with_voice(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input with automatic language detection and voice synthesis"""
        # First, process the input using the agent's core logic
        agent_response = await self.process(input_data)
        
        if agent_response.get("success") and self.voice_service.client:
            detected_language = agent_response.get("detected_language", "en")
            text_to_synthesize = agent_response.get("translated_content", "")
            
            if text_to_synthesize:
                self.logger.info(f"Synthesizing voice in detected language: {detected_language}")
                voice_output = self.voice_service.synthesize_speech_auto_language(text_to_synthesize)
                agent_response["voice_output"] = voice_output
            else:
                self.logger.warning(f"No text to synthesize for agent {self.name} response.")
                agent_response["voice_output"] = {"success": False, "message": "No text to synthesize."}
        else:
            self.logger.warning(f"Voice synthesis disabled for {self.name} - ElevenLabs API key not found or agent processing failed.")
            agent_response["voice_output"] = {"success": False, "message": "Voice synthesis not available."}
        
        return agent_response

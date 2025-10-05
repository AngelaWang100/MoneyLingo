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
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request with automatic language detection"""
        try:
            content = input_data.get("content", "")
            user_level = input_data.get("user_level", "beginner")
            
            # Detect language
            detected_language = self.detect_language(content)
            
            # Create system prompt for auto-language response
            system_prompt = f"""
            You are a financial assistant that automatically detects user language and responds in the same language.
            The user's message appears to be in {detected_language}.
            
            Provide helpful financial advice in {detected_language} appropriate for a {user_level} level.
            Be warm, professional, and helpful.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"User message: {content}")
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Log the auto-language decision
            self.log_decision(
                decision=f"Auto-detected language: {detected_language}",
                context={"content_length": len(content), "detected_language": detected_language},
                confidence=0.9
            )
            
            return {
                "response": response.content,
                "detected_language": detected_language,
                "user_level": user_level,
                "agent": self.name,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Auto-language voice processing failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'por favor', 'dinero', 'ahorro', 'inversión']):
            return "Spanish"
        
        # French indicators
        if any(word in text_lower for word in ['bonjour', 'merci', 'argent', 'épargne', 'investissement']):
            return "French"
        
        # German indicators
        if any(word in text_lower for word in ['hallo', 'danke', 'geld', 'sparen', 'investition']):
            return "German"
        
        # Italian indicators
        if any(word in text_lower for word in ['ciao', 'grazie', 'denaro', 'risparmio', 'investimento']):
            return "Italian"
        
        # Portuguese indicators
        if any(word in text_lower for word in ['olá', 'obrigado', 'dinheiro', 'poupança', 'investimento']):
            return "Portuguese"
        
        # Chinese indicators
        if any(char in text for char in '你好谢谢钱储蓄投资'):
            return "Chinese"
        
        # Japanese indicators
        if any(char in text for char in 'こんにちはありがとうお金貯金投資'):
            return "Japanese"
        
        # Korean indicators
        if any(char in text for char in '안녕하세요감사합니다돈저축투자'):
            return "Korean"
        
        # Arabic indicators
        if any(char in text for char in 'مرحباشكراالمالادخارالاستثمار'):
            return "Arabic"
        
        # Hindi indicators
        if any(word in text_lower for word in ['नमस्ते', 'धन्यवाद', 'पैसा', 'बचत', 'निवेश']):
            return "Hindi"
        
        # Russian indicators
        if any(word in text_lower for word in ['привет', 'спасибо', 'деньги', 'сбережения', 'инвестиции']):
            return "Russian"
        
        # Default to English
        return "English"
    
    async def process_with_voice(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process with voice synthesis in detected language"""
        try:
            # Get the response
            result = await self.process(input_data)
            
            if not result.get("success"):
                return result
            
            # Add voice synthesis
            if self.voice_enabled:
                detected_language = result.get("detected_language", "English")
                response_text = result.get("response", "")
                
                # Create voice response
                voice_result = await self._generate_voice_response(result, detected_language)
                result["voice"] = voice_result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Auto-language voice processing failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }

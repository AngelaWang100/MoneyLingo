"""
Gemini-powered translation and explanation agent
"""
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from .base_agent import BaseAgent

class TranslationAgent(BaseAgent):
    """Agent for translating and explaining financial concepts in multiple languages"""
    
    def __init__(self):
        super().__init__(
            name="translation_agent",
            description="Translates financial content and explains concepts in user's preferred language"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate and explain financial content"""
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
            self.logger.error(f"Translation failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }

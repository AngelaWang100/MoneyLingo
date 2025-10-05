"""
Main application entry point for MoneyLingo agent system
"""
import os
import asyncio
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from agents.orchestrator import AgentOrchestrator
from agents.voice_translation_agent import VoiceTranslationAgent
from agents.auto_language_voice_agent import AutoLanguageVoiceAgent
from voice.elevenlabs_service import ElevenLabsVoiceService
from observability.comet_integration import CometObserver
from monetization.monetization_service import MoneyLingoMonetization

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MoneyLingo Agent System",
    description="Multi-agent system for financial planning and remittance",
    version="1.0.0"
)

# Initialize components
orchestrator = AgentOrchestrator()
observer = CometObserver()
voice_translation_agent = VoiceTranslationAgent()
auto_language_voice_agent = AutoLanguageVoiceAgent()
voice_service = ElevenLabsVoiceService()
monetization_service = MoneyLingoMonetization()

# Pydantic models
class FinancialRequest(BaseModel):
    goals: List[str]
    income: float
    expenses: float
    timeline: str = "1 year"
    language: str = "English"
    user_level: str = "beginner"

class RemittanceRequest(BaseModel):
    amount: float
    currency: str = "USD"
    destination: str
    source_country: str
    destination_country: str

class TranslationRequest(BaseModel):
    content: str
    language: str
    user_level: str = "beginner"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RealityCheck Agent System is running", "status": "healthy"}

@app.post("/process/financial")
async def process_financial_request(request: FinancialRequest):
    """Process a complete financial planning request"""
    try:
        observer.log_agent_start("financial_orchestrator", request.dict())
        
        input_data = {
            "goals": request.goals,
            "income": request.income,
            "expenses": request.expenses,
            "timeline": request.timeline,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await orchestrator.process_request(input_data)
        
        observer.log_agent_end("financial_orchestrator", result, result.get("success", False))
        
        return result
        
    except Exception as e:
        logger.error(f"Financial processing failed: {e}")
        observer.log_error("financial_orchestrator", str(e), {"request": request.dict()})
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/remittance")
async def process_remittance_request(request: RemittanceRequest):
    """Process a remittance request"""
    try:
        observer.log_agent_start("remittance_orchestrator", request.dict())
        
        input_data = {
            "amount": request.amount,
            "currency": request.currency,
            "destination": request.destination,
            "source_country": request.source_country,
            "destination_country": request.destination_country
        }
        
        result = await orchestrator.process_request(input_data)
        
        observer.log_agent_end("remittance_orchestrator", result, result.get("success", False))
        
        return result
        
    except Exception as e:
        logger.error(f"Remittance processing failed: {e}")
        observer.log_error("remittance_orchestrator", str(e), {"request": request.dict()})
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_content(request: TranslationRequest):
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
        
        return result
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        observer.log_error("translation_agent", str(e), {"request": request.dict()})
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health/agents")
async def health_check_agents():
    """Check health of all agents"""
    try:
        # Test each agent with a simple request
        test_data = {"content": "test", "language": "English"}
        
        translation_result = await orchestrator.translation_agent.process(test_data)
        financial_result = await orchestrator.financial_planning_agent.process({"goals": ["test"], "income": 1000, "expenses": 500})
        remittance_result = await orchestrator.remittance_agent.process({"amount": 100, "currency": "USD", "destination": "test"})
        
        return {
            "translation_agent": translation_result.get("success", False),
            "financial_planning_agent": financial_result.get("success", False),
            "remittance_agent": remittance_result.get("success", False),
            "overall_health": all([
                translation_result.get("success", False),
                financial_result.get("success", False),
                remittance_result.get("success", False)
            ])
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"error": str(e), "overall_health": False}

@app.post("/translate/voice")
async def translate_with_voice(request: TranslationRequest):
    """Translate content with voice synthesis"""
    try:
        observer.log_agent_start("voice_translation_agent", request.dict())
        
        input_data = {
            "content": request.content,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await voice_translation_agent.process_with_voice(input_data, language=request.language.lower())
        
        observer.log_agent_end("voice_translation_agent", result, result.get("success", False))
        
        return result
        
    except Exception as e:
        logger.error(f"Voice translation failed: {e}")
        observer.log_error("voice_translation_agent", str(e), {"request": request.dict()})
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/synthesize")
async def synthesize_voice(text: str, language: str = "en"):
    """Synthesize voice from text"""
    try:
        result = voice_service.synthesize_speech(text, language=language)
        return result
    except Exception as e:
        logger.error(f"Voice synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/auto-language")
async def auto_language_voice(request: TranslationRequest):
    """Process voice with automatic language detection"""
    try:
        observer.log_agent_start("auto_language_voice_agent", request.dict())
        
        input_data = {
            "content": request.content,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await auto_language_voice_agent.process_with_voice(input_data)
        
        observer.log_agent_end("auto_language_voice_agent", result, result.get("success", False))
        
        return result
        
    except Exception as e:
        logger.error(f"Auto-language voice processing failed: {e}")
        observer.log_error("auto_language_voice_agent", str(e), {"request": request.dict()})
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voice/status")
async def voice_status():
    """Get voice service status"""
    try:
        return voice_translation_agent.get_voice_status()
    except Exception as e:
        logger.error(f"Voice status check failed: {e}")
        return {"error": str(e)}

# Monetization endpoints
@app.get("/monetization/subscription/{user_id}")
async def get_subscription_info(user_id: str):
    """Get user subscription information"""
    try:
        result = monetization_service.get_user_subscription_info(user_id)
        return result
    except Exception as e:
        logger.error(f"Subscription info retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monetization/pricing")
async def get_pricing_info():
    """Get pricing information for all services"""
    try:
        return {
            "success": True,
            "pricing": monetization_service.service_pricing,
            "currency": "USD",
            "description": "RealityCheck AI Financial Assistant Pricing"
        }
    except Exception as e:
        logger.error(f"Pricing info retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monetization/check-access")
async def check_user_access(user_id: str, service_type: str):
    """Check if user has access to a service"""
    try:
        result = monetization_service.check_user_access(user_id, service_type)
        return result
    except Exception as e:
        logger.error(f"Access check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monetization/process-request")
async def process_monetized_request(user_id: str, service_type: str, request_data: dict):
    """Process a service request with monetization"""
    try:
        result = monetization_service.process_service_request(user_id, service_type, request_data)
        return result
    except Exception as e:
        logger.error(f"Monetized request processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monetization/analytics")
async def get_monetization_analytics(start_date: str = None, end_date: str = None):
    """Get monetization analytics"""
    try:
        result = monetization_service.get_monetization_analytics(start_date, end_date)
        return result
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monetization/create-plans")
async def create_subscription_plans():
    """Create subscription plans"""
    try:
        result = monetization_service.create_subscription_plans()
        return result
    except Exception as e:
        logger.error(f"Plan creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

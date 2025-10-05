"""
Main application entry point for RealityCheck agent system
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
from voice.elevenlabs_service import ElevenLabsVoiceService
from observability.comet_integration import CometObserver

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RealityCheck Agent System",
    description="Multi-agent system for financial planning and remittance",
    version="1.0.0"
)

# Initialize components
orchestrator = AgentOrchestrator()
observer = CometObserver()
voice_translation_agent = VoiceTranslationAgent()
voice_service = ElevenLabsVoiceService()

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

@app.get("/voice/status")
async def voice_status():
    """Get voice service status"""
    try:
        return voice_translation_agent.get_voice_status()
    except Exception as e:
        logger.error(f"Voice status check failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

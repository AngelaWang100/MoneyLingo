"""
Simple backend server for MoneyLingo voice features
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MoneyLingo Simple Backend",
    description="Simple backend for voice features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    success: bool = True

class VoiceRequest(BaseModel):
    text: str
    language: str = "en"

class VoiceResponse(BaseModel):
    audio_url: str
    success: bool = True

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "MoneyLingo Simple Backend is running", "status": "healthy"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    try:
        # Simple AI responses based on keywords
        message = request.message.lower()
        
        if "hello" in message or "hi" in message:
            response = "Hello! I'm your MoneyLingo financial assistant. How can I help you today?"
        elif "budget" in message:
            response = "Let me help you create a budget. First, tell me about your monthly income and expenses."
        elif "save" in message or "saving" in message:
            response = "Great! Let's talk about saving strategies. What's your current financial goal?"
        elif "invest" in message or "investment" in message:
            response = "Investing can help grow your wealth over time. What's your investment timeline and risk tolerance?"
        elif "credit" in message:
            response = "Credit management is crucial for financial health. I can help you understand credit scores, building credit, and managing debt."
        elif "debt" in message:
            response = "Let's tackle your debt together. What types of debt do you have and what are the interest rates?"
        elif "retirement" in message:
            response = "Planning for retirement is important at any age. Let's discuss your retirement goals and timeline."
        elif "tax" in message:
            response = "Tax planning can save you money. I can help you understand deductions, credits, and tax-advantaged accounts."
        else:
            response = f"I understand you're asking about '{request.message}'. As your financial assistant, I'm here to help with budgeting, saving, investing, credit, and financial planning. Could you be more specific about what you'd like to know?"
        
        return ChatResponse(response=response, success=True)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/synthesize", response_model=VoiceResponse)
async def synthesize_voice(request: VoiceRequest):
    """Simple voice synthesis endpoint"""
    try:
        # For now, return a mock audio URL
        # In a real implementation, this would generate actual audio
        mock_audio_url = f"data:audio/speech;text={request.text}"
        
        return VoiceResponse(
            audio_url=mock_audio_url,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Voice synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_text(request: Dict[str, Any]):
    """Simple translation endpoint"""
    try:
        text = request.get("text", "")
        target_language = request.get("target_language", "en")
        
        # Simple mock translation
        translated_text = f"[Translated to {target_language}] {text}"
        
        return {
            "translated_text": translated_text,
            "source_language": "auto",
            "target_language": target_language,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/financial/advice")
async def get_financial_advice(request: Dict[str, Any]):
    """Simple financial advice endpoint"""
    try:
        question = request.get("question", "")
        
        # Simple financial advice based on keywords
        if "budget" in question.lower():
            advice = "Start by tracking your income and expenses. Create a 50/30/20 budget: 50% for needs, 30% for wants, 20% for savings and debt repayment."
        elif "save" in question.lower():
            advice = "Set up automatic transfers to a high-yield savings account. Start with an emergency fund of 3-6 months of expenses."
        elif "invest" in question.lower():
            advice = "Consider starting with low-cost index funds or ETFs. Diversify your portfolio and invest for the long term."
        else:
            advice = "I recommend starting with a budget, building an emergency fund, and then considering investments based on your goals and risk tolerance."
        
        return {
            "advice": advice,
            "recommendations": ["Create a budget", "Build emergency fund", "Start investing"],
            "risk_level": "moderate",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Financial advice error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

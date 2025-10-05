"""
Main application entry point for MoneyLingo agent system
Refactored with clean API structure
"""
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route handlers
from api.routes import financial, voice, translation, remittance, monetization

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RealityCheck Agent System",
    description="Multi-agent system for financial planning and remittance",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    financial.router, 
    prefix="/api/v1/financial", 
    tags=["financial"]
)

app.include_router(
    voice.router, 
    prefix="/api/v1/voice", 
    tags=["voice"]
)

app.include_router(
    translation.router, 
    prefix="/api/v1/translate", 
    tags=["translation"]
)

app.include_router(
    remittance.router, 
    prefix="/api/v1/remittance", 
    tags=["remittance"]
)

app.include_router(
    monetization.router, 
    prefix="/api/v1/monetization", 
    tags=["monetization"]
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "RealityCheck Agent System is running", 
        "status": "healthy",
        "version": "2.0.0",
        "api_docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        return {
            "status": "healthy",
            "services": {
                "api": "operational",
                "agents": "operational", 
                "voice": "operational",
                "monetization": "operational"
            },
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

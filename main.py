# FastAPI app for explaining financial transactions in plain language with multi-language support

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MoneyLingo router
from api.routes.moneylingo import router as moneylingo_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MoneyLingo API",
    description="Financial transaction explanation service with multi-language support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the MoneyLingo router
app.include_router(moneylingo_router, prefix="/api", tags=["MoneyLingo"])

# Simple root endpoint
@app.get("/")
async def root():
    return {
        "message": "MoneyLingo API - Financial Transaction Explanations", 
        "version": "1.0.0",
        "description": "Explains confusing transactions in plain language and translates to your preferred language",
        "documentation": "/docs",
        "key_features": [
            "Transaction explanations in plain language",
            "Multi-language support (English, Spanish, Hindi, Chinese, French, Arabic)",
            "PDF bank statement processing",
            "Voice responses (coming soon)",
            "Spending analysis and insights"
        ],
        "main_endpoints": {
            "explain_transaction": "/api/explain-transaction",
            "upload_pdf": "/api/upload-pdf", 
            "ask_question": "/api/ask-question",
            "customers": "/api/customers",
            "accounts": "/api/accounts",
            "spending_summary": "/api/spending-summary/{customer_id}"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "moneylingo-api", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

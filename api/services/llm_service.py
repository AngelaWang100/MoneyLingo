# LLM Service - No Mock Responses
# All responses must come from real AI backend

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """
    LLM service that requires real AI backend.
    No mock responses - all functionality requires actual AI.
    """
    def __init__(self):
        logger.info("Initialized LLMService - requires real AI backend")

    async def explain_transaction(self, transaction: Dict[str, Any]) -> str:
        """Generates a plain-language explanation for a transaction."""
        logger.error("Real AI backend is required for transaction explanation")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

    async def explain_transaction_text(self, transaction_text: str) -> str:
        """Generates a plain-language explanation for a raw transaction string."""
        logger.error("Real AI backend is required for transaction text explanation")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

    async def answer_financial_question(self, question: str, context: str) -> str:
        """Answers a financial question based on provided context."""
        logger.error("Real AI backend is required for financial question answering")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

    async def generate_spending_analysis(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates a spending analysis from a list of transactions."""
        logger.error("Real AI backend is required for spending analysis")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

# Create a single instance of the service
llm_service = LLMService()
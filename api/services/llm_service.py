# This is a placeholder for a real Large Language Model (LLM) service.

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """
    A placeholder service for LLM-based financial analysis.
    Currently, it returns mock explanations and analysis.
    """
    def __init__(self):
        logger.info("Initialized placeholder LLMService")

    async def explain_transaction(self, transaction: Dict[str, Any]) -> str:
        """Generates a plain-language explanation for a transaction."""
        logger.info(f"Generating mock explanation for transaction: {transaction.get('_id')}")
        description = transaction.get('description', 'N/A')
        return f"This is a mock explanation for the transaction: '{description}'."

    async def explain_transaction_text(self, transaction_text: str) -> str:
        """Generates a plain-language explanation for a raw transaction string."""
        logger.info(f"Generating mock explanation for text: '{transaction_text}'")
        return f"This is a mock explanation for the transaction text: '{transaction_text}'."

    async def answer_financial_question(self, question: str, context: str) -> str:
        """Answers a financial question based on provided context."""
        logger.info(f"Generating mock answer for question: '{question}'")
        return f"This is a mock answer to your question about '{question}'. The provided context was: '{context}'."

    async def generate_spending_analysis(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates a spending analysis from a list of transactions."""
        logger.info(f"Generating mock spending analysis for {len(transactions)} transactions.")
        return {
            "summary": "This is a mock spending summary. You have spent most of your money on mock purchases.",
            "by_category": {
                "Shopping": 500.0,
                "Groceries": 300.0,
                "Restaurants": 200.0
            }
        }

# Create a single instance of the service
llm_service = LLMService()

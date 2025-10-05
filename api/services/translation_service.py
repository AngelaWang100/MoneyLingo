# Translation Service - No Mock Responses
# All translations must come from real AI backend

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    """
    Translation service that requires real AI backend.
    No mock responses - all translations require actual AI.
    """
    def __init__(self):
        logger.info("Initialized TranslationService - requires real AI backend")

    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language using real AI backend."""
        logger.error("Real AI backend is required for translation")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

    async def translate_financial_content(self, content: str, target_language: str) -> str:
        """Translate financial content to target language using real AI backend."""
        logger.error("Real AI backend is required for financial content translation")
        raise NotImplementedError("Real AI backend is required - no mock responses available")

# Create a single instance of the service
translation_service = TranslationService()
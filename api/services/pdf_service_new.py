# This is a placeholder for a real PDF processing service.

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFService:
    """
    A placeholder service for processing uploaded PDF bank statements.
    """
    def __init__(self):
        logger.info("Initialized placeholder PDFService")

    async def process_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """
        Processes an uploaded PDF file.

        Args:
            file_content: The byte content of the PDF file.

        Returns:
            A dictionary with extracted data.
        """
        logger.info(f"Processing PDF with size: {len(file_content)} bytes (mock processing)")

        # Parse the PDF here
        return {
            "summary": {
                "account_holder": "Mock Account Holder",
                "account_number": "xxxx-xxxx-1234",
                "statement_period": "2025-09-01 to 2025-09-30"
            },
            "transactions": [
                {
                    "date": "2025-09-15",
                    "description": "Mock Purchase at Store",
                    "amount": -50.75
                },
                {
                    "date": "2025-09-10",
                    "description": "Mock Deposit",
                    "amount": 1000.00
                }
            ]
        }

# Create a single instance of the service
pdf_service = PDFService()

"""
Remittance agent for XRPL testnet integration
"""
import os
import requests
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from .base_agent import BaseAgent

class RemittanceAgent(BaseAgent):
    """Agent for handling remittance operations via XRPL testnet"""
    
    def __init__(self):
        super().__init__(
            name="remittance_agent",
            description="Handles remittance operations and XRPL testnet integration"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
        self.backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process remittance request"""
        try:
            amount = input_data.get("amount", 0)
            currency = input_data.get("currency", "USD")
            destination = input_data.get("destination", "")
            source_country = input_data.get("source_country", "")
            destination_country = input_data.get("destination_country", "")
            
            # Create remittance analysis prompt
            analysis_prompt = f"""
            Analyze this remittance request:
            - Amount: {amount} {currency}
            - From: {source_country}
            - To: {destination_country}
            - Destination: {destination}
            
            Provide:
            1. Cost analysis (fees, exchange rates)
            2. Time estimates
            3. Risk assessment
            4. Alternative options
            5. Compliance considerations
            """
            
            messages = [
                SystemMessage(content="You are a remittance and cross-border payment expert. Analyze the request and provide detailed insights."),
                HumanMessage(content=analysis_prompt)
            ]
            
            # Get AI analysis
            response = await self.llm.ainvoke(messages)
            
            # Call backend remittance API
            remittance_data = await self._call_remittance_api(amount, currency, destination)
            
            # Log the remittance decision
            self.log_decision(
                decision=f"Processed remittance of {amount} {currency}",
                context={
                    "amount": amount,
                    "currency": currency,
                    "source": source_country,
                    "destination": destination_country,
                    "backend_connected": remittance_data.get("success", False)
                },
                confidence=0.9
            )
            
            return {
                "ai_analysis": response.content,
                "remittance_data": remittance_data,
                "agent": self.name,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Remittance processing failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    async def _call_remittance_api(self, amount: float, currency: str, destination: str) -> Dict[str, Any]:
        """Call the backend remittance API"""
        try:
            url = f"{self.backend_url}{os.getenv('REMITTANCE_ENDPOINT', '/remittance')}"
            payload = {
                "amount": amount,
                "currency": currency,
                "destination": destination
            }
            response = requests.post(url, json=payload, timeout=15)
            return response.json() if response.status_code == 200 else {"success": False, "error": "API call failed"}
        except Exception as e:
            self.logger.warning(f"Remittance API call failed: {e}")
            return {"success": False, "error": str(e)}

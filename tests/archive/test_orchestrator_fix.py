"""
Test orchestrator with lazy initialization
"""
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LazyAgentOrchestrator:
    """Orchestrator with lazy agent initialization"""
    
    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        self._translation_agent = None
        self._financial_planning_agent = None
        self._remittance_agent = None
    
    @property
    def translation_agent(self):
        if self._translation_agent is None:
            from agents.translation_agent import TranslationAgent
            self._translation_agent = TranslationAgent()
        return self._translation_agent
    
    @property
    def financial_planning_agent(self):
        if self._financial_planning_agent is None:
            from agents.financial_planning_agent import FinancialPlanningAgent
            self._financial_planning_agent = FinancialPlanningAgent()
        return self._financial_planning_agent
    
    @property
    def remittance_agent(self):
        if self._remittance_agent is None:
            from agents.remittance_agent import RemittanceAgent
            self._remittance_agent = RemittanceAgent()
        return self._remittance_agent
    
    async def process_request(self, input_data: dict) -> dict:
        """Process a request through all agents"""
        try:
            # Translation
            translation_result = await self.translation_agent.process(input_data)
            
            # Financial Planning
            financial_result = await self.financial_planning_agent.process(input_data)
            
            # Remittance
            remittance_result = await self.remittance_agent.process(input_data)
            
            return {
                "success": True,
                "translation": translation_result,
                "financial_planning": financial_result,
                "remittance": remittance_result,
                "message": "All agents processed successfully"
            }
        except Exception as e:
            self.logger.error(f"Orchestrator processing failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

async def test_lazy_orchestrator():
    """Test the lazy orchestrator"""
    print("🧪 Testing Lazy Agent Orchestrator")
    print("=" * 50)
    
    try:
        orchestrator = LazyAgentOrchestrator()
        print("✅ Orchestrator created successfully")
        
        # Test with sample data
        input_data = {
            "content": "I want to save for retirement and send money to Mexico",
            "language": "Spanish",
            "user_level": "beginner",
            "user_profile": {
                "age": 25,
                "income": 50000,
                "savings": 10000,
                "goals": ["retirement", "house"]
            },
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico"
        }
        
        print("📝 Processing request through all agents...")
        result = await orchestrator.process_request(input_data)
        
        if result.get("success"):
            print("✅ Orchestrator: SUCCESS")
            print(f"📄 Translation length: {len(result.get('translation', {}).get('translated_content', ''))}")
            print(f"📄 Financial planning length: {len(result.get('financial_planning', {}).get('ai_recommendations', ''))}")
            print(f"📄 Remittance length: {len(result.get('remittance', {}).get('ai_analysis', ''))}")
        else:
            print(f"❌ Orchestrator: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Lazy Orchestrator Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_lazy_orchestrator())

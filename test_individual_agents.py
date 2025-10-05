"""
Test individual agents without orchestrator
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

async def test_individual_agents():
    """Test each agent individually"""
    print("🧪 Testing Individual RealityCheck Agents")
    print("=" * 50)
    
    # Test Translation Agent
    print("\n🌍 Testing Translation Agent...")
    try:
        from agents.translation_agent import TranslationAgent
        translation_agent = TranslationAgent()
        
        input_data = {
            "content": "Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods.",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await translation_agent.process(input_data)
        if result.get("success"):
            print("✅ Translation Agent: SUCCESS")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
        else:
            print(f"❌ Translation Agent: {result.get('error')}")
    except Exception as e:
        print(f"❌ Translation Agent failed: {e}")
    
    # Test Financial Planning Agent
    print("\n💰 Testing Financial Planning Agent...")
    try:
        from agents.financial_planning_agent import FinancialPlanningAgent
        financial_agent = FinancialPlanningAgent()
        
        input_data = {
            "user_profile": {
                "age": 25,
                "income": 50000,
                "savings": 10000,
                "goals": ["retirement", "house"]
            },
            "request": "Create a financial plan for retirement"
        }
        
        result = await financial_agent.process(input_data)
        if result.get("success"):
            print("✅ Financial Planning Agent: SUCCESS")
            print(f"📄 AI recommendations length: {len(result.get('ai_recommendations', ''))}")
        else:
            print(f"❌ Financial Planning Agent: {result.get('error')}")
    except Exception as e:
        print(f"❌ Financial Planning Agent failed: {e}")
    
    # Test Remittance Agent
    print("\n💸 Testing Remittance Agent...")
    try:
        from agents.remittance_agent import RemittanceAgent
        remittance_agent = RemittanceAgent()
        
        input_data = {
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico",
            "user_preferences": {"speed": "fast", "cost": "low"}
        }
        
        result = await remittance_agent.process(input_data)
        if result.get("success"):
            print("✅ Remittance Agent: SUCCESS")
            print(f"📄 AI analysis length: {len(result.get('ai_analysis', ''))}")
        else:
            print(f"❌ Remittance Agent: {result.get('error')}")
    except Exception as e:
        print(f"❌ Remittance Agent failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Individual Agent Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_individual_agents())

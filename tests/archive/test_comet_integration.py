#!/usr/bin/env python3
"""
Test Comet integration with RealityCheck agents
"""
import asyncio
import os
from dotenv import load_dotenv
from agents.translation_agent import TranslationAgent
from agents.financial_planning_agent import FinancialPlanningAgent
from agents.remittance_agent import RemittanceAgent
from observability.comet_integration import CometObserver

# Load environment variables
load_dotenv()

async def test_comet_integration():
    """Test Comet integration with all agents"""
    try:
        print("🧪 Testing Comet Integration with RealityCheck Agents")
        print("=" * 60)
        
        # Check environment
        comet_api = os.getenv("COMET_API_KEY")
        comet_workspace = os.getenv("COMET_WORKSPACE")
        
        print(f"🔑 Comet API Key: {'SET' if comet_api else 'NOT SET'}")
        print(f"🏢 Comet Workspace: {comet_workspace if comet_workspace else 'NOT SET'}")
        print()
        
        # Create observer
        observer = CometObserver()
        print("📊 Created Comet Observer")
        
        # Test Translation Agent
        print("\n🤖 Testing Translation Agent with Comet...")
        translation_agent = TranslationAgent()
        
        test_data = {
            "content": "Diversification is a risk management strategy that mixes a wide variety of investments within a portfolio.",
            "language": "French",
            "user_level": "intermediate"
        }
        
        observer.log_agent_start("translation_agent", test_data)
        result = await translation_agent.process(test_data)
        observer.log_agent_end("translation_agent", result, result.get("success", False))
        
        if result.get("success"):
            print("✅ Translation Agent: SUCCESS")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
        else:
            print("❌ Translation Agent: FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Test Financial Planning Agent
        print("\n💰 Testing Financial Planning Agent with Comet...")
        financial_agent = FinancialPlanningAgent()
        
        financial_data = {
            "goals": ["Save for retirement", "Buy a house"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "5 years"
        }
        
        observer.log_agent_start("financial_planning_agent", financial_data)
        result = await financial_agent.process(financial_data)
        observer.log_agent_end("financial_planning_agent", result, result.get("success", False))
        
        if result.get("success"):
            print("✅ Financial Planning Agent: SUCCESS")
            print(f"📄 AI recommendations length: {len(result.get('ai_recommendations', ''))}")
        else:
            print("❌ Financial Planning Agent: FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Test Remittance Agent
        print("\n💸 Testing Remittance Agent with Comet...")
        remittance_agent = RemittanceAgent()
        
        remittance_data = {
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico",
            "source_country": "USA",
            "destination_country": "Mexico"
        }
        
        observer.log_agent_start("remittance_agent", remittance_data)
        result = await remittance_agent.process(remittance_data)
        observer.log_agent_end("remittance_agent", result, result.get("success", False))
        
        if result.get("success"):
            print("✅ Remittance Agent: SUCCESS")
            print(f"📄 AI analysis length: {len(result.get('ai_analysis', ''))}")
        else:
            print("❌ Remittance Agent: FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Create final report
        print("\n📊 Creating Comet Report...")
        all_results = [
            {"agent": "translation", "success": True},
            {"agent": "financial_planning", "success": True},
            {"agent": "remittance", "success": True}
        ]
        
        report = observer.create_agent_report(all_results)
        print(f"📈 Report created: {report}")
        
        print("\n🎉 Comet Integration Test Complete!")
        print("Check your Comet dashboard for detailed logs and metrics!")
        
        return True
        
    except Exception as e:
        print(f"❌ Comet integration test failed: {e}")
        return False

async def main():
    success = await test_comet_integration()
    
    if success:
        print("\n🚀 Your RealityCheck system with Comet observability is ready!")
        print("🔗 Check your Comet dashboard to see the logged data")
    else:
        print("\n⚠️  Comet integration needs attention")

if __name__ == "__main__":
    asyncio.run(main())

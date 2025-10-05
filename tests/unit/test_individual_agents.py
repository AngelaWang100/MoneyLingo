"""
Unit tests for individual agents
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_translation_agent():
    """Test translation agent individually"""
    try:
        from api.services.agents.translation_agent import TranslationAgent
        
        agent = TranslationAgent()
        logger.info("✅ Translation agent initialized")
        
        test_data = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        success = result.get("success", False)
        logger.info(f"Translation agent result: {success}")
        return success
        
    except Exception as e:
        logger.error(f"Translation agent test failed: {e}")
        return False

async def test_financial_planning_agent():
    """Test financial planning agent individually"""
    try:
        from api.services.agents.financial_planning_agent import FinancialPlanningAgent
        
        agent = FinancialPlanningAgent()
        logger.info("✅ Financial planning agent initialized")
        
        test_data = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        success = result.get("success", False)
        logger.info(f"Financial planning agent result: {success}")
        return success
        
    except Exception as e:
        logger.error(f"Financial planning agent test failed: {e}")
        return False

async def test_remittance_agent():
    """Test remittance agent individually"""
    try:
        from api.services.agents.remittance_agent import RemittanceAgent
        
        agent = RemittanceAgent()
        logger.info("✅ Remittance agent initialized")
        
        test_data = {
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico",
            "source_country": "United States",
            "destination_country": "Mexico"
        }
        
        result = await agent.process(test_data)
        success = result.get("success", False)
        logger.info(f"Remittance agent result: {success}")
        return success
        
    except Exception as e:
        logger.error(f"Remittance agent test failed: {e}")
        return False

async def test_voice_services():
    """Test voice services individually"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        service = ElevenLabsVoiceService()
        logger.info("✅ Voice service initialized")
        
        result = service.synthesize_speech("Hello, this is a test", language="en")
        success = result.get("success", False)
        logger.info(f"Voice service result: {success}")
        return success
        
    except Exception as e:
        logger.error(f"Voice service test failed: {e}")
        return False

async def run_unit_tests():
    """Run all unit tests"""
    logger.info("🚀 Starting unit tests...")
    
    tests = [
        ("Translation Agent", test_translation_agent),
        ("Financial Planning Agent", test_financial_planning_agent),
        ("Remittance Agent", test_remittance_agent),
        ("Voice Services", test_voice_services),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Testing {test_name}...")
        try:
            result = await test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status}: {test_name}")
        except Exception as e:
            logger.error(f"❌ FAILED: {test_name} - {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 UNIT TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} unit tests passed")
    
    if passed == total:
        logger.info("🎉 All unit tests passed!")
    else:
        logger.warning(f"⚠️  {total - passed} unit tests failed.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_unit_tests())

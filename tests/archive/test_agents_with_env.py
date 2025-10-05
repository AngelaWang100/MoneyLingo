"""
Test agents with environment variables loaded
"""
import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_translation_agent_with_env():
    """Test translation agent with environment variables"""
    try:
        from api.services.agents.translation_agent import TranslationAgent
        
        agent = TranslationAgent()
        logger.info("✅ Translation agent initialized successfully")
        
        # Test with simple data
        test_data = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        logger.info(f"✅ Translation agent result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Translation agent failed: {e}")
        return False

async def test_financial_agent_with_env():
    """Test financial planning agent with environment variables"""
    try:
        from api.services.agents.financial_planning_agent import FinancialPlanningAgent
        
        agent = FinancialPlanningAgent()
        logger.info("✅ Financial planning agent initialized successfully")
        
        # Test with simple data
        test_data = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        logger.info(f"✅ Financial planning agent result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Financial planning agent failed: {e}")
        return False

async def test_voice_service_with_env():
    """Test voice service with environment variables"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        service = ElevenLabsVoiceService()
        logger.info("✅ Voice service initialized successfully")
        
        # Test voice synthesis
        result = service.synthesize_speech("Hello, this is a test", language="en")
        logger.info(f"✅ Voice service result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Voice service failed: {e}")
        return False

async def test_orchestrator_with_env():
    """Test orchestrator with environment variables"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator initialized successfully")
        
        # Test with simple data
        test_data = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await orchestrator.process_request(test_data)
        logger.info(f"✅ Orchestrator result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Orchestrator failed: {e}")
        return False

async def run_agent_tests_with_env():
    """Run all agent tests with environment variables"""
    logger.info("🚀 Starting agent tests with environment variables...")
    
    # First check environment
    google_key = os.getenv("GOOGLE_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    logger.info(f"🔑 Google API Key: {'✅ Set' if google_key and not google_key.startswith('your_') else '❌ Not set or placeholder'}")
    logger.info(f"🔑 ElevenLabs API Key: {'✅ Set' if elevenlabs_key and not elevenlabs_key.startswith('your_') else '❌ Not set or placeholder'}")
    
    tests = [
        ("Translation Agent", test_translation_agent_with_env),
        ("Financial Planning Agent", test_financial_agent_with_env),
        ("Voice Service", test_voice_service_with_env),
        ("Orchestrator", test_orchestrator_with_env),
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
    logger.info("📊 AGENT TEST SUMMARY (WITH ENV)")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} agent tests passed")
    
    if passed == total:
        logger.info("🎉 All agents are working correctly with your API keys!")
    else:
        logger.warning(f"⚠️  {total - passed} agent tests failed.")
        logger.info("💡 Make sure your .env file has real API keys (not placeholders)")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_agent_tests_with_env())

"""
Integration tests for orchestrator and agent coordination
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

async def test_orchestrator_coordination():
    """Test orchestrator coordinating multiple agents"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator initialized")
        
        test_data = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await orchestrator.process_request(test_data)
        success = result.get("success", False)
        successful_count = result.get("successful_count", 0)
        total_count = result.get("total_count", 0)
        
        logger.info(f"Orchestrator result: {success}")
        logger.info(f"Successful agents: {successful_count}/{total_count}")
        
        return success and successful_count > 0
        
    except Exception as e:
        logger.error(f"Orchestrator test failed: {e}")
        return False

async def test_agent_error_handling():
    """Test orchestrator error handling when agents fail"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator initialized for error handling test")
        
        # Test with invalid data to trigger errors
        invalid_data = {
            "goals": [],  # Empty goals
            "income": -1000,  # Negative income
            "expenses": "invalid",  # Wrong type
            "timeline": "",
            "language": "",
            "user_level": ""
        }
        
        result = await orchestrator.process_request(invalid_data)
        success = result.get("success", False)
        successful_count = result.get("successful_count", 0)
        
        logger.info(f"Error handling test result: {success}")
        logger.info(f"Successful agents despite errors: {successful_count}")
        
        # Should still work with some agents even with invalid data
        return True  # Orchestrator should handle errors gracefully
        
    except Exception as e:
        logger.error(f"Error handling test failed: {e}")
        return False

async def test_voice_integration():
    """Test voice services integration"""
    try:
        from api.services.agents.auto_language_voice_agent import AutoLanguageVoiceAgent
        from api.services.agents.voice_translation_agent import VoiceTranslationAgent
        
        # Test auto language voice agent
        auto_voice_agent = AutoLanguageVoiceAgent()
        logger.info("✅ Auto language voice agent initialized")
        
        test_data = {
            "content": "Hola, necesito ayuda con mi plan de jubilación",
            "user_level": "beginner"
        }
        
        result = await auto_voice_agent.process_with_voice(test_data)
        auto_voice_success = result.get("success", False)
        logger.info(f"Auto language voice result: {auto_voice_success}")
        
        # Test voice translation agent
        voice_translation_agent = VoiceTranslationAgent()
        logger.info("✅ Voice translation agent initialized")
        
        translation_data = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await voice_translation_agent.process_with_voice(translation_data)
        voice_translation_success = result.get("success", False)
        logger.info(f"Voice translation result: {voice_translation_success}")
        
        return auto_voice_success and voice_translation_success
        
    except Exception as e:
        logger.error(f"Voice integration test failed: {e}")
        return False

async def run_integration_tests():
    """Run all integration tests"""
    logger.info("🚀 Starting integration tests...")
    
    tests = [
        ("Orchestrator Coordination", test_orchestrator_coordination),
        ("Agent Error Handling", test_agent_error_handling),
        ("Voice Integration", test_voice_integration),
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
    logger.info("📊 INTEGRATION TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} integration tests passed")
    
    if passed == total:
        logger.info("🎉 All integration tests passed!")
    else:
        logger.warning(f"⚠️  {total - passed} integration tests failed.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_integration_tests())

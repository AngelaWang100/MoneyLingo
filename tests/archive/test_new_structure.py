"""
Comprehensive test script for the new API structure
"""
import asyncio
import logging
import sys
import os
from typing import Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_orchestrator():
    """Test the agent orchestrator"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator initialized successfully")
        
        # Test with sample data
        test_data = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await orchestrator.process_request(test_data)
        logger.info(f"✅ Orchestrator test result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Orchestrator test failed: {e}")
        return False

async def test_translation_agent():
    """Test the translation agent"""
    try:
        from api.services.agents.translation_agent import TranslationAgent
        
        agent = TranslationAgent()
        logger.info("✅ Translation agent initialized successfully")
        
        test_data = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        logger.info(f"✅ Translation agent test result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Translation agent test failed: {e}")
        return False

async def test_financial_planning_agent():
    """Test the financial planning agent"""
    try:
        from api.services.agents.financial_planning_agent import FinancialPlanningAgent
        
        agent = FinancialPlanningAgent()
        logger.info("✅ Financial planning agent initialized successfully")
        
        test_data = {
            "goals": ["retirement", "emergency fund"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        result = await agent.process(test_data)
        logger.info(f"✅ Financial planning agent test result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Financial planning agent test failed: {e}")
        return False

async def test_remittance_agent():
    """Test the remittance agent"""
    try:
        from api.services.agents.remittance_agent import RemittanceAgent
        
        agent = RemittanceAgent()
        logger.info("✅ Remittance agent initialized successfully")
        
        test_data = {
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico",
            "source_country": "United States",
            "destination_country": "Mexico"
        }
        
        result = await agent.process(test_data)
        logger.info(f"✅ Remittance agent test result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Remittance agent test failed: {e}")
        return False

async def test_voice_service():
    """Test the voice service"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        service = ElevenLabsVoiceService()
        logger.info("✅ Voice service initialized successfully")
        
        # Test voice synthesis
        result = service.synthesize_speech("Hello, this is a test", language="en")
        logger.info(f"✅ Voice service test result: {result.get('success', False)}")
        return result.get('success', False)
        
    except Exception as e:
        logger.error(f"❌ Voice service test failed: {e}")
        return False

async def test_monetization_service():
    """Test the monetization service"""
    try:
        from monetization.monetization_service import RealityCheckMonetization
        
        service = RealityCheckMonetization()
        logger.info("✅ Monetization service initialized successfully")
        
        # Test pricing info
        pricing = service.service_pricing
        logger.info(f"✅ Monetization service has {len(pricing)} service types")
        return True
        
    except Exception as e:
        logger.error(f"❌ Monetization service test failed: {e}")
        return False

async def test_api_routes():
    """Test API route imports"""
    try:
        from api.routes import financial, voice, translation, remittance, monetization
        logger.info("✅ All API routes imported successfully")
        
        # Test route handlers
        from api.models.financial import FinancialRequest
        from api.models.voice import TranslationRequest
        from api.models.remittance import RemittanceRequest
        
        logger.info("✅ All Pydantic models imported successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ API routes test failed: {e}")
        return False

async def test_dependencies():
    """Test dependency injection"""
    try:
        from api.dependencies import (
            get_orchestrator, get_voice_service, 
            get_monetization_service, get_observer
        )
        
        # Test dependency functions
        orchestrator = get_orchestrator()
        voice_service = get_voice_service()
        monetization_service = get_monetization_service()
        observer = get_observer()
        
        logger.info("✅ All dependencies initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Dependencies test failed: {e}")
        return False

async def test_config():
    """Test configuration"""
    try:
        from api.config import settings
        
        logger.info(f"✅ Configuration loaded: {settings.app_name}")
        logger.info(f"✅ Debug mode: {settings.debug}")
        logger.info(f"✅ Host: {settings.host}:{settings.port}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    logger.info("🚀 Starting comprehensive agent tests...")
    
    tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies),
        ("API Routes", test_api_routes),
        ("Orchestrator", test_orchestrator),
        ("Translation Agent", test_translation_agent),
        ("Financial Planning Agent", test_financial_planning_agent),
        ("Remittance Agent", test_remittance_agent),
        ("Voice Service", test_voice_service),
        ("Monetization Service", test_monetization_service),
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
    logger.info("📊 TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All agents are working correctly!")
    else:
        logger.warning(f"⚠️  {total - passed} tests failed. Check the logs above.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_all_tests())

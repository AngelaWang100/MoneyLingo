"""
Test agent instantiation without API calls
"""
import sys
import os
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_agent_instantiation():
    """Test that agents can be instantiated"""
    try:
        # Test base agent
        from api.services.agents.base_agent import BaseAgent
        
        class TestAgent(BaseAgent):
            async def process(self, input_data):
                return {"success": True, "test": "passed"}
        
        test_agent = TestAgent("test_agent", "Test agent")
        logger.info("✅ Base agent works correctly")
        
        # Test orchestrator (without running)
        from api.services.agents.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator instantiated successfully")
        
        # Test individual agents (without API calls)
        from api.services.agents.translation_agent import TranslationAgent
        translation_agent = TranslationAgent()
        logger.info("✅ Translation agent instantiated")
        
        from api.services.agents.financial_planning_agent import FinancialPlanningAgent
        financial_agent = FinancialPlanningAgent()
        logger.info("✅ Financial planning agent instantiated")
        
        from api.services.agents.remittance_agent import RemittanceAgent
        remittance_agent = RemittanceAgent()
        logger.info("✅ Remittance agent instantiated")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent instantiation failed: {e}")
        return False

def test_voice_service():
    """Test voice service instantiation"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        voice_service = ElevenLabsVoiceService()
        logger.info("✅ Voice service instantiated successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Voice service instantiation failed: {e}")
        return False

def test_monetization_service():
    """Test monetization service instantiation"""
    try:
        from monetization.monetization_service import RealityCheckMonetization
        monetization_service = RealityCheckMonetization()
        logger.info("✅ Monetization service instantiated successfully")
        
        # Test pricing access
        pricing = monetization_service.service_pricing
        logger.info(f"✅ Pricing has {len(pricing)} service types")
        return True
        
    except Exception as e:
        logger.error(f"❌ Monetization service instantiation failed: {e}")
        return False

def test_dependencies():
    """Test dependency injection"""
    try:
        from api.dependencies import (
            get_orchestrator, get_voice_service, 
            get_monetization_service, get_observer
        )
        
        # Test that dependencies can be called
        orchestrator = get_orchestrator()
        voice_service = get_voice_service()
        monetization_service = get_monetization_service()
        observer = get_observer()
        
        logger.info("✅ All dependencies work correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Dependencies test failed: {e}")
        return False

def run_instantiation_tests():
    """Run all instantiation tests"""
    logger.info("🚀 Starting agent instantiation tests...")
    
    tests = [
        ("Agent Instantiation", test_agent_instantiation),
        ("Voice Service", test_voice_service),
        ("Monetization Service", test_monetization_service),
        ("Dependencies", test_dependencies),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Testing {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status}: {test_name}")
        except Exception as e:
            logger.error(f"❌ FAILED: {test_name} - {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 INSTANTIATION TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} instantiation tests passed")
    
    if passed == total:
        logger.info("🎉 All agents can be instantiated correctly!")
    else:
        logger.warning(f"⚠️  {total - passed} instantiation tests failed.")
    
    return results

if __name__ == "__main__":
    run_instantiation_tests()

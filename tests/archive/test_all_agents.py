"""
Test all agents in the new API structure
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_all_agents():
    """Test all agents in the system"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        from api.services.agents.translation_agent import TranslationAgent
        from api.services.agents.financial_planning_agent import FinancialPlanningAgent
        from api.services.agents.remittance_agent import RemittanceAgent
        from api.services.agents.auto_language_voice_agent import AutoLanguageVoiceAgent
        from api.services.agents.voice_translation_agent import VoiceTranslationAgent
        from api.services.agents.tavily_research_agent import TavilyResearchAgent
        
        logger.info("✅ All agents imported successfully")
        
        # Test individual agents
        agents = {
            "Translation Agent": TranslationAgent(),
            "Financial Planning Agent": FinancialPlanningAgent(),
            "Remittance Agent": RemittanceAgent(),
            "Auto Language Voice Agent": AutoLanguageVoiceAgent(),
            "Voice Translation Agent": VoiceTranslationAgent(),
            "Tavily Research Agent": TavilyResearchAgent(),
        }
        
        test_data = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner",
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "query": "retirement planning strategies"
        }
        
        results = {}
        
        for agent_name, agent in agents.items():
            logger.info(f"\n🧪 Testing {agent_name}...")
            try:
                result = await agent.process(test_data)
                success = result.get("success", False)
                results[agent_name] = success
                status = "✅ PASSED" if success else "❌ FAILED"
                logger.info(f"{status}: {agent_name}")
            except Exception as e:
                logger.error(f"❌ FAILED: {agent_name} - {e}")
                results[agent_name] = False
        
        # Test orchestrator
        logger.info(f"\n🧪 Testing Orchestrator...")
        try:
            orchestrator = AgentOrchestrator()
            result = await orchestrator.process_request(test_data)
            success = result.get("success", False)
            results["Orchestrator"] = success
            status = "✅ PASSED" if success else "❌ FAILED"
            logger.info(f"{status}: Orchestrator")
        except Exception as e:
            logger.error(f"❌ FAILED: Orchestrator - {e}")
            results["Orchestrator"] = False
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("📊 COMPREHENSIVE AGENT TEST SUMMARY")
        logger.info("="*60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for agent_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status}: {agent_name}")
        
        logger.info(f"\n🎯 Overall: {passed}/{total} agents passed")
        
        if passed == total:
            logger.info("🎉 ALL AGENTS ARE WORKING PERFECTLY!")
        else:
            logger.warning(f"⚠️  {total - passed} agents failed.")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Test setup failed: {e}")
        return {}

async def test_voice_services():
    """Test voice services"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        voice_service = ElevenLabsVoiceService()
        logger.info("✅ Voice service initialized")
        
        # Test voice synthesis
        result = voice_service.synthesize_speech("Hello, this is a test", language="en")
        success = result.get("success", False)
        
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{status}: Voice Service")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Voice service test failed: {e}")
        return False

async def test_observability():
    """Test observability services"""
    try:
        from api.services.observability.comet_integration import CometObserver
        
        observer = CometObserver()
        logger.info("✅ Observability service initialized")
        
        # Test logging
        observer.log_agent_start("test_agent", {"test": "data"})
        observer.log_agent_end("test_agent", {"result": "success"}, True)
        
        status_info = observer.get_observability_status()
        logger.info(f"✅ Observability status: {status_info}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Observability test failed: {e}")
        return False

async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    logger.info("🚀 Starting comprehensive agent tests...")
    
    tests = [
        ("All Agents", test_all_agents),
        ("Voice Services", test_voice_services),
        ("Observability", test_observability),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"🧪 Testing {test_name}...")
        try:
            result = await test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status}: {test_name}")
        except Exception as e:
            logger.error(f"❌ FAILED: {test_name} - {e}")
            results[test_name] = False
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("🏆 FINAL COMPREHENSIVE TEST SUMMARY")
    logger.info("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} test categories passed")
    
    if passed == total:
        logger.info("🎉 ALL SYSTEMS ARE WORKING PERFECTLY!")
        logger.info("🚀 Your RealityCheck platform is ready for hackathon success!")
    else:
        logger.warning(f"⚠️  {total - passed} test categories failed.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())

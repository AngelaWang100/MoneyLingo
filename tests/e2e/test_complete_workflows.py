"""
End-to-end tests for complete user workflows
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

async def test_retirement_planning_workflow():
    """Test complete retirement planning workflow"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Starting retirement planning workflow")
        
        # Complete retirement planning request
        retirement_data = {
            "goals": ["retirement planning", "emergency fund"],
            "income": 75000,
            "expenses": 45000,
            "timeline": "5 years",
            "language": "English",
            "user_level": "intermediate"
        }
        
        result = await orchestrator.process_request(retirement_data)
        success = result.get("success", False)
        successful_agents = result.get("result", {}).get("successful_agents", [])
        
        logger.info(f"Retirement planning workflow result: {success}")
        logger.info(f"Successful agents: {successful_agents}")
        
        # Check if we got meaningful results
        agent_results = result.get("result", {}).get("agent_results", {})
        has_financial_advice = False
        has_translation = False
        
        for agent_name, agent_result in agent_results.items():
            if agent_result.get("success"):
                result_data = agent_result.get("result", {})
                if "ai_recommendations" in result_data:
                    has_financial_advice = True
                if "translated_content" in result_data:
                    has_translation = True
        
        logger.info(f"Has financial advice: {has_financial_advice}")
        logger.info(f"Has translation: {has_translation}")
        
        return success and len(successful_agents) >= 2
        
    except Exception as e:
        logger.error(f"Retirement planning workflow failed: {e}")
        return False

async def test_multilingual_workflow():
    """Test multilingual user workflow"""
    try:
        from api.services.agents.auto_language_voice_agent import AutoLanguageVoiceAgent
        from api.services.agents.voice_translation_agent import VoiceTranslationAgent
        
        logger.info("✅ Starting multilingual workflow")
        
        # Test Spanish user
        spanish_data = {
            "content": "Hola, necesito ayuda con mi plan de inversión para la jubilación",
            "user_level": "beginner"
        }
        
        auto_voice_agent = AutoLanguageVoiceAgent()
        spanish_result = await auto_voice_agent.process_with_voice(spanish_data)
        spanish_success = spanish_result.get("success", False)
        detected_language = spanish_result.get("detected_language", "Unknown")
        
        logger.info(f"Spanish workflow result: {spanish_success}")
        logger.info(f"Detected language: {detected_language}")
        
        # Test French user
        french_data = {
            "content": "Bonjour, je veux investir mon argent pour ma retraite",
            "user_level": "intermediate"
        }
        
        french_result = await auto_voice_agent.process_with_voice(french_data)
        french_success = french_result.get("success", False)
        french_detected = french_result.get("detected_language", "Unknown")
        
        logger.info(f"French workflow result: {french_success}")
        logger.info(f"Detected language: {french_detected}")
        
        # Test voice translation
        voice_translation_agent = VoiceTranslationAgent()
        translation_data = {
            "content": "I need help with investment strategies",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        translation_result = await voice_translation_agent.process_with_voice(translation_data)
        translation_success = translation_result.get("success", False)
        
        logger.info(f"Voice translation result: {translation_success}")
        
        return spanish_success and french_success and translation_success
        
    except Exception as e:
        logger.error(f"Multilingual workflow failed: {e}")
        return False

async def test_research_workflow():
    """Test financial research workflow"""
    try:
        from api.services.agents.tavily_research_agent import TavilyResearchAgent
        
        logger.info("✅ Starting research workflow")
        
        research_agent = TavilyResearchAgent()
        
        # Test different research queries
        research_queries = [
            {
                "query": "sustainable investing trends 2024",
                "research_type": "sustainable_investing",
                "max_results": 3
            },
            {
                "query": "cryptocurrency market analysis",
                "research_type": "market_analysis",
                "max_results": 2
            }
        ]
        
        all_successful = True
        
        for i, query_data in enumerate(research_queries, 1):
            logger.info(f"Research query {i}: {query_data['query']}")
            
            result = await research_agent.process(query_data)
            success = result.get("success", False)
            research_results = result.get("research_results", [])
            
            logger.info(f"Research {i} result: {success}")
            logger.info(f"Research results found: {len(research_results)}")
            
            if not success:
                all_successful = False
        
        return all_successful
        
    except Exception as e:
        logger.error(f"Research workflow failed: {e}")
        return False

async def test_voice_synthesis_workflow():
    """Test complete voice synthesis workflow"""
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        logger.info("✅ Starting voice synthesis workflow")
        
        voice_service = ElevenLabsVoiceService()
        
        # Test different languages and content
        test_cases = [
            {"text": "Welcome to RealityCheck financial assistant", "language": "en"},
            {"text": "Bienvenido al asistente financiero RealityCheck", "language": "es"},
            {"text": "Bienvenue à l'assistant financier RealityCheck", "language": "fr"},
        ]
        
        all_successful = True
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"Voice test {i}: {test_case['language']}")
            
            result = voice_service.synthesize_speech(
                test_case["text"], 
                language=test_case["language"]
            )
            success = result.get("success", False)
            filename = result.get("filename", "N/A")
            
            logger.info(f"Voice synthesis {i} result: {success}")
            logger.info(f"Generated file: {filename}")
            
            if not success:
                all_successful = False
        
        return all_successful
        
    except Exception as e:
        logger.error(f"Voice synthesis workflow failed: {e}")
        return False

async def run_e2e_tests():
    """Run all end-to-end tests"""
    logger.info("🚀 Starting end-to-end tests...")
    
    tests = [
        ("Retirement Planning Workflow", test_retirement_planning_workflow),
        ("Multilingual Workflow", test_multilingual_workflow),
        ("Research Workflow", test_research_workflow),
        ("Voice Synthesis Workflow", test_voice_synthesis_workflow),
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
    logger.info("📊 END-TO-END TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} E2E tests passed")
    
    if passed == total:
        logger.info("🎉 All end-to-end tests passed!")
        logger.info("🚀 Your RealityCheck platform is ready for production!")
    else:
        logger.warning(f"⚠️  {total - passed} E2E tests failed.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_e2e_tests())

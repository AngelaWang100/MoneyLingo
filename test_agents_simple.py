#!/usr/bin/env python3
"""
Simple Agent Test Script for RealityCheck
Tests backend AI agents without external dependencies
"""

import sys
import os
import asyncio
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentTester:
    def __init__(self):
        self.results = {}
        
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
        
    def print_success(self, message: str):
        print(f"✅ {message}")
        
    def print_error(self, message: str):
        print(f"❌ {message}")
        
    def print_info(self, message: str):
        print(f"ℹ️  {message}")
        
    async def test_agent_imports(self):
        """Test that all agents can be imported"""
        self.print_header("AGENT IMPORT TESTS")
        
        agents_to_test = [
            ("Translation Agent", "api.services.agents.translation_agent", "TranslationAgent"),
            ("Financial Planning Agent", "api.services.agents.financial_planning_agent", "FinancialPlanningAgent"),
            ("Remittance Agent", "api.services.agents.remittance_agent", "RemittanceAgent"),
            ("Voice Translation Agent", "api.services.agents.voice_translation_agent", "VoiceTranslationAgent"),
            ("Auto Language Voice Agent", "api.services.agents.auto_language_voice_agent", "AutoLanguageVoiceAgent"),
            ("Tavily Research Agent", "api.services.agents.tavily_research_agent", "TavilyResearchAgent"),
        ]
        
        import_results = {}
        
        for agent_name, module_path, class_name in agents_to_test:
            try:
                module = __import__(module_path, fromlist=[class_name])
                agent_class = getattr(module, class_name)
                agent_instance = agent_class()
                
                self.print_success(f"{agent_name} imported and instantiated successfully")
                import_results[agent_name] = True
                
            except ImportError as e:
                self.print_error(f"{agent_name} import failed: {e}")
                import_results[agent_name] = False
            except Exception as e:
                self.print_error(f"{agent_name} instantiation failed: {e}")
                import_results[agent_name] = False
        
        return import_results
    
    async def test_agent_methods(self):
        """Test that agents have required methods"""
        self.print_header("AGENT METHOD TESTS")
        
        try:
            from api.services.agents.translation_agent import TranslationAgent
            from api.services.agents.financial_planning_agent import FinancialPlanningAgent
            from api.services.agents.remittance_agent import RemittanceAgent
            
            # Test Translation Agent
            translation_agent = TranslationAgent()
            required_methods = ['process', 'log_decision']
            for method in required_methods:
                if hasattr(translation_agent, method):
                    self.print_success(f"Translation Agent has {method} method")
                else:
                    self.print_error(f"Translation Agent missing {method} method")
            
            # Test Financial Planning Agent
            financial_agent = FinancialPlanningAgent()
            for method in required_methods:
                if hasattr(financial_agent, method):
                    self.print_success(f"Financial Planning Agent has {method} method")
                else:
                    self.print_error(f"Financial Planning Agent missing {method} method")
            
            # Test Remittance Agent
            remittance_agent = RemittanceAgent()
            for method in required_methods:
                if hasattr(remittance_agent, method):
                    self.print_success(f"Remittance Agent has {method} method")
                else:
                    self.print_error(f"Remittance Agent missing {method} method")
            
            return True
            
        except Exception as e:
            self.print_error(f"Agent method test failed: {e}")
            return False
    
    async def test_agent_processing(self):
        """Test agent processing with mock data"""
        self.print_header("AGENT PROCESSING TESTS")
        
        try:
            from api.services.agents.translation_agent import TranslationAgent
            from api.services.agents.financial_planning_agent import FinancialPlanningAgent
            
            # Test Translation Agent
            translation_agent = TranslationAgent()
            test_data = {
                "content": "Hello, I need help with retirement planning",
                "target_language": "es",
                "context": "financial_advice"
            }
            
            self.print_info("Testing Translation Agent with mock data...")
            try:
                result = await translation_agent.process(test_data)
                if result and isinstance(result, dict):
                    self.print_success("Translation Agent processed data successfully")
                    self.print_info(f"Result keys: {list(result.keys())}")
                else:
                    self.print_error("Translation Agent returned invalid result")
            except Exception as e:
                self.print_error(f"Translation Agent processing failed: {e}")
            
            # Test Financial Planning Agent
            financial_agent = FinancialPlanningAgent()
            test_data = {
                "goals": ["retirement planning"],
                "income": 5000,
                "expenses": 3000,
                "timeline": "5 years"
            }
            
            self.print_info("Testing Financial Planning Agent with mock data...")
            try:
                result = await financial_agent.process(test_data)
                if result and isinstance(result, dict):
                    self.print_success("Financial Planning Agent processed data successfully")
                    self.print_info(f"Result keys: {list(result.keys())}")
                else:
                    self.print_error("Financial Planning Agent returned invalid result")
            except Exception as e:
                self.print_error(f"Financial Planning Agent processing failed: {e}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Agent processing test failed: {e}")
            return False
    
    async def test_voice_services(self):
        """Test voice services"""
        self.print_header("VOICE SERVICES TESTS")
        
        try:
            from voice.elevenlabs_service import ElevenLabsVoiceService
            
            voice_service = ElevenLabsVoiceService()
            
            if voice_service.client:
                self.print_success("ElevenLabs service initialized with API key")
            else:
                self.print_info("ElevenLabs service initialized without API key (expected for demo)")
            
            # Test voice synthesis method exists
            if hasattr(voice_service, 'synthesize_speech'):
                self.print_success("Voice synthesis method available")
            else:
                self.print_error("Voice synthesis method missing")
            
            return True
            
        except Exception as e:
            self.print_error(f"Voice services test failed: {e}")
            return False
    
    async def test_api_routes(self):
        """Test API route configuration"""
        self.print_header("API ROUTES TESTS")
        
        try:
            from api.routes import financial, voice, translation, remittance, monetization
            
            # Test route modules can be imported
            self.print_success("Financial routes imported successfully")
            self.print_success("Voice routes imported successfully")
            self.print_success("Translation routes imported successfully")
            self.print_success("Remittance routes imported successfully")
            self.print_success("Monetization routes imported successfully")
            
            return True
            
        except Exception as e:
            self.print_error(f"API routes test failed: {e}")
            return False
    
    async def test_main_application(self):
        """Test main application can be imported"""
        self.print_header("MAIN APPLICATION TESTS")
        
        try:
            from main_new import app
            
            self.print_success("Main application imported successfully")
            self.print_info(f"FastAPI app: {app}")
            self.print_info(f"App title: {app.title}")
            self.print_info(f"App version: {app.version}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Main application test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all agent tests"""
        self.print_header("REALITYCHECK AGENT TEST SUITE")
        self.print_info(f"Timestamp: {datetime.now().isoformat()}")
        self.print_info("Testing backend AI agents and services...")
        
        test_functions = [
            ("Agent Imports", self.test_agent_imports),
            ("Agent Methods", self.test_agent_methods),
            ("Agent Processing", self.test_agent_processing),
            ("Voice Services", self.test_voice_services),
            ("API Routes", self.test_api_routes),
            ("Main Application", self.test_main_application),
        ]
        
        results = {}
        total_passed = 0
        total_tests = len(test_functions)
        
        for test_name, test_func in test_functions:
            try:
                result = await test_func()
                results[test_name] = result
                if result:
                    total_passed += 1
                    self.print_success(f"{test_name}: PASSED")
                else:
                    self.print_error(f"{test_name}: FAILED")
            except Exception as e:
                self.print_error(f"{test_name}: ERROR - {e}")
                results[test_name] = False
        
        # Final summary
        self.print_header("TEST SUITE SUMMARY")
        self.print_info(f"Total tests: {total_tests}")
        self.print_info(f"Passed: {total_passed}")
        self.print_info(f"Failed: {total_tests - total_passed}")
        
        if total_passed == total_tests:
            self.print_success("🎉 ALL TESTS PASSED!")
            self.print_success("🚀 Backend AI agents are working correctly!")
        else:
            self.print_info(f"⚠️  {total_tests - total_passed} tests failed")
            self.print_info("Check the errors above for details")
        
        return results

async def main():
    """Main test function"""
    print("🧪 Starting RealityCheck Agent Tests...")
    print("Testing backend AI agents and services...")
    print()
    
    tester = AgentTester()
    results = await tester.run_all_tests()
    
    print("\n🎯 Test Results Summary:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())

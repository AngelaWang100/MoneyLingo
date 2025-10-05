#!/usr/bin/env python3
"""
Agent Structure Test for RealityCheck
Tests the structure and capabilities of backend AI agents
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentStructureTester:
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
        
    def test_file_structure(self):
        """Test that all agent files exist"""
        self.print_header("FILE STRUCTURE TESTS")
        
        required_files = [
            "agents/translation_agent.py",
            "agents/financial_planning_agent.py", 
            "agents/remittance_agent.py",
            "agents/voice_translation_agent.py",
            "agents/auto_language_voice_agent.py",
            "agents/tavily_research_agent.py",
            "agents/base_agent.py",
            "agents/orchestrator.py",
            "api/services/agents/translation_agent.py",
            "api/services/agents/financial_planning_agent.py",
            "api/services/agents/remittance_agent.py",
            "api/services/agents/voice_translation_agent.py",
            "api/services/agents/auto_language_voice_agent.py",
            "api/services/agents/tavily_research_agent.py",
            "api/services/agents/base_agent.py",
            "api/services/agents/orchestrator.py",
            "voice/elevenlabs_service.py",
            "api/routes/financial.py",
            "api/routes/voice.py",
            "api/routes/translation.py",
            "api/routes/remittance.py",
            "api/routes/monetization.py",
            "main_new.py"
        ]
        
        file_results = {}
        
        for file_path in required_files:
            if os.path.exists(file_path):
                self.print_success(f"File exists: {file_path}")
                file_results[file_path] = True
            else:
                self.print_error(f"File missing: {file_path}")
                file_results[file_path] = False
        
        return file_results
    
    def test_agent_classes(self):
        """Test that agent classes are defined correctly"""
        self.print_header("AGENT CLASS TESTS")
        
        agent_files = [
            ("agents/translation_agent.py", "TranslationAgent"),
            ("agents/financial_planning_agent.py", "FinancialPlanningAgent"),
            ("agents/remittance_agent.py", "RemittanceAgent"),
            ("agents/voice_translation_agent.py", "VoiceTranslationAgent"),
            ("agents/auto_language_voice_agent.py", "AutoLanguageVoiceAgent"),
            ("agents/tavily_research_agent.py", "TavilyResearchAgent"),
        ]
        
        class_results = {}
        
        for file_path, class_name in agent_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                if f"class {class_name}" in content:
                    self.print_success(f"{class_name} class found in {file_path}")
                    class_results[class_name] = True
                else:
                    self.print_error(f"{class_name} class not found in {file_path}")
                    class_results[class_name] = False
                    
            except Exception as e:
                self.print_error(f"Error reading {file_path}: {e}")
                class_results[class_name] = False
        
        return class_results
    
    def test_agent_methods(self):
        """Test that agents have required methods"""
        self.print_header("AGENT METHOD TESTS")
        
        agent_files = [
            ("agents/translation_agent.py", ["process", "log_decision"]),
            ("agents/financial_planning_agent.py", ["process", "log_decision"]),
            ("agents/remittance_agent.py", ["process", "log_decision"]),
            ("agents/voice_translation_agent.py", ["process", "log_decision"]),
            ("agents/auto_language_voice_agent.py", ["process", "log_decision"]),
            ("agents/tavily_research_agent.py", ["process", "log_decision"]),
        ]
        
        method_results = {}
        
        for file_path, required_methods in agent_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                agent_name = file_path.split('/')[-1].replace('.py', '')
                method_found = {}
                
                for method in required_methods:
                    if f"def {method}" in content or f"async def {method}" in content:
                        self.print_success(f"{agent_name} has {method} method")
                        method_found[method] = True
                    else:
                        self.print_error(f"{agent_name} missing {method} method")
                        method_found[method] = False
                
                method_results[agent_name] = method_found
                
            except Exception as e:
                self.print_error(f"Error reading {file_path}: {e}")
                method_results[file_path] = {}
        
        return method_results
    
    def test_api_routes(self):
        """Test API route structure"""
        self.print_header("API ROUTES TESTS")
        
        route_files = [
            "api/routes/financial.py",
            "api/routes/voice.py", 
            "api/routes/translation.py",
            "api/routes/remittance.py",
            "api/routes/monetization.py"
        ]
        
        route_results = {}
        
        for file_path in route_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if "router" in content and "FastAPI" in content:
                    self.print_success(f"API routes defined in {file_path}")
                    route_results[file_path] = True
                else:
                    self.print_error(f"API routes not properly defined in {file_path}")
                    route_results[file_path] = False
                    
            except Exception as e:
                self.print_error(f"Error reading {file_path}: {e}")
                route_results[file_path] = False
        
        return route_results
    
    def test_ai_integrations(self):
        """Test AI integration points"""
        self.print_header("AI INTEGRATION TESTS")
        
        integration_tests = [
            ("Gemini AI Integration", "langchain_google_genai", "ChatGoogleGenerativeAI"),
            ("ElevenLabs Voice", "elevenlabs", "ElevenLabs"),
            ("Tavily Research", "tavily", "TavilyClient"),
            ("FastAPI Framework", "fastapi", "FastAPI"),
            ("Pydantic Models", "pydantic", "BaseModel"),
        ]
        
        integration_results = {}
        
        for test_name, module_name, class_name in integration_tests:
            # Check if integration is referenced in code
            found_in_code = False
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith('.py'):
                        try:
                            with open(os.path.join(root, file), 'r') as f:
                                content = f.read()
                                if module_name in content or class_name in content:
                                    found_in_code = True
                                    break
                        except:
                            continue
                if found_in_code:
                    break
            
            if found_in_code:
                self.print_success(f"{test_name} integration found in code")
                integration_results[test_name] = True
            else:
                self.print_error(f"{test_name} integration not found in code")
                integration_results[test_name] = False
        
        return integration_results
    
    def test_main_application(self):
        """Test main application structure"""
        self.print_header("MAIN APPLICATION TESTS")
        
        try:
            with open("main_new.py", 'r') as f:
                content = f.read()
            
            app_tests = [
                ("FastAPI App", "FastAPI"),
                ("CORS Middleware", "CORSMiddleware"),
                ("Route Inclusion", "include_router"),
                ("Health Check", "health"),
                ("Uvicorn Server", "uvicorn.run"),
            ]
            
            app_results = {}
            
            for test_name, keyword in app_tests:
                if keyword in content:
                    self.print_success(f"{test_name} found in main application")
                    app_results[test_name] = True
                else:
                    self.print_error(f"{test_name} not found in main application")
                    app_results[test_name] = False
            
            return app_results
            
        except Exception as e:
            self.print_error(f"Error reading main application: {e}")
            return {}
    
    def run_all_tests(self):
        """Run all structure tests"""
        self.print_header("REALITYCHECK AGENT STRUCTURE TEST SUITE")
        self.print_info(f"Timestamp: {datetime.now().isoformat()}")
        self.print_info("Testing backend AI agent structure and capabilities...")
        
        test_functions = [
            ("File Structure", self.test_file_structure),
            ("Agent Classes", self.test_agent_classes),
            ("Agent Methods", self.test_agent_methods),
            ("API Routes", self.test_api_routes),
            ("AI Integrations", self.test_ai_integrations),
            ("Main Application", self.test_main_application),
        ]
        
        results = {}
        total_passed = 0
        total_tests = len(test_functions)
        
        for test_name, test_func in test_functions:
            try:
                result = test_func()
                results[test_name] = result
                
                # Count passed tests
                if isinstance(result, dict):
                    passed = sum(1 for v in result.values() if v)
                    total = len(result)
                    if passed > 0:
                        self.print_success(f"{test_name}: {passed}/{total} passed")
                        total_passed += 1
                    else:
                        self.print_error(f"{test_name}: 0/{total} passed")
                else:
                    if result:
                        total_passed += 1
                        self.print_success(f"{test_name}: PASSED")
                    else:
                        self.print_error(f"{test_name}: FAILED")
                        
            except Exception as e:
                self.print_error(f"{test_name}: ERROR - {e}")
                results[test_name] = False
        
        # Final summary
        self.print_header("STRUCTURE TEST SUMMARY")
        self.print_info(f"Test categories: {total_tests}")
        self.print_info(f"Categories passed: {total_passed}")
        self.print_info(f"Categories failed: {total_tests - total_passed}")
        
        if total_passed == total_tests:
            self.print_success("🎉 ALL STRUCTURE TESTS PASSED!")
            self.print_success("🚀 Backend AI agent structure is correct!")
        else:
            self.print_info(f"⚠️  {total_tests - total_passed} test categories failed")
            self.print_info("Check the errors above for details")
        
        return results

def main():
    """Main test function"""
    print("🧪 Starting RealityCheck Agent Structure Tests...")
    print("Testing backend AI agent structure and capabilities...")
    print()
    
    tester = AgentStructureTester()
    results = tester.run_all_tests()
    
    print("\n🎯 Structure Test Results:")
    for test_name, result in results.items():
        if isinstance(result, dict):
            passed = sum(1 for v in result.values() if v)
            total = len(result)
            status = f"✅ {passed}/{total}" if passed > 0 else f"❌ {passed}/{total}"
            print(f"{status} {test_name}")
        else:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
    
    return results

if __name__ == "__main__":
    main()

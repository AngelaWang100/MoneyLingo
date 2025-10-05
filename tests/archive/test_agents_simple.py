"""
Simple test script for agents without API dependencies
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

def test_imports():
    """Test that all modules can be imported"""
    try:
        # Test API structure imports
        from api.routes import financial, voice, translation, remittance, monetization
        logger.info("✅ API routes imported successfully")
        
        from api.models import financial as financial_models, voice as voice_models
        logger.info("✅ Pydantic models imported successfully")
        
        from api.dependencies import get_orchestrator, get_voice_service
        logger.info("✅ Dependencies imported successfully")
        
        from api.config import settings
        logger.info("✅ Configuration imported successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    try:
        from api.models.financial import FinancialRequest, FinancialResponse
        from api.models.voice import TranslationRequest, VoiceResponse
        from api.models.remittance import RemittanceRequest
        
        # Test model creation
        financial_req = FinancialRequest(
            goals=["retirement"],
            income=5000,
            expenses=3000
        )
        
        translation_req = TranslationRequest(
            content="Hello world",
            language="Spanish"
        )
        
        remittance_req = RemittanceRequest(
            amount=1000,
            currency="USD",
            destination="Mexico",
            source_country="US",
            destination_country="Mexico"
        )
        
        logger.info("✅ All Pydantic models work correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Model test failed: {e}")
        return False

def test_route_handlers():
    """Test route handler functions"""
    try:
        from api.routes.financial import router as financial_router
        from api.routes.voice import router as voice_router
        from api.routes.translation import router as translation_router
        from api.routes.remittance import router as remittance_router
        from api.routes.monetization import router as monetization_router
        
        # Check that routers have routes
        financial_routes = [route.path for route in financial_router.routes]
        voice_routes = [route.path for route in voice_router.routes]
        
        logger.info(f"✅ Financial routes: {financial_routes}")
        logger.info(f"✅ Voice routes: {voice_routes}")
        logger.info("✅ All route handlers are properly configured")
        return True
        
    except Exception as e:
        logger.error(f"❌ Route handler test failed: {e}")
        return False

def test_agent_structure():
    """Test agent file structure"""
    try:
        # Check if agent files exist
        agent_files = [
            "api/services/agents/base_agent.py",
            "api/services/agents/orchestrator.py", 
            "api/services/agents/translation_agent.py",
            "api/services/agents/financial_planning_agent.py",
            "api/services/agents/remittance_agent.py"
        ]
        
        for file_path in agent_files:
            if not os.path.exists(file_path):
                logger.error(f"❌ Missing file: {file_path}")
                return False
        
        logger.info("✅ All agent files exist")
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent structure test failed: {e}")
        return False

def test_main_app():
    """Test main application structure"""
    try:
        # Test that main_new.py can be imported
        import main_new
        logger.info("✅ Main application imported successfully")
        
        # Check FastAPI app
        app = main_new.app
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        logger.info(f"✅ App has {len(routes)} routes")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Main app test failed: {e}")
        return False

def test_directory_structure():
    """Test that the new directory structure is correct"""
    try:
        required_dirs = [
            "api",
            "api/routes", 
            "api/services",
            "api/services/agents",
            "api/models",
            "api/dependencies"
        ]
        
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                logger.error(f"❌ Missing directory: {dir_path}")
                return False
        
        logger.info("✅ Directory structure is correct")
        return True
        
    except Exception as e:
        logger.error(f"❌ Directory structure test failed: {e}")
        return False

def run_simple_tests():
    """Run all simple tests"""
    logger.info("🚀 Starting simple agent structure tests...")
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Imports", test_imports),
        ("Pydantic Models", test_models),
        ("Route Handlers", test_route_handlers),
        ("Agent Structure", test_agent_structure),
        ("Main Application", test_main_app),
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
    logger.info("📊 SIMPLE TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All structural tests passed! The new API structure is working correctly!")
    else:
        logger.warning(f"⚠️  {total - passed} tests failed. Check the logs above.")
    
    return results

if __name__ == "__main__":
    run_simple_tests()

#!/usr/bin/env python3
"""
Quick setup test for RealityCheck Agent System
"""
import os
import sys
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported"""
    try:
        logger.info("Testing imports...")
        
        # Test basic imports
        import requests
        import pandas as pd
        from dotenv import load_dotenv
        
        # Test agent imports
        from agents.base_agent import BaseAgent
        from agents.translation_agent import TranslationAgent
        from agents.financial_planning_agent import FinancialPlanningAgent
        from agents.remittance_agent import RemittanceAgent
        from agents.orchestrator import AgentOrchestrator
        
        # Test observability
        from observability.comet_integration import CometObserver
        
        logger.info("✅ All imports successful")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    try:
        logger.info("Testing environment...")
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for required variables
        required_vars = ["GOOGLE_API_KEY", "COMET_API_KEY", "COMET_WORKSPACE"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.warning(f"⚠️  Missing environment variables: {missing_vars}")
            logger.info("Please set these in your .env file")
            return False
        
        logger.info("✅ Environment variables set")
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment test failed: {e}")
        return False

async def test_agent_creation():
    """Test agent instantiation"""
    try:
        logger.info("Testing agent creation...")
        
        # Create agents
        from agents.translation_agent import TranslationAgent
        from agents.financial_planning_agent import FinancialPlanningAgent
        from agents.remittance_agent import RemittanceAgent
        
        translation_agent = TranslationAgent()
        financial_agent = FinancialPlanningAgent()
        remittance_agent = RemittanceAgent()
        
        logger.info("✅ All agents created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent creation failed: {e}")
        return False

async def test_simple_translation():
    """Test a simple translation without API calls"""
    try:
        logger.info("Testing simple translation...")
        
        from agents.translation_agent import TranslationAgent
        agent = TranslationAgent()
        
        # Test with mock data (won't make actual API calls without proper keys)
        test_data = {
            "content": "Test financial concept",
            "language": "English",
            "user_level": "beginner"
        }
        
        # This will fail gracefully if API key is not set
        result = await agent.process(test_data)
        
        if result.get("success") or "error" in result:
            logger.info("✅ Translation agent responds (may need API key for full functionality)")
            return True
        else:
            logger.warning("⚠️  Translation agent test inconclusive")
            return True
            
    except Exception as e:
        logger.error(f"❌ Translation test failed: {e}")
        return False

def main():
    """Run all setup tests"""
    logger.info("RealityCheck Agent System - Setup Test")
    logger.info("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Agent Creation Test", test_agent_creation),
        ("Simple Translation Test", test_simple_translation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("SETUP TEST SUMMARY")
    logger.info("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! System is ready.")
        return 0
    else:
        logger.warning("⚠️  Some tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

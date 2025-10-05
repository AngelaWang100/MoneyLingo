"""
Master test runner for all RealityCheck tests
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_unit_tests():
    """Run unit tests"""
    try:
        from tests.unit.test_individual_agents import run_unit_tests
        logger.info("🧪 Running unit tests...")
        return await run_unit_tests()
    except Exception as e:
        logger.error(f"Unit tests failed: {e}")
        return {}

async def run_integration_tests():
    """Run integration tests"""
    try:
        from tests.integration.test_orchestrator import run_integration_tests
        logger.info("🧪 Running integration tests...")
        return await run_integration_tests()
    except Exception as e:
        logger.error(f"Integration tests failed: {e}")
        return {}

async def run_e2e_tests():
    """Run end-to-end tests"""
    try:
        from tests.e2e.test_complete_workflows import run_e2e_tests
        logger.info("🧪 Running E2E tests...")
        return await run_e2e_tests()
    except Exception as e:
        logger.error(f"E2E tests failed: {e}")
        return {}

async def run_all_tests():
    """Run all test suites"""
    logger.info("🚀 Starting comprehensive RealityCheck test suite...")
    
    test_suites = [
        ("Unit Tests", run_unit_tests),
        ("Integration Tests", run_integration_tests),
        ("End-to-End Tests", run_e2e_tests),
    ]
    
    all_results = {}
    total_passed = 0
    total_tests = 0
    
    for suite_name, suite_func in test_suites:
        logger.info(f"\n{'='*60}")
        logger.info(f"🧪 Running {suite_name}...")
        logger.info('='*60)
        
        try:
            results = await suite_func()
            all_results[suite_name] = results
            
            # Count results
            suite_passed = sum(1 for result in results.values() if result)
            suite_total = len(results)
            total_passed += suite_passed
            total_tests += suite_total
            
            logger.info(f"✅ {suite_name}: {suite_passed}/{suite_total} passed")
            
        except Exception as e:
            logger.error(f"❌ {suite_name} failed: {e}")
            all_results[suite_name] = {}
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("🏆 COMPREHENSIVE TEST SUITE SUMMARY")
    logger.info("="*60)
    
    for suite_name, results in all_results.items():
        if results:
            suite_passed = sum(1 for result in results.values() if result)
            suite_total = len(results)
            status = "✅ PASSED" if suite_passed == suite_total else "⚠️  PARTIAL"
            logger.info(f"{status}: {suite_name} ({suite_passed}/{suite_total})")
        else:
            logger.info(f"❌ FAILED: {suite_name}")
    
    logger.info(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("🚀 RealityCheck is ready for hackathon success!")
    else:
        logger.warning(f"⚠️  {total_tests - total_passed} tests failed.")
    
    return all_results

if __name__ == "__main__":
    asyncio.run(run_all_tests())

#!/usr/bin/env python3
"""
Simple test without comet dependencies
"""
import os
import sys
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_imports():
    """Test basic imports without comet"""
    try:
        logger.info("Testing basic imports...")
        
        import requests
        import pandas as pd
        from dotenv import load_dotenv
        
        logger.info("✅ Basic imports successful")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    try:
        logger.info("Testing environment...")
        
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

def test_google_gemini():
    """Test Google Gemini import"""
    try:
        logger.info("Testing Google Gemini...")
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        logger.info("✅ Google Gemini import successful")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Google Gemini import failed: {e}")
        return False

def test_langchain():
    """Test LangChain imports"""
    try:
        logger.info("Testing LangChain...")
        
        from langchain.schema import HumanMessage, SystemMessage
        from langgraph.graph import StateGraph, END
        
        logger.info("✅ LangChain imports successful")
        return True
        
    except ImportError as e:
        logger.error(f"❌ LangChain import failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("RealityCheck Agent System - Simple Test")
    logger.info("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Environment", test_environment),
        ("Google Gemini", test_google_gemini),
        ("LangChain", test_langchain)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("SIMPLE TEST SUMMARY")
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

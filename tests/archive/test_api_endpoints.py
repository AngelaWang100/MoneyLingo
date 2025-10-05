"""
Test API endpoints functionality
"""
import requests
import json
import time
import subprocess
import signal
import os
from typing import Dict, Any

def start_server():
    """Start the FastAPI server"""
    try:
        # Start server in background
        process = subprocess.Popen(
            ["python3", "main_new.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_financial_endpoint():
    """Test financial planning endpoint"""
    try:
        payload = {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        }
        
        response = requests.post(
            "http://localhost:8001/api/v1/financial/plan",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Financial planning endpoint working")
            return True
        else:
            print(f"❌ Financial planning failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Financial planning error: {e}")
        return False

def test_voice_endpoint():
    """Test voice synthesis endpoint"""
    try:
        payload = {
            "text": "Hello, this is a test",
            "language": "en"
        }
        
        response = requests.post(
            "http://localhost:8001/api/v1/voice/synthesize",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Voice synthesis endpoint working")
            return True
        else:
            print(f"❌ Voice synthesis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Voice synthesis error: {e}")
        return False

def test_translation_endpoint():
    """Test translation endpoint"""
    try:
        payload = {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        response = requests.post(
            "http://localhost:8001/api/v1/translate/",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Translation endpoint working")
            return True
        else:
            print(f"❌ Translation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return False

def test_monetization_endpoint():
    """Test monetization endpoint"""
    try:
        response = requests.get(
            "http://localhost:8001/api/v1/monetization/pricing",
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Monetization endpoint working")
            return True
        else:
            print(f"❌ Monetization failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Monetization error: {e}")
        return False

def test_api_documentation():
    """Test API documentation endpoints"""
    try:
        # Test Swagger UI
        response = requests.get("http://localhost:8001/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Swagger UI accessible")
            return True
        else:
            print(f"❌ Swagger UI failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API documentation error: {e}")
        return False

def run_endpoint_tests():
    """Run all endpoint tests"""
    print("🚀 Starting API endpoint tests...")
    
    # Start server
    print("\n🔧 Starting FastAPI server...")
    server_process = start_server()
    
    if not server_process:
        print("❌ Could not start server")
        return False
    
    try:
        # Wait a bit more for server to fully start
        time.sleep(2)
        
        tests = [
            ("Health Check", test_health_endpoint),
            ("Financial Planning", test_financial_endpoint),
            ("Voice Synthesis", test_voice_endpoint),
            ("Translation", test_translation_endpoint),
            ("Monetization", test_monetization_endpoint),
            ("API Documentation", test_api_documentation),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testing {test_name}...")
            try:
                result = test_func()
                results[test_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"{status}: {test_name}")
            except Exception as e:
                print(f"❌ FAILED: {test_name} - {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "="*50)
        print("📊 ENDPOINT TEST SUMMARY")
        print("="*50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
        
        print(f"\n🎯 Overall: {passed}/{total} endpoint tests passed")
        
        if passed == total:
            print("🎉 All API endpoints are working correctly!")
        else:
            print(f"⚠️  {total - passed} endpoint tests failed.")
        
        return results
        
    finally:
        # Clean up server process
        if server_process:
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
                print("\n🔧 Server stopped")
            except:
                server_process.kill()
                print("\n🔧 Server force stopped")

if __name__ == "__main__":
    run_endpoint_tests()

#!/usr/bin/env python3
"""
Backend API Demo Script for RealityCheck
Demonstrates all working backend endpoints with live API calls
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any

class BackendDemo:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
        
    def print_success(self, message: str):
        print(f"✅ {message}")
        
    def print_error(self, message: str):
        print(f"❌ {message}")
        
    def print_info(self, message: str):
        print(f"ℹ️  {message}")
        
    def test_health_check(self):
        """Test basic health check"""
        self.print_header("HEALTH CHECK")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Backend is healthy: {data['status']}")
                self.print_info(f"Services: {json.dumps(data.get('services', {}), indent=2)}")
                return True
            else:
                self.print_error(f"Health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Health check failed: {e}")
            return False
    
    def test_financial_planning(self):
        """Test financial planning endpoint"""
        self.print_header("FINANCIAL PLANNING API")
        
        # Test data
        financial_data = {
            "goals": ["Retirement savings", "Emergency fund", "Home purchase"],
            "income": 7500,
            "expenses": 4500,
            "timeline": "5 years",
            "risk_tolerance": "moderate"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/financial/plan",
                json=financial_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Financial plan generated successfully!")
                self.print_info(f"Plan ID: {data.get('plan_id', 'N/A')}")
                self.print_info(f"Recommendations: {data.get('recommendations', 'N/A')[:100]}...")
                return True
            else:
                self.print_error(f"Financial planning failed: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Financial planning failed: {e}")
            return False
    
    def test_voice_synthesis(self):
        """Test voice synthesis endpoint"""
        self.print_header("VOICE SYNTHESIS API")
        
        voice_data = {
            "text": "Welcome to MoneyLingo! Your AI financial assistant is ready to help you plan for the future.",
            "language": "en",
            "voice_id": "default"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/voice/synthesize",
                json=voice_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Voice synthesis completed!")
                self.print_info(f"Audio file: {data.get('filepath', 'N/A')}")
                self.print_info(f"Duration: {data.get('duration', 'N/A')} seconds")
                return True
            else:
                self.print_error(f"Voice synthesis failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Voice synthesis failed: {e}")
            return False
    
    def test_translation(self):
        """Test translation endpoint"""
        self.print_header("TRANSLATION API")
        
        translation_data = {
            "content": "Your monthly budget should include 50% for needs, 30% for wants, and 20% for savings.",
            "target_language": "es",
            "context": "financial_advice"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/translate/translate",
                json=translation_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Translation completed!")
                self.print_info(f"Original: {translation_data['content']}")
                self.print_info(f"Translated: {data.get('translated_content', 'N/A')}")
                return True
            else:
                self.print_error(f"Translation failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Translation failed: {e}")
            return False
    
    def test_remittance_analysis(self):
        """Test remittance analysis endpoint"""
        self.print_header("REMITTANCE ANALYSIS API")
        
        remittance_data = {
            "amount": 1000,
            "from_country": "US",
            "to_country": "Mexico",
            "currency": "USD"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/remittance/analyze",
                json=remittance_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Remittance analysis completed!")
                self.print_info(f"Best method: {data.get('best_method', 'N/A')}")
                self.print_info(f"Estimated fees: {data.get('estimated_fees', 'N/A')}")
                return True
            else:
                self.print_error(f"Remittance analysis failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Remittance analysis failed: {e}")
            return False
    
    def test_monetization(self):
        """Test monetization endpoint"""
        self.print_header("MONETIZATION API")
        
        monetization_data = {
            "user_id": "demo_user_123",
            "service_type": "financial_planning",
            "tier": "premium"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/monetization/calculate",
                json=monetization_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Monetization calculation completed!")
                self.print_info(f"Price: ${data.get('price', 'N/A')}")
                self.print_info(f"Features: {data.get('features', 'N/A')}")
                return True
            else:
                self.print_error(f"Monetization failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Monetization failed: {e}")
            return False
    
    def run_full_demo(self):
        """Run complete backend demo"""
        self.print_header("REALITYCHECK BACKEND DEMO")
        self.print_info(f"Testing backend at: {self.base_url}")
        self.print_info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Test all endpoints
        tests = [
            ("Health Check", self.test_health_check),
            ("Financial Planning", self.test_financial_planning),
            ("Voice Synthesis", self.test_voice_synthesis),
            ("Translation", self.test_translation),
            ("Remittance Analysis", self.test_remittance_analysis),
            ("Monetization", self.test_monetization)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.print_error(f"{test_name} failed with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        self.print_header("DEMO SUMMARY")
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            self.print_success("All backend APIs are working perfectly!")
        else:
            self.print_info(f"{total - passed} tests failed - check backend logs")
        
        return passed == total

def main():
    """Main demo function"""
    print("🚀 Starting RealityCheck Backend Demo...")
    print("Make sure your backend is running on port 8001")
    print("Run: python main_new.py")
    print()
    
    demo = BackendDemo()
    success = demo.run_full_demo()
    
    if success:
        print("\n🎉 Backend demo completed successfully!")
        print("Your backend APIs are fully functional and ready for integration!")
    else:
        print("\n⚠️  Some backend tests failed. Check your backend setup.")
    
    return success

if __name__ == "__main__":
    main()

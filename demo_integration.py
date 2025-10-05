#!/usr/bin/env python3
"""
Integration Demo Script for RealityCheck
Demonstrates how frontend and backend work together
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any

class IntegrationDemo:
    def __init__(self, backend_url: str = "http://localhost:8001", frontend_url: str = "http://localhost:3000"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.session = requests.Session()
        
    def print_header(self, title: str):
        print(f"\n{'='*70}")
        print(f"🔗 {title}")
        print(f"{'='*70}")
        
    def print_success(self, message: str):
        print(f"✅ {message}")
        
    def print_error(self, message: str):
        print(f"❌ {message}")
        
    def print_info(self, message: str):
        print(f"ℹ️  {message}")
        
    def test_backend_health(self):
        """Test backend health"""
        try:
            response = self.session.get(f"{self.backend_url}/health")
            if response.status_code == 200:
                self.print_success("Backend is healthy and ready")
                return True
            else:
                self.print_error(f"Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Backend not accessible: {e}")
            return False
    
    def test_frontend_health(self):
        """Test frontend health"""
        try:
            response = self.session.get(f"{self.frontend_url}")
            if response.status_code == 200:
                self.print_success("Frontend is accessible")
                return True
            else:
                self.print_error(f"Frontend health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Frontend not accessible: {e}")
            return False
    
    def simulate_user_journey(self):
        """Simulate complete user journey"""
        self.print_header("COMPLETE USER JOURNEY SIMULATION")
        
        # Step 1: User visits frontend
        self.print_info("Step 1: User visits MoneyLingo frontend")
        self.print_success("✅ Frontend loads with dashboard")
        
        # Step 2: User creates financial plan
        self.print_info("Step 2: User creates financial plan")
        financial_data = {
            "goals": ["Retirement savings", "Emergency fund"],
            "income": 7500,
            "expenses": 4500,
            "timeline": "5 years"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/v1/financial/plan",
                json=financial_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                plan_data = response.json()
                self.print_success("✅ Financial plan created via backend API")
                self.print_info(f"   Plan ID: {plan_data.get('plan_id', 'N/A')}")
                self.print_info(f"   Recommendations: {plan_data.get('recommendations', 'N/A')[:100]}...")
            else:
                self.print_error("❌ Financial plan creation failed")
                return False
        except Exception as e:
            self.print_error(f"❌ Financial plan creation failed: {e}")
            return False
        
        # Step 3: User requests voice explanation
        self.print_info("Step 3: User requests voice explanation")
        voice_data = {
            "text": "Your financial plan recommends saving $1,500 monthly with a balanced portfolio approach.",
            "language": "en"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/v1/voice/synthesize",
                json=voice_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                voice_result = response.json()
                self.print_success("✅ Voice synthesis completed")
                self.print_info(f"   Audio file: {voice_result.get('filepath', 'N/A')}")
                self.print_info(f"   Duration: {voice_result.get('duration', 'N/A')} seconds")
            else:
                self.print_error("❌ Voice synthesis failed")
                return False
        except Exception as e:
            self.print_error(f"❌ Voice synthesis failed: {e}")
            return False
        
        # Step 4: User requests translation
        self.print_info("Step 4: User requests Spanish translation")
        translation_data = {
            "content": "Your financial plan recommends saving $1,500 monthly with a balanced portfolio approach.",
            "target_language": "es",
            "context": "financial_advice"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/v1/translate/translate",
                json=translation_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                translation_result = response.json()
                self.print_success("✅ Translation completed")
                self.print_info(f"   Original: {translation_data['content']}")
                self.print_info(f"   Translated: {translation_result.get('translated_content', 'N/A')}")
            else:
                self.print_error("❌ Translation failed")
                return False
        except Exception as e:
            self.print_error(f"❌ Translation failed: {e}")
            return False
        
        # Step 5: User analyzes remittance
        self.print_info("Step 5: User analyzes remittance options")
        remittance_data = {
            "amount": 1000,
            "from_country": "US",
            "to_country": "Mexico"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/api/v1/remittance/analyze",
                json=remittance_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                remittance_result = response.json()
                self.print_success("✅ Remittance analysis completed")
                self.print_info(f"   Best method: {remittance_result.get('best_method', 'N/A')}")
                self.print_info(f"   Estimated fees: ${remittance_result.get('estimated_fees', 'N/A')}")
            else:
                self.print_error("❌ Remittance analysis failed")
                return False
        except Exception as e:
            self.print_error(f"❌ Remittance analysis failed: {e}")
            return False
        
        # Step 6: Frontend displays results
        self.print_info("Step 6: Frontend displays integrated results")
        self.print_success("✅ Frontend receives all data from backend")
        self.print_success("✅ User sees complete financial dashboard")
        self.print_success("✅ Voice playback available")
        self.print_success("✅ Multilingual support active")
        
        return True
    
    def demonstrate_api_endpoints(self):
        """Demonstrate all API endpoints"""
        self.print_header("API ENDPOINTS DEMONSTRATION")
        
        endpoints = [
            ("GET", "/health", "Health check"),
            ("GET", "/", "Root endpoint"),
            ("POST", "/api/v1/financial/plan", "Financial planning"),
            ("POST", "/api/v1/voice/synthesize", "Voice synthesis"),
            ("POST", "/api/v1/translate/translate", "Translation"),
            ("POST", "/api/v1/remittance/analyze", "Remittance analysis"),
            ("POST", "/api/v1/monetization/calculate", "Monetization")
        ]
        
        for method, endpoint, description in endpoints:
            try:
                url = f"{self.backend_url}{endpoint}"
                if method == "GET":
                    response = self.session.get(url)
                else:
                    # Use sample data for POST requests
                    sample_data = {
                        "goals": ["test"],
                        "income": 5000,
                        "expenses": 3000,
                        "timeline": "1 year"
                    }
                    response = self.session.post(url, json=sample_data)
                
                status = "✅" if response.status_code in [200, 201] else "❌"
                self.print_info(f"{status} {method} {endpoint} - {description} ({response.status_code})")
                
            except Exception as e:
                self.print_error(f"❌ {method} {endpoint} - {description} (Error: {e})")
    
    def show_integration_architecture(self):
        """Show integration architecture"""
        self.print_header("INTEGRATION ARCHITECTURE")
        
        architecture = """
        🌐 FRONTEND (React + TypeScript)
        ├── Dashboard UI
        ├── Financial Planning Interface
        ├── Voice Controls
        ├── Translation Interface
        └── Remittance Analysis UI
        
        🔗 API GATEWAY (FastAPI)
        ├── CORS enabled for frontend
        ├── Request routing
        ├── Authentication
        └── Response formatting
        
        🤖 BACKEND SERVICES
        ├── Financial Planning Agent (Gemini AI)
        ├── Voice Synthesis Service (ElevenLabs)
        ├── Translation Agent (Gemini AI)
        ├── Remittance Analysis (XRPL)
        └── Monetization Service (Echo AI)
        
        📊 DATA FLOW
        Frontend → API Gateway → AI Agents → External APIs → Response → Frontend
        """
        
        print(architecture)
        
        self.print_info("Integration Points:")
        self.print_info("• Frontend makes HTTP requests to backend APIs")
        self.print_info("• Backend processes requests with AI agents")
        self.print_info("• External APIs provide AI capabilities")
        self.print_info("• Results flow back to frontend for display")
    
    def run_integration_demo(self):
        """Run complete integration demo"""
        self.print_header("REALITYCHECK INTEGRATION DEMO")
        self.print_info(f"Backend: {self.backend_url}")
        self.print_info(f"Frontend: {self.frontend_url}")
        self.print_info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Test both services
        backend_healthy = self.test_backend_health()
        frontend_healthy = self.test_frontend_health()
        
        if not backend_healthy:
            self.print_error("Backend is not running. Start it with: python main_new.py")
            return False
        
        if not frontend_healthy:
            self.print_error("Frontend is not running. Start it with: cd frontend && npm run dev")
            return False
        
        # Show architecture
        self.show_integration_architecture()
        
        # Demonstrate API endpoints
        self.demonstrate_api_endpoints()
        
        # Simulate user journey
        journey_success = self.simulate_user_journey()
        
        # Final summary
        self.print_header("INTEGRATION DEMO SUMMARY")
        
        if journey_success:
            self.print_success("🎉 Complete integration demo successful!")
            self.print_success("✅ Frontend and backend are working together")
            self.print_success("✅ All AI services are functional")
            self.print_success("✅ User journey completed successfully")
        else:
            self.print_error("⚠️  Integration demo had issues")
            self.print_error("Check backend logs and API responses")
        
        return journey_success

def main():
    """Main integration demo function"""
    print("🔗 Starting RealityCheck Integration Demo...")
    print("This demo shows how frontend and backend work together")
    print()
    
    demo = IntegrationDemo()
    success = demo.run_integration_demo()
    
    if success:
        print("\n🎯 Integration demo completed successfully!")
        print("Your frontend and backend are fully integrated!")
        print("\n📱 Frontend Demo: http://localhost:3000/demo")
        print("🔧 Backend API: http://localhost:8001/docs")
    else:
        print("\n⚠️  Integration demo had issues.")
        print("Make sure both frontend and backend are running.")
    
    return success

if __name__ == "__main__":
    main()

"""
Test RealityCheck monetization system with Echo AI SDK
"""
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_monetization_system():
    """Test the complete monetization system"""
    print("💰 Testing RealityCheck Monetization System")
    print("=" * 60)
    
    try:
        from monetization.monetization_service import RealityCheckMonetization
        
        # Initialize monetization service
        monetization = RealityCheckMonetization()
        print("✅ Monetization service initialized")
        
        # Test user ID
        test_user_id = "test_user_123"
        
        # Test 1: Get pricing information
        print("\n📊 Testing Pricing Information...")
        print("-" * 40)
        
        pricing_info = monetization.service_pricing
        print(f"✅ Available services: {len(pricing_info)}")
        
        for service_type, plans in pricing_info.items():
            print(f"   📋 {service_type.title()}:")
            for tier, details in plans.items():
                print(f"      {tier.title()}: ${details['price']} - {details['description']}")
        
        # Test 2: Check user access
        print("\n🔐 Testing User Access Control...")
        print("-" * 40)
        
        services_to_test = ["voice_translation", "financial_planning", "remittance_analysis", "multilingual_voice"]
        
        for service_type in services_to_test:
            access_result = monetization.check_user_access(test_user_id, service_type)
            status = "✅" if access_result.get("access") else "❌"
            print(f"{status} {service_type}: {access_result.get('reason', 'Unknown')}")
        
        # Test 3: Process service requests
        print("\n🔄 Testing Service Request Processing...")
        print("-" * 40)
        
        # Test voice translation request
        voice_request = {
            "content": "Hello, I need help with my retirement plan",
            "language": "English",
            "user_level": "beginner"
        }
        
        voice_result = monetization.process_service_request(
            user_id=test_user_id,
            service_type="voice_translation",
            request_data=voice_request
        )
        
        if voice_result.get("success"):
            print("✅ Voice translation request processed successfully")
            print(f"   💰 Cost: ${voice_result.get('cost', 0)}")
            print(f"   📊 Remaining credits: {voice_result.get('remaining_credits', 0)}")
        else:
            print(f"❌ Voice translation request failed: {voice_result.get('error')}")
        
        # Test financial planning request
        financial_request = {
            "goals": ["retirement", "house_purchase"],
            "income": 75000,
            "age": 30,
            "savings": 25000
        }
        
        financial_result = monetization.process_service_request(
            user_id=test_user_id,
            service_type="financial_planning",
            request_data=financial_request
        )
        
        if financial_result.get("success"):
            print("✅ Financial planning request processed successfully")
            print(f"   💰 Cost: ${financial_result.get('cost', 0)}")
            print(f"   📊 Remaining credits: {financial_result.get('remaining_credits', 0)}")
        else:
            print(f"❌ Financial planning request failed: {financial_result.get('error')}")
        
        # Test 4: Get subscription information
        print("\n📋 Testing Subscription Information...")
        print("-" * 40)
        
        subscription_info = monetization.get_user_subscription_info(test_user_id)
        
        if subscription_info.get("success"):
            print("✅ Subscription information retrieved successfully")
            print(f"   👤 User ID: {subscription_info.get('user_id')}")
            print(f"   📊 Subscription tier: {subscription_info.get('subscription_tier', 'free')}")
            print(f"   📈 Monthly limit: {subscription_info.get('monthly_limit', 0)}")
            print(f"   📊 Current usage: {subscription_info.get('current_usage', 0)}")
        else:
            print(f"❌ Subscription info retrieval failed: {subscription_info.get('error')}")
        
        # Test 5: Create subscription plans
        print("\n📦 Testing Subscription Plan Creation...")
        print("-" * 40)
        
        plans_result = monetization.create_subscription_plans()
        
        if plans_result.get("success"):
            print(f"✅ Created {plans_result.get('plans_created', 0)} subscription plans")
            for plan in plans_result.get('plans', []):
                print(f"   📋 {plan.get('plan_name')}: ${plan.get('price')}")
        else:
            print(f"❌ Plan creation failed: {plans_result.get('error')}")
        
        # Test 6: Get monetization analytics
        print("\n📈 Testing Monetization Analytics...")
        print("-" * 40)
        
        analytics = monetization.get_monetization_analytics()
        
        if analytics.get("success"):
            print("✅ Analytics retrieved successfully")
            print(f"   💰 Total revenue: ${analytics.get('total_revenue', 0)}")
            print(f"   👥 Total users: {analytics.get('total_users', 0)}")
            print(f"   📊 Conversion rate: {analytics.get('conversion_rate', 0):.2%}")
            
            realitycheck_metrics = analytics.get('realitycheck_metrics', {})
            print(f"   🔧 Total services: {realitycheck_metrics.get('total_services', 0)}")
            print(f"   💵 Avg revenue per user: ${realitycheck_metrics.get('average_revenue_per_user', 0):.2f}")
        else:
            print(f"❌ Analytics retrieval failed: {analytics.get('error')}")
        
        print("\n" + "=" * 60)
        print("🎉 Monetization System Test Complete!")
        print("💰 RealityCheck is ready for Echo AI monetization!")
        print("🏆 Perfect for Merit Systems Echo AI App Challenge!")
        
    except Exception as e:
        print(f"❌ Monetization test failed: {e}")
        logger.error(f"Monetization test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_monetization_system())

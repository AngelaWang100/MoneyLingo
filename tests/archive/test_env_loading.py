"""
Test environment variable loading
"""
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_env_loading():
    """Test if environment variables are loaded correctly"""
    print("🔍 Testing environment variable loading...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file exists: {env_file}")
    else:
        print(f"❌ .env file not found: {env_file}")
        print("💡 Create .env file from env.example:")
        print("   cp env.example .env")
        return False
    
    # Check key environment variables
    env_vars = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
        "COMET_API_KEY": os.getenv("COMET_API_KEY"),
        "ECHO_API_KEY": os.getenv("ECHO_API_KEY"),
    }
    
    print("\n📋 Environment Variables Status:")
    for var_name, var_value in env_vars.items():
        if var_value and var_value != f"your_{var_name.lower()}_here":
            print(f"✅ {var_name}: {'*' * 10}...{var_value[-4:] if len(var_value) > 4 else '***'}")
        else:
            print(f"❌ {var_name}: Not set or using placeholder")
    
    # Check if we have at least some real API keys
    real_keys = [var for var in env_vars.values() if var and not var.startswith("your_") and not var.endswith("_here")]
    
    if real_keys:
        print(f"\n✅ Found {len(real_keys)} real API keys")
        return True
    else:
        print("\n❌ No real API keys found")
        print("💡 Please update your .env file with real API keys")
        return False

def test_agent_with_env():
    """Test agent initialization with environment variables"""
    print("\n🧪 Testing agent initialization with environment...")
    
    try:
        # Load environment
        load_dotenv()
        
        # Test if we can import and initialize agents
        from api.services.agents.translation_agent import TranslationAgent
        
        # Check if Google API key is available
        google_key = os.getenv("GOOGLE_API_KEY")
        if not google_key or google_key.startswith("your_"):
            print("❌ Google API key not properly configured")
            return False
        
        print("✅ Google API key found")
        
        # Try to initialize agent
        agent = TranslationAgent()
        print("✅ Translation agent initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_voice_service_with_env():
    """Test voice service with environment variables"""
    print("\n🎤 Testing voice service with environment...")
    
    try:
        # Load environment
        load_dotenv()
        
        # Test voice service
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        # Check ElevenLabs API key
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_key or elevenlabs_key.startswith("your_"):
            print("❌ ElevenLabs API key not properly configured")
            return False
        
        print("✅ ElevenLabs API key found")
        
        # Initialize voice service
        voice_service = ElevenLabsVoiceService()
        print("✅ Voice service initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice service initialization failed: {e}")
        return False

def run_env_tests():
    """Run all environment tests"""
    print("🚀 Starting environment variable tests...")
    
    tests = [
        ("Environment Loading", test_env_loading),
        ("Agent with Environment", test_agent_with_env),
        ("Voice Service with Environment", test_voice_service_with_env),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Testing {test_name}...")
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
    print("📊 ENVIRONMENT TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} environment tests passed")
    
    if passed == total:
        print("🎉 Environment variables are working correctly!")
    else:
        print("⚠️  Some environment issues found. Check the logs above.")
    
    return results

if __name__ == "__main__":
    run_env_tests()

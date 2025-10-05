#!/usr/bin/env python3
"""
Test the Translation Agent with Google API
"""
import asyncio
import os
from dotenv import load_dotenv
from agents.translation_agent import TranslationAgent

# Load environment variables
load_dotenv()

async def test_translation_agent():
    """Test the translation agent"""
    try:
        print("🤖 Testing Translation Agent...")
        
        # Create agent
        agent = TranslationAgent()
        print(f"✅ Created agent: {agent}")
        
        # Test data
        test_data = {
            "content": "Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods.",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        print(f"📝 Testing with: {test_data['content'][:50]}...")
        print(f"🌍 Target language: {test_data['language']}")
        print(f"👤 User level: {test_data['user_level']}")
        
        # Process request
        print("⏳ Processing translation...")
        result = await agent.process(test_data)
        
        if result.get("success"):
            print("✅ SUCCESS!")
            print(f"📄 Translated content:")
            print(f"   {result.get('translated_content', 'No content')}")
            print(f"🌍 Language: {result.get('language')}")
            print(f"👤 User level: {result.get('user_level')}")
        else:
            print("❌ FAILED!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
        return result.get("success", False)
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def main():
    print("🧪 Testing RealityCheck Translation Agent")
    print("=" * 50)
    
    success = await test_translation_agent()
    
    if success:
        print("\n🎉 Translation Agent is working perfectly!")
        print("Your RealityCheck system is ready for the hackathon!")
    else:
        print("\n⚠️  Translation Agent test failed.")
        print("Check your Google API key and try again.")

if __name__ == "__main__":
    asyncio.run(main())

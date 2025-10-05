#!/usr/bin/env python3
"""
Test Google API key with a simple Gemini request
"""
import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

async def test_google_api():
    """Test Google API key with a simple request"""
    try:
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment")
            print("Please set GOOGLE_API_KEY in your .env file")
            return False
        
        print(f"✅ Found GOOGLE_API_KEY: {api_key[:10]}...")
        
        # Create Gemini client
        print("🤖 Creating Gemini client...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.3
        )
        
        # Test with a simple request
        print("📝 Testing with simple request...")
        message = HumanMessage(content="Hello! Can you translate 'Hello World' to Spanish?")
        
        print("⏳ Sending request to Gemini...")
        response = await llm.ainvoke([message])
        
        print(f"✅ SUCCESS! Gemini response:")
        print(f"📄 {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

async def main():
    print("🧪 Testing Google API Key")
    print("=" * 40)
    
    success = await test_google_api()
    
    if success:
        print("\n🎉 Google API key is working perfectly!")
        print("Your RealityCheck agents are ready to use Gemini!")
    else:
        print("\n⚠️  Google API key test failed.")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    asyncio.run(main())

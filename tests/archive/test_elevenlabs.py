#!/usr/bin/env python3
"""
Test ElevenLabs integration with RealityCheck agents
"""
import asyncio
import os
from dotenv import load_dotenv
from voice.elevenlabs_service import ElevenLabsVoiceService
from agents.voice_translation_agent import VoiceTranslationAgent

# Load environment variables
load_dotenv()

async def test_elevenlabs_service():
    """Test ElevenLabs voice service"""
    print("🎤 Testing ElevenLabs Voice Service")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found")
        print("Please get your API key from: https://elevenlabs.io/")
        return False
    
    print(f"✅ Found ElevenLabs API key: {api_key[:10]}...")
    
    # Test voice service
    voice_service = ElevenLabsVoiceService()
    
    # Test available voices
    print("\n🔊 Testing available voices...")
    voices_result = voice_service.get_available_voices()
    
    if voices_result.get("success"):
        print(f"✅ Found {len(voices_result['voices'])} available voices")
        for voice in voices_result['voices'][:3]:  # Show first 3 voices
            print(f"   - {voice['name']} ({voice['voice_id']})")
    else:
        print(f"❌ Failed to get voices: {voices_result.get('error')}")
    
    # Test voice synthesis
    print("\n🎵 Testing voice synthesis...")
    test_text = "Hello! I'm your RealityCheck financial assistant. I can help you with translations, financial planning, and remittance analysis."
    
    synthesis_result = voice_service.synthesize_speech(
        text=test_text,
        language="en"
    )
    
    if synthesis_result.get("success"):
        print("✅ Voice synthesis successful!")
        print(f"📁 Audio file: {synthesis_result['filepath']}")
        print(f"📊 Text length: {synthesis_result['text_length']} characters")
    else:
        print(f"❌ Voice synthesis failed: {synthesis_result.get('error')}")
    
    return synthesis_result.get("success", False)

async def test_voice_translation_agent():
    """Test voice-enhanced translation agent"""
    print("\n🌍 Testing Voice-Enhanced Translation Agent")
    print("=" * 50)
    
    agent = VoiceTranslationAgent()
    
    # Test data
    test_data = {
        "content": "Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods.",
        "language": "Spanish",
        "user_level": "beginner"
    }
    
    print(f"📝 Input: {test_data['content'][:50]}...")
    print(f"🌍 Target: {test_data['language']}")
    
    # Test with voice
    result = await agent.process_with_voice(test_data, language="es")
    
    if result.get("success"):
        print("✅ Voice-enhanced translation successful!")
        print(f"📄 Translation length: {len(result.get('translated_content', ''))}")
        
        if result.get("voice", {}).get("success"):
            print(f"🎤 Voice file: {result['voice']['voice_file']}")
        else:
            print("⚠️  Voice synthesis not available")
    else:
        print(f"❌ Voice translation failed: {result.get('error')}")
    
    return result.get("success", False)

async def test_multilingual_voice():
    """Test multilingual voice synthesis"""
    print("\n🌐 Testing Multilingual Voice Synthesis")
    print("=" * 50)
    
    agent = VoiceTranslationAgent()
    
    if not agent.voice_enabled:
        print("⚠️  Voice synthesis not available - skipping multilingual test")
        return True
    
    # Test multilingual voice
    test_text = "Welcome to RealityCheck! I can help you with financial planning and remittance analysis."
    languages = ["en", "es", "fr"]
    
    result = await agent.create_multilingual_voice_response(test_text, languages)
    
    if result.get("success"):
        print("✅ Multilingual voice synthesis successful!")
        for lang, lang_result in result["multilingual_responses"].items():
            if lang_result.get("success"):
                print(f"   🌍 {lang}: {lang_result['filepath']}")
            else:
                print(f"   ❌ {lang}: {lang_result.get('error')}")
    else:
        print(f"❌ Multilingual voice failed: {result.get('error')}")
    
    return result.get("success", False)

async def main():
    print("🧪 REALITYCHECK ELEVENLABS INTEGRATION TEST")
    print("=" * 60)
    
    tests = [
        ("ElevenLabs Service", test_elevenlabs_service),
        ("Voice Translation Agent", test_voice_translation_agent),
        ("Multilingual Voice", test_multilingual_voice)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("ELEVENLABS INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ElevenLabs integration is working perfectly!")
        print("🎤 Your RealityCheck agents now have natural voice synthesis!")
        print("🏆 Ready for 'Best Use of ElevenLabs' prize!")
    else:
        print("⚠️  Some tests failed. Check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())

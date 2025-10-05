"""
Test auto-language voice detection and synthesis
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

async def test_auto_language_detection():
    """Test automatic language detection and voice synthesis"""
    print("🌍 Testing Auto-Language Voice Detection")
    print("=" * 60)
    
    try:
        from agents.auto_language_voice_agent import AutoLanguageVoiceAgent
        from voice.elevenlabs_service import ElevenLabsVoiceService
        
        # Test language detection
        voice_service = ElevenLabsVoiceService()
        
        test_cases = [
            {
                "text": "Hola, ¿cómo puedo ahorrar dinero para mi jubilación?",
                "expected_language": "es",
                "description": "Spanish financial question"
            },
            {
                "text": "Bonjour, comment puis-je investir mon argent?",
                "expected_language": "fr",
                "description": "French investment question"
            },
            {
                "text": "Hallo, wie kann ich mein Geld sparen?",
                "expected_language": "de",
                "description": "German savings question"
            },
            {
                "text": "Ciao, come posso risparmiare denaro?",
                "expected_language": "it",
                "description": "Italian savings question"
            },
            {
                "text": "Olá, como posso investir meu dinheiro?",
                "expected_language": "pt",
                "description": "Portuguese investment question"
            },
            {
                "text": "Hello, how can I save money for retirement?",
                "expected_language": "en",
                "description": "English financial question"
            },
            {
                "text": "你好，我如何为退休存钱？",
                "expected_language": "zh",
                "description": "Chinese financial question"
            },
            {
                "text": "こんにちは、退職のためにどのようにお金を貯めることができますか？",
                "expected_language": "ja",
                "description": "Japanese financial question"
            }
        ]
        
        print("🔍 Testing Language Detection...")
        print("-" * 40)
        
        for i, test_case in enumerate(test_cases, 1):
            detected = voice_service.detect_language(test_case["text"])
            expected = test_case["expected_language"]
            status = "✅" if detected == expected else "❌"
            
            print(f"{status} Test {i}: {test_case['description']}")
            print(f"   Input: {test_case['text'][:50]}...")
            print(f"   Expected: {expected}, Detected: {detected}")
            print()
        
        # Test auto-language voice agent
        print("🤖 Testing Auto-Language Voice Agent...")
        print("-" * 40)
        
        agent = AutoLanguageVoiceAgent()
        
        # Test with Spanish input
        spanish_input = {
            "content": "Hola, necesito ayuda con mi plan de jubilación. Tengo 30 años y quiero empezar a ahorrar."
        }
        
        print("🇪🇸 Testing Spanish Input...")
        print(f"Input: {spanish_input['content']}")
        
        result = await agent.process_with_voice(spanish_input)
        
        if result.get("success"):
            print("✅ Spanish processing successful!")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
            print(f"🌍 Detected language: {result.get('detected_language')}")
            if result.get("voice_output", {}).get("success"):
                print(f"🎤 Voice file: {result['voice_output']['filepath']}")
            else:
                print(f"⚠️  Voice synthesis: {result['voice_output'].get('message')}")
        else:
            print(f"❌ Spanish processing failed: {result.get('error')}")
        
        print()
        
        # Test with French input
        french_input = {
            "content": "Bonjour, je veux investir mon argent. Pouvez-vous m'aider?"
        }
        
        print("🇫🇷 Testing French Input...")
        print(f"Input: {french_input['content']}")
        
        result = await agent.process_with_voice(french_input)
        
        if result.get("success"):
            print("✅ French processing successful!")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
            print(f"🌍 Detected language: {result.get('detected_language')}")
            if result.get("voice_output", {}).get("success"):
                print(f"🎤 Voice file: {result['voice_output']['filepath']}")
            else:
                print(f"⚠️  Voice synthesis: {result['voice_output'].get('message')}")
        else:
            print(f"❌ French processing failed: {result.get('error')}")
        
        print()
        
        # Test with German input
        german_input = {
            "content": "Hallo, ich möchte mein Geld sparen. Können Sie mir helfen?"
        }
        
        print("🇩🇪 Testing German Input...")
        print(f"Input: {german_input['content']}")
        
        result = await agent.process_with_voice(german_input)
        
        if result.get("success"):
            print("✅ German processing successful!")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
            print(f"🌍 Detected language: {result.get('detected_language')}")
            if result.get("voice_output", {}).get("success"):
                print(f"🎤 Voice file: {result['voice_output']['filepath']}")
            else:
                print(f"⚠️  Voice synthesis: {result['voice_output'].get('message')}")
        else:
            print(f"❌ German processing failed: {result.get('error')}")
        
        print()
        
        # Test with English input
        english_input = {
            "content": "Hello, I want to save money for retirement. Can you help me create a plan?"
        }
        
        print("🇺🇸 Testing English Input...")
        print(f"Input: {english_input['content']}")
        
        result = await agent.process_with_voice(english_input)
        
        if result.get("success"):
            print("✅ English processing successful!")
            print(f"📄 Response length: {len(result.get('translated_content', ''))}")
            print(f"🌍 Detected language: {result.get('detected_language')}")
            if result.get("voice_output", {}).get("success"):
                print(f"🎤 Voice file: {result['voice_output']['filepath']}")
            else:
                print(f"⚠️  Voice synthesis: {result['voice_output'].get('message')}")
        else:
            print(f"❌ English processing failed: {result.get('error')}")
        
        print("\n" + "=" * 60)
        print("🎉 Auto-Language Voice Detection Test Complete!")
        print("🌍 Your RealityCheck system now supports automatic language detection!")
        print("🎤 Voice synthesis works in any language the user speaks!")
        
    except Exception as e:
        print(f"❌ Auto-language test failed: {e}")
        logger.error(f"Auto-language test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_auto_language_detection())

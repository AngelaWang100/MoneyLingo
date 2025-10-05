"""
Comprehensive logging system for all RealityCheck agents
"""
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentOutputLogger:
    """Comprehensive logging system for all agents"""
    
    def __init__(self):
        self.logs = []
        self.start_time = datetime.now()
        
    def log_agent_output(self, agent_name: str, input_data: dict, output_data: dict, execution_time: float):
        """Log agent output with comprehensive details"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "input_data": input_data,
            "output_data": output_data,
            "execution_time_seconds": execution_time,
            "success": output_data.get("success", False),
            "response_length": len(str(output_data.get("translated_content", output_data.get("ai_recommendations", output_data.get("ai_analysis", ""))))),
            "voice_enabled": "voice_output" in output_data
        }
        self.logs.append(log_entry)
        
        # Print summary
        status = "✅ SUCCESS" if log_entry["success"] else "❌ FAILED"
        print(f"{status} {agent_name.upper()}")
        print(f"   📄 Response length: {log_entry['response_length']} characters")
        print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
        if log_entry["voice_enabled"]:
            print(f"   🎤 Voice output: {output_data.get('voice_output', {}).get('filepath', 'N/A')}")
        print()
    
    def save_logs(self, filename: str = None):
        """Save all logs to JSON file"""
        if filename is None:
            filename = f"agent_outputs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            "session_info": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_agents_tested": len(self.logs),
                "successful_agents": len([log for log in self.logs if log["success"]]),
                "failed_agents": len([log for log in self.logs if not log["success"]])
            },
            "agent_outputs": self.logs
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📁 Logs saved to: {filename}")
        return filename

async def test_all_agents_with_logging():
    """Test all agents with comprehensive logging"""
    print("🧪 COMPREHENSIVE REALITYCHECK AGENT TESTING")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    logger = AgentOutputLogger()
    
    # Test Translation Agent
    print("🌍 Testing Translation Agent...")
    try:
        from agents.translation_agent import TranslationAgent
        start_time = datetime.now()
        
        translation_agent = TranslationAgent()
        input_data = {
            "content": "Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods. This is a fundamental concept in personal finance and investment planning.",
            "language": "Spanish",
            "user_level": "beginner"
        }
        
        result = await translation_agent.process(input_data)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.log_agent_output("translation_agent", input_data, result, execution_time)
        
    except Exception as e:
        print(f"❌ Translation Agent failed: {e}")
        logger.log_agent_output("translation_agent", input_data, {"error": str(e), "success": False}, 0)
    
    # Test Financial Planning Agent
    print("💰 Testing Financial Planning Agent...")
    try:
        from agents.financial_planning_agent import FinancialPlanningAgent
        start_time = datetime.now()
        
        financial_agent = FinancialPlanningAgent()
        input_data = {
            "user_profile": {
                "age": 28,
                "income": 75000,
                "savings": 25000,
                "debt": 15000,
                "goals": ["retirement", "house_purchase", "emergency_fund"]
            },
            "request": "Create a comprehensive financial plan for retirement and house purchase"
        }
        
        result = await financial_agent.process(input_data)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.log_agent_output("financial_planning_agent", input_data, result, execution_time)
        
    except Exception as e:
        print(f"❌ Financial Planning Agent failed: {e}")
        logger.log_agent_output("financial_planning_agent", input_data, {"error": str(e), "success": False}, 0)
    
    # Test Remittance Agent
    print("💸 Testing Remittance Agent...")
    try:
        from agents.remittance_agent import RemittanceAgent
        start_time = datetime.now()
        
        remittance_agent = RemittanceAgent()
        input_data = {
            "amount": 2500,
            "currency": "USD",
            "destination": "Mexico",
            "user_preferences": {
                "speed": "fast",
                "cost": "low",
                "security": "high"
            }
        }
        
        result = await remittance_agent.process(input_data)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.log_agent_output("remittance_agent", input_data, result, execution_time)
        
    except Exception as e:
        print(f"❌ Remittance Agent failed: {e}")
        logger.log_agent_output("remittance_agent", input_data, {"error": str(e), "success": False}, 0)
    
    # Test Voice Translation Agent
    print("🎤 Testing Voice Translation Agent...")
    try:
        from agents.voice_translation_agent import VoiceTranslationAgent
        start_time = datetime.now()
        
        voice_agent = VoiceTranslationAgent()
        input_data = {
            "content": "Here's your personalized retirement plan with XRPL remittance options for international transfers.",
            "language": "Spanish",
            "user_level": "intermediate"
        }
        
        result = await voice_agent.process_with_voice(input_data, language="es")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.log_agent_output("voice_translation_agent", input_data, result, execution_time)
        
    except Exception as e:
        print(f"❌ Voice Translation Agent failed: {e}")
        logger.log_agent_output("voice_translation_agent", input_data, {"error": str(e), "success": False}, 0)
    
    # Test Voice Service Directly
    print("🔊 Testing ElevenLabs Voice Service...")
    try:
        from voice.elevenlabs_service import ElevenLabsVoiceService
        start_time = datetime.now()
        
        voice_service = ElevenLabsVoiceService()
        input_data = {
            "text": "Welcome to RealityCheck, your AI-powered financial assistant. I can help you with retirement planning, international remittances, and financial translations.",
            "language": "en"
        }
        
        result = voice_service.synthesize_speech(input_data["text"], language=input_data["language"])
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.log_agent_output("elevenlabs_voice_service", input_data, result, execution_time)
        
    except Exception as e:
        print(f"❌ ElevenLabs Voice Service failed: {e}")
        logger.log_agent_output("elevenlabs_voice_service", input_data, {"error": str(e), "success": False}, 0)
    
    # Save all logs
    print("\n" + "=" * 60)
    print("📊 SAVING COMPREHENSIVE LOGS...")
    print("=" * 60)
    
    log_file = logger.save_logs()
    
    # Print summary
    print("\n📈 TEST SUMMARY")
    print("=" * 30)
    print(f"✅ Successful agents: {len([log for log in logger.logs if log['success']])}")
    print(f"❌ Failed agents: {len([log for log in logger.logs if not log['success']])}")
    print(f"📁 Log file: {log_file}")
    print(f"📄 Total log entries: {len(logger.logs)}")
    
    # Show voice files generated
    voice_files = []
    for log in logger.logs:
        if log.get("voice_enabled") and log.get("success"):
            voice_output = log["output_data"].get("voice_output", {})
            if voice_output.get("filepath"):
                voice_files.append(voice_output["filepath"])
    
    if voice_files:
        print(f"\n🎤 Voice files generated: {len(voice_files)}")
        for voice_file in voice_files:
            print(f"   📁 {voice_file}")
    
    print(f"\n🎉 Comprehensive agent testing complete!")
    print(f"📊 All outputs logged to: {log_file}")

if __name__ == "__main__":
    asyncio.run(test_all_agents_with_logging())

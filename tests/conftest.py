"""
Test configuration and fixtures for RealityCheck
"""
import os
import sys
import asyncio
import pytest
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

@pytest.fixture
def test_data():
    """Common test data"""
    return {
        "financial_planning": {
            "goals": ["retirement planning"],
            "income": 5000,
            "expenses": 3000,
            "timeline": "1 year",
            "language": "English",
            "user_level": "beginner"
        },
        "translation": {
            "content": "Hello, I need help with retirement planning",
            "language": "Spanish",
            "user_level": "beginner"
        },
        "remittance": {
            "amount": 1000,
            "currency": "USD",
            "destination": "Mexico",
            "source_country": "United States",
            "destination_country": "Mexico"
        },
        "voice": {
            "text": "Hello, this is a test",
            "language": "en"
        },
        "research": {
            "query": "retirement planning strategies 2024",
            "research_type": "retirement_planning",
            "max_results": 3
        }
    }

@pytest.fixture
def orchestrator():
    """Orchestrator fixture"""
    from api.services.agents.orchestrator import AgentOrchestrator
    return AgentOrchestrator()

@pytest.fixture
def translation_agent():
    """Translation agent fixture"""
    from api.services.agents.translation_agent import TranslationAgent
    return TranslationAgent()

@pytest.fixture
def financial_agent():
    """Financial planning agent fixture"""
    from api.services.agents.financial_planning_agent import FinancialPlanningAgent
    return FinancialPlanningAgent()

@pytest.fixture
def remittance_agent():
    """Remittance agent fixture"""
    from api.services.agents.remittance_agent import RemittanceAgent
    return RemittanceAgent()

@pytest.fixture
def voice_service():
    """Voice service fixture"""
    from voice.elevenlabs_service import ElevenLabsVoiceService
    return ElevenLabsVoiceService()

@pytest.fixture
def auto_language_agent():
    """Auto language voice agent fixture"""
    from api.services.agents.auto_language_voice_agent import AutoLanguageVoiceAgent
    return AutoLanguageVoiceAgent()

@pytest.fixture
def voice_translation_agent():
    """Voice translation agent fixture"""
    from api.services.agents.voice_translation_agent import VoiceTranslationAgent
    return VoiceTranslationAgent()

@pytest.fixture
def research_agent():
    """Tavily research agent fixture"""
    from api.services.agents.tavily_research_agent import TavilyResearchAgent
    return TavilyResearchAgent()

@pytest.fixture
def observer():
    """Comet observer fixture"""
    from api.services.observability.comet_integration import CometObserver
    return CometObserver()

@pytest.fixture
def monetization_service():
    """Monetization service fixture"""
    from monetization.monetization_service import RealityCheckMonetization
    return RealityCheckMonetization()

# Async test support
@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

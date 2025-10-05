"""
Main orchestrator for coordinating all agents
"""
import asyncio
from typing import Dict, Any, List
import logging

from .translation_agent import TranslationAgent
from .financial_planning_agent import FinancialPlanningAgent
from .remittance_agent import RemittanceAgent
from .auto_language_voice_agent import AutoLanguageVoiceAgent
from .voice_translation_agent import VoiceTranslationAgent
from .tavily_research_agent import TavilyResearchAgent

class AgentOrchestrator:
    """Orchestrates all agents with robust error handling"""
    
    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        self.translation_agent = TranslationAgent()
        self.financial_planning_agent = FinancialPlanningAgent()
        self.remittance_agent = RemittanceAgent()
        self.auto_language_voice_agent = AutoLanguageVoiceAgent()
        self.voice_translation_agent = VoiceTranslationAgent()
        self.tavily_research_agent = TavilyResearchAgent()
    
    async def _run_agent_safely(self, agent, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run an agent safely with error handling"""
        try:
            self.logger.info(f"Running {agent_name}...")
            result = await agent.process(input_data)
            self.logger.info(f"{agent_name} completed successfully")
            return {
                "success": True,
                "agent": agent_name,
                "result": result,
                "error": None
            }
        except Exception as e:
            self.logger.error(f"{agent_name} failed: {e}")
            return {
                "success": False,
                "agent": agent_name,
                "result": None,
                "error": str(e)
            }
    
    async def process_request(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete request through all agents with robust orchestration"""
        try:
            self.logger.info("Starting orchestration process...")
            
            # Run all agents with error handling
            agent_results = {}
            successful_agents = []
            failed_agents = []
            
            # Run Translation Agent
            translation_result = await self._run_agent_safely(
                self.translation_agent, "translation_agent", input_data
            )
            agent_results["translation"] = translation_result
            if translation_result["success"]:
                successful_agents.append("translation")
            else:
                failed_agents.append("translation")
            
            # Run Financial Planning Agent
            financial_result = await self._run_agent_safely(
                self.financial_planning_agent, "financial_planning_agent", input_data
            )
            agent_results["financial_planning"] = financial_result
            if financial_result["success"]:
                successful_agents.append("financial_planning")
            else:
                failed_agents.append("financial_planning")
            
            # Run Remittance Agent
            remittance_result = await self._run_agent_safely(
                self.remittance_agent, "remittance_agent", input_data
            )
            agent_results["remittance"] = remittance_result
            if remittance_result["success"]:
                successful_agents.append("remittance")
            else:
                failed_agents.append("remittance")
            
            # Create synthesis
            synthesis = self._create_synthesis(agent_results, successful_agents, failed_agents)
            
            self.logger.info(f"Orchestration completed: {len(successful_agents)}/{len(agent_results)} agents successful")
            
            return {
                "success": len(successful_agents) > 0,  # Success if at least one agent worked
                "result": {
                    "synthesis": synthesis,
                    "agent_results": agent_results,
                    "successful_agents": successful_agents,
                    "failed_agents": failed_agents
                },
                "agents_used": list(agent_results.keys()),
                "successful_count": len(successful_agents),
                "total_count": len(agent_results)
            }
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agents_used": [],
                "successful_count": 0,
                "total_count": 0
            }
    
    def _create_synthesis(self, agent_results: Dict[str, Any], successful_agents: List[str], failed_agents: List[str]) -> str:
        """Create a synthesis of all agent results"""
        synthesis_parts = []
        
        if successful_agents:
            synthesis_parts.append(f"Successfully processed by {len(successful_agents)} agents: {', '.join(successful_agents)}")
        
        if failed_agents:
            synthesis_parts.append(f"Failed agents: {', '.join(failed_agents)}")
        
        # Add key insights from successful agents
        for agent_name in successful_agents:
            result = agent_results[agent_name]["result"]
            if result and result.get("success"):
                if agent_name == "translation" and result.get("translated_content"):
                    synthesis_parts.append(f"Translation: Content translated successfully")
                elif agent_name == "financial_planning" and result.get("ai_recommendations"):
                    synthesis_parts.append(f"Financial Planning: AI recommendations generated")
                elif agent_name == "remittance" and result.get("ai_analysis"):
                    synthesis_parts.append(f"Remittance: Analysis completed")
        
        return " | ".join(synthesis_parts) if synthesis_parts else "No agents completed successfully"

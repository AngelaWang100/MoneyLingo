"""
Main orchestrator for coordinating all agents
"""
import asyncio
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import logging

from .translation_agent import TranslationAgent
from .financial_planning_agent import FinancialPlanningAgent
from .remittance_agent import RemittanceAgent

class AgentOrchestrator:
    """Orchestrates all agents using LangGraph"""
    
    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        self.translation_agent = TranslationAgent()
        self.financial_planning_agent = FinancialPlanningAgent()
        self.remittance_agent = RemittanceAgent()
        
        # Build the agent graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph({"messages": add_messages})
        
        # Add nodes for each agent
        workflow.add_node("translation", self._translation_node)
        workflow.add_node("financial_planning", self._financial_planning_node)
        workflow.add_node("remittance", self._remittance_node)
        workflow.add_node("final_synthesis", self._synthesis_node)
        
        # Define the flow
        workflow.set_entry_point("translation")
        workflow.add_edge("translation", "financial_planning")
        workflow.add_edge("financial_planning", "remittance")
        workflow.add_edge("remittance", "final_synthesis")
        workflow.add_edge("final_synthesis", END)
        
        return workflow.compile()
    
    async def _translation_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Translation agent node"""
        try:
            result = await self.translation_agent.process(state.get("input_data", {}))
            return {
                "messages": [AIMessage(content=f"Translation completed: {result}")]
            }
        except Exception as e:
            self.logger.error(f"Translation node failed: {e}")
            return {
                "messages": [AIMessage(content=f"Translation failed: {str(e)}")]
            }
    
    async def _financial_planning_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Financial planning agent node"""
        try:
            result = await self.financial_planning_agent.process(state.get("input_data", {}))
            return {
                "messages": [AIMessage(content=f"Financial planning completed: {result}")]
            }
        except Exception as e:
            self.logger.error(f"Financial planning node failed: {e}")
            return {
                "messages": [AIMessage(content=f"Financial planning failed: {str(e)}")]
            }
    
    async def _remittance_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Remittance agent node"""
        try:
            result = await self.remittance_agent.process(state.get("input_data", {}))
            return {
                "messages": [AIMessage(content=f"Remittance processing completed: {result}")]
            }
        except Exception as e:
            self.logger.error(f"Remittance node failed: {e}")
            return {
                "messages": [AIMessage(content=f"Remittance processing failed: {str(e)}")]
            }
    
    async def _synthesis_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Final synthesis of all agent results"""
        try:
            messages = state.get("messages", [])
            synthesis = f"All agents have completed processing. Results: {len(messages)} messages processed."
            return {
                "messages": [AIMessage(content=synthesis)]
            }
        except Exception as e:
            self.logger.error(f"Synthesis node failed: {e}")
            return {
                "messages": [AIMessage(content=f"Synthesis failed: {str(e)}")]
            }
    
    async def process_request(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete request through all agents"""
        try:
            initial_state = {
                "messages": [HumanMessage(content=str(input_data))],
                "input_data": input_data
            }
            
            result = await self.graph.ainvoke(initial_state)
            
            self.logger.info(f"Orchestration completed successfully")
            return {
                "success": True,
                "result": result,
                "agents_used": ["translation", "financial_planning", "remittance"]
            }
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agents_used": []
            }

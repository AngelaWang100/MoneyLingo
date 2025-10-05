"""
Financial planning agent that orchestrates workflows and calls backend APIs
"""
import os
import requests
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from .base_agent import BaseAgent

class FinancialPlanningAgent(BaseAgent):
    """Agent for financial planning workflows and backend API coordination"""
    
    def __init__(self):
        super().__init__(
            name="financial_planning_agent",
            description="Orchestrates financial planning workflows and coordinates with backend APIs"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key="AIzaSyD0zqBY42YTeKwij1kL6RAaERjuxEtthzs",
            temperature=0.2
        )
        self.backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process financial planning request and coordinate with backend"""
        try:
            user_goals = input_data.get("goals", [])
            user_income = input_data.get("income", 0)
            user_expenses = input_data.get("expenses", 0)
            user_timeline = input_data.get("timeline", "1 year")
            
            # Create planning prompt
            planning_prompt = f"""
            Create a comprehensive financial plan based on:
            - Goals: {user_goals}
            - Monthly Income: ${user_income}
            - Monthly Expenses: ${user_expenses}
            - Timeline: {user_timeline}
            
            Provide specific, actionable recommendations including:
            1. Budget allocation
            2. Savings strategy
            3. Investment recommendations
            4. Risk assessment
            5. Timeline milestones
            """
            
            messages = [
                SystemMessage(content="You are a certified financial planner. Provide detailed, actionable financial advice."),
                HumanMessage(content=planning_prompt)
            ]
            
            # Get AI recommendations
            response = await self.llm.ainvoke(messages)
            
            # Call backend APIs to get real data
            plan_data = await self._call_plan_api(user_goals, user_income, user_expenses)
            transaction_data = await self._call_transactions_api()
            
            # Log the planning decision
            self.log_decision(
                decision="Generated financial plan with backend integration",
                context={
                    "goals_count": len(user_goals),
                    "income": user_income,
                    "expenses": user_expenses,
                    "backend_connected": plan_data.get("success", False)
                },
                confidence=0.85
            )
            
            return {
                "ai_recommendations": response.content,
                "backend_plan": plan_data,
                "transaction_insights": transaction_data,
                "agent": self.name,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Financial planning failed: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "success": False
            }
    
    async def _call_plan_api(self, goals: List[str], income: float, expenses: float) -> Dict[str, Any]:
        """Call the backend plan API"""
        try:
            url = f"{self.backend_url}{os.getenv('PLAN_ENDPOINT', '/plan')}"
            payload = {
                "goals": goals,
                "income": income,
                "expenses": expenses
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.json() if response.status_code == 200 else {"success": False, "error": "API call failed"}
        except Exception as e:
            self.logger.warning(f"Plan API call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_transactions_api(self) -> Dict[str, Any]:
        """Call the backend transactions API"""
        try:
            url = f"{self.backend_url}{os.getenv('TRANSACTIONS_ENDPOINT', '/transactions')}"
            response = requests.get(url, timeout=10)
            return response.json() if response.status_code == 200 else {"success": False, "error": "API call failed"}
        except Exception as e:
            self.logger.warning(f"Transactions API call failed: {e}")
            return {"success": False, "error": str(e)}

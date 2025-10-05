"""
Financial planning routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from api.models.financial import FinancialRequest, FinancialResponse, BudgetRequest, BudgetResponse
from api.dependencies import get_orchestrator, get_observer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/plan", response_model=FinancialResponse, status_code=status.HTTP_200_OK)
async def create_financial_plan(
    request: FinancialRequest,
    orchestrator = Depends(get_orchestrator),
    observer = Depends(get_observer)
) -> FinancialResponse:
    """Create a comprehensive financial plan"""
    try:
        observer.log_agent_start("financial_orchestrator", request.dict())
        
        input_data = {
            "goals": request.goals,
            "income": request.income,
            "expenses": request.expenses,
            "timeline": request.timeline,
            "language": request.language,
            "user_level": request.user_level
        }
        
        result = await orchestrator.process_request(input_data)
        
        observer.log_agent_end("financial_orchestrator", result, result.get("success", False))
        
        return FinancialResponse(
            success=result.get("success", False),
            ai_recommendations=result.get("ai_recommendations"),
            backend_plan=result.get("backend_plan"),
            transaction_insights=result.get("transaction_insights"),
            agent=result.get("agent", "financial_orchestrator"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Financial planning failed: {e}")
        observer.log_error("financial_orchestrator", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Financial planning failed: {str(e)}"
        )

@router.post("/budget", response_model=BudgetResponse, status_code=status.HTTP_200_OK)
async def analyze_budget(
    request: BudgetRequest,
    orchestrator = Depends(get_orchestrator),
    observer = Depends(get_observer)
) -> BudgetResponse:
    """Analyze budget and provide recommendations"""
    try:
        observer.log_agent_start("budget_analysis", request.dict())
        
        # Convert budget request to orchestrator format
        input_data = {
            "goals": ["Budget optimization"],
            "income": request.income,
            "expenses": sum(request.expenses.values()),
            "timeline": "1 month",
            "language": request.language,
            "user_level": "beginner"
        }
        
        result = await orchestrator.process_request(input_data)
        
        observer.log_agent_end("budget_analysis", result, result.get("success", False))
        
        return BudgetResponse(
            success=result.get("success", False),
            budget_analysis=result.get("backend_plan"),
            recommendations=result.get("ai_recommendations"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Budget analysis failed: {e}")
        observer.log_error("budget_analysis", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Budget analysis failed: {str(e)}"
        )

@router.get("/analytics")
async def get_financial_analytics(
    orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Get financial analytics and insights"""
    try:
        # This would typically query a database for analytics
        # Real financial data required - no mock responses
        raise NotImplementedError("Real financial backend is required - no mock responses available")
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analytics retrieval failed: {str(e)}"
        )

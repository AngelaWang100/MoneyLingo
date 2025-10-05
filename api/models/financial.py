"""
Financial planning models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FinancialRequest(BaseModel):
    """Request model for financial planning"""
    goals: List[str] = Field(..., description="Financial goals")
    income: float = Field(..., gt=0, description="Monthly income")
    expenses: float = Field(..., ge=0, description="Monthly expenses")
    timeline: str = Field(default="1 year", description="Planning timeline")
    language: str = Field(default="English", description="Preferred language")
    user_level: str = Field(default="beginner", description="User experience level")

class FinancialResponse(BaseModel):
    """Response model for financial planning"""
    success: bool
    ai_recommendations: Optional[str] = None
    backend_plan: Optional[dict] = None
    transaction_insights: Optional[dict] = None
    agent: str
    error: Optional[str] = None

class BudgetRequest(BaseModel):
    """Request model for budget analysis"""
    income: float = Field(..., gt=0)
    expenses: dict = Field(..., description="Expense categories")
    savings_goal: float = Field(default=0, ge=0)
    language: str = Field(default="English")

class BudgetResponse(BaseModel):
    """Response model for budget analysis"""
    success: bool
    budget_analysis: Optional[dict] = None
    recommendations: Optional[str] = None
    error: Optional[str] = None

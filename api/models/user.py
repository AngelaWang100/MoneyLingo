"""
User and authentication models
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, Literal
from datetime import datetime

# Authentication models
class LoginRequest(BaseModel):
    email: EmailStr
    auth_code: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int  # in seconds
    user_id: int

class UserProfile(BaseModel):
    user_id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime

class UserInDB(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

# Legacy models for backward compatibility
class UserRequest(BaseModel):
    """Base user request model"""
    user_id: str = Field(..., description="User identifier")
    session_token: Optional[str] = Field(None, description="Session token")

class SubscriptionInfo(BaseModel):
    """User subscription information"""
    user_id: str
    subscription_tier: str
    remaining_credits: int
    services: Dict[str, Any]
    expires_at: Optional[datetime] = None

class AccessCheckRequest(BaseModel):
    """Request model for access checking"""
    user_id: str = Field(..., description="User identifier")
    service_type: str = Field(..., description="Service type to check")

class AccessCheckResponse(BaseModel):
    """Response model for access checking"""
    access: bool
    remaining_credits: Optional[int] = None
    subscription_tier: Optional[str] = None
    upgrade_required: Optional[bool] = None
    reason: Optional[str] = None

class ServiceRequest(BaseModel):
    """Request model for service processing"""
    user_id: str = Field(..., description="User identifier")
    service_type: str = Field(..., description="Service type")
    request_data: Dict[str, Any] = Field(..., description="Request data")

class ServiceResponse(BaseModel):
    """Response model for service processing"""
    success: bool
    service_type: str
    cost: Optional[float] = None
    remaining_credits: Optional[int] = None
    tracking_id: Optional[str] = None
    payment_id: Optional[str] = None
    error: Optional[str] = None

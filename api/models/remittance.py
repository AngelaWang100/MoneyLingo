"""
Remittance and XRPL models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class RemittanceRequest(BaseModel):
    """Request model for remittance analysis"""
    amount: float = Field(..., gt=0, description="Transfer amount")
    currency: str = Field(default="USD", description="Currency code")
    destination: str = Field(..., description="Destination country/region")
    source_country: str = Field(..., description="Source country")
    destination_country: str = Field(..., description="Destination country")

class RemittanceResponse(BaseModel):
    """Response model for remittance analysis"""
    success: bool
    xrpl_analysis: Optional[Dict[str, Any]] = None
    cost_breakdown: Optional[Dict[str, Any]] = None
    recommendations: Optional[str] = None
    agent: str
    error: Optional[str] = None

class XRPLTransactionRequest(BaseModel):
    """Request model for XRPL transaction"""
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD")
    destination_address: str = Field(..., description="XRPL destination address")
    source_address: str = Field(..., description="XRPL source address")

class XRPLTransactionResponse(BaseModel):
    """Response model for XRPL transaction"""
    success: bool
    transaction_id: Optional[str] = None
    fees: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None

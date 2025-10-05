"""
Remittance and XRPL routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from api.models.remittance import (
    RemittanceRequest, RemittanceResponse, 
    XRPLTransactionRequest, XRPLTransactionResponse
)
from api.dependencies import get_orchestrator, get_observer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=RemittanceResponse, status_code=status.HTTP_200_OK)
async def analyze_remittance(
    request: RemittanceRequest,
    orchestrator = Depends(get_orchestrator),
    observer = Depends(get_observer)
) -> RemittanceResponse:
    """Analyze remittance options and costs"""
    try:
        observer.log_agent_start("remittance_orchestrator", request.dict())
        
        input_data = {
            "amount": request.amount,
            "currency": request.currency,
            "destination": request.destination,
            "source_country": request.source_country,
            "destination_country": request.destination_country
        }
        
        result = await orchestrator.process_request(input_data)
        
        observer.log_agent_end("remittance_orchestrator", result, result.get("success", False))
        
        return RemittanceResponse(
            success=result.get("success", False),
            xrpl_analysis=result.get("xrpl_analysis"),
            cost_breakdown=result.get("cost_breakdown"),
            recommendations=result.get("recommendations"),
            agent=result.get("agent", "remittance_agent"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Remittance analysis failed: {e}")
        observer.log_error("remittance_orchestrator", str(e), {"request": request.dict()})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Remittance analysis failed: {str(e)}"
        )

@router.post("/xrpl/transaction", response_model=XRPLTransactionResponse, status_code=status.HTTP_200_OK)
async def create_xrpl_transaction(
    request: XRPLTransactionRequest,
    orchestrator = Depends(get_orchestrator)
) -> XRPLTransactionResponse:
    """Create XRPL transaction"""
    try:
        # This would integrate with XRPL testnet
        # Real XRPL integration required - no mock responses
        raise NotImplementedError("Real XRPL backend is required - no mock responses available")
        
    except Exception as e:
        logger.error(f"XRPL transaction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"XRPL transaction failed: {str(e)}"
        )

@router.get("/xrpl/status/{transaction_id}")
async def get_transaction_status(transaction_id: str) -> Dict[str, Any]:
    """Get XRPL transaction status"""
    try:
        # Real XRPL status check required - no mock responses
        raise NotImplementedError("Real XRPL backend is required - no mock responses available")
    except Exception as e:
        logger.error(f"Transaction status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transaction status check failed: {str(e)}"
        )

@router.get("/currencies")
async def get_supported_currencies() -> Dict[str, Any]:
    """Get list of supported currencies"""
    return {
        "success": True,
        "currencies": [
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
            {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$"},
            {"code": "AUD", "name": "Australian Dollar", "symbol": "A$"},
            {"code": "XRP", "name": "XRP", "symbol": "XRP"}
        ]
    }

@router.get("/countries")
async def get_supported_countries() -> Dict[str, Any]:
    """Get list of supported countries"""
    return {
        "success": True,
        "countries": [
            {"code": "US", "name": "United States"},
            {"code": "CA", "name": "Canada"},
            {"code": "GB", "name": "United Kingdom"},
            {"code": "DE", "name": "Germany"},
            {"code": "FR", "name": "France"},
            {"code": "JP", "name": "Japan"},
            {"code": "AU", "name": "Australia"},
            {"code": "IN", "name": "India"},
            {"code": "MX", "name": "Mexico"},
            {"code": "BR", "name": "Brazil"}
        ]
    }

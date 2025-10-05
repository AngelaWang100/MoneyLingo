"""
Monetization and Echo AI routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
import logging

from api.models.user import (
    SubscriptionInfo, AccessCheckRequest, AccessCheckResponse,
    ServiceRequest, ServiceResponse
)
from api.dependencies import get_monetization_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/subscription/{user_id}", response_model=SubscriptionInfo, status_code=status.HTTP_200_OK)
async def get_subscription_info(
    user_id: str,
    monetization_service = Depends(get_monetization_service)
) -> SubscriptionInfo:
    """Get user subscription information"""
    try:
        result = monetization_service.get_user_subscription_info(user_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get("error", "Subscription not found")
            )
        
        return SubscriptionInfo(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Subscription info retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Subscription info retrieval failed: {str(e)}"
        )

@router.get("/pricing")
async def get_pricing_info(
    monetization_service = Depends(get_monetization_service)
) -> Dict[str, Any]:
    """Get pricing information for all services"""
    try:
        return {
            "success": True,
            "pricing": monetization_service.service_pricing,
            "currency": "USD",
            "description": "RealityCheck AI Financial Assistant Pricing"
        }
    except Exception as e:
        logger.error(f"Pricing info retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pricing info retrieval failed: {str(e)}"
        )

@router.post("/check-access", response_model=AccessCheckResponse, status_code=status.HTTP_200_OK)
async def check_user_access(
    request: AccessCheckRequest,
    monetization_service = Depends(get_monetization_service)
) -> AccessCheckResponse:
    """Check if user has access to a service"""
    try:
        result = monetization_service.check_user_access(request.user_id, request.service_type)
        
        return AccessCheckResponse(
            access=result.get("access", False),
            remaining_credits=result.get("remaining_credits"),
            subscription_tier=result.get("subscription_tier"),
            upgrade_required=result.get("upgrade_required"),
            reason=result.get("reason")
        )
        
    except Exception as e:
        logger.error(f"Access check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Access check failed: {str(e)}"
        )

@router.post("/process-request", response_model=ServiceResponse, status_code=status.HTTP_200_OK)
async def process_monetized_request(
    request: ServiceRequest,
    monetization_service = Depends(get_monetization_service)
) -> ServiceResponse:
    """Process a service request with monetization"""
    try:
        result = monetization_service.process_service_request(
            request.user_id, 
            request.service_type, 
            request.request_data
        )
        
        return ServiceResponse(
            success=result.get("success", False),
            service_type=result.get("service_type", request.service_type),
            cost=result.get("cost"),
            remaining_credits=result.get("remaining_credits"),
            tracking_id=result.get("tracking_id"),
            payment_id=result.get("payment_id"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Monetized request processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Monetized request processing failed: {str(e)}"
        )

@router.get("/analytics")
async def get_monetization_analytics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    monetization_service = Depends(get_monetization_service)
) -> Dict[str, Any]:
    """Get monetization analytics"""
    try:
        result = monetization_service.get_monetization_analytics(start_date, end_date)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Analytics retrieval failed")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analytics retrieval failed: {str(e)}"
        )

@router.post("/create-plans")
async def create_subscription_plans(
    monetization_service = Depends(get_monetization_service)
) -> Dict[str, Any]:
    """Create subscription plans"""
    try:
        result = monetization_service.create_subscription_plans()
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Plan creation failed")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Plan creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plan creation failed: {str(e)}"
        )

@router.get("/services")
async def get_available_services() -> Dict[str, Any]:
    """Get list of available services"""
    return {
        "success": True,
        "services": [
            {
                "id": "voice_translation",
                "name": "Voice Translation",
                "description": "Translate financial content with voice synthesis"
            },
            {
                "id": "financial_planning",
                "name": "Financial Planning",
                "description": "AI-powered financial planning and budgeting"
            },
            {
                "id": "remittance_analysis",
                "name": "Remittance Analysis",
                "description": "XRPL-based remittance cost analysis"
            },
            {
                "id": "multilingual_voice",
                "name": "Multilingual Voice",
                "description": "Voice responses in multiple languages"
            }
        ]
    }

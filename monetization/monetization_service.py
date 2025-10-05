"""
Monetization service for MoneyLingo agents
"""
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .echo_integration import EchoMonetizationService

class MoneyLingoMonetization:
    """Monetization service for MoneyLingo financial assistant"""
    
    def __init__(self):
        self.logger = logging.getLogger("moneylingo_monetization")
        self.echo_service = EchoMonetizationService()
        
        # Define service pricing
        self.service_pricing = {
            "voice_translation": {
                "free": {"credits": 10, "price": 0, "description": "10 voice translations per month"},
                "basic": {"credits": 100, "price": 9.99, "description": "100 voice translations per month"},
                "premium": {"credits": 500, "price": 29.99, "description": "500 voice translations per month"},
                "enterprise": {"credits": 2000, "price": 99.99, "description": "2000 voice translations per month"}
            },
            "financial_planning": {
                "free": {"credits": 5, "price": 0, "description": "5 financial plans per month"},
                "basic": {"credits": 50, "price": 19.99, "description": "50 financial plans per month"},
                "premium": {"credits": 200, "price": 49.99, "description": "200 financial plans per month"},
                "enterprise": {"credits": 1000, "price": 199.99, "description": "1000 financial plans per month"}
            },
            "remittance_analysis": {
                "free": {"credits": 3, "price": 0, "description": "3 remittance analyses per month"},
                "basic": {"credits": 25, "price": 14.99, "description": "25 remittance analyses per month"},
                "premium": {"credits": 100, "price": 39.99, "description": "100 remittance analyses per month"},
                "enterprise": {"credits": 500, "price": 149.99, "description": "500 remittance analyses per month"}
            },
            "multilingual_voice": {
                "free": {"credits": 5, "price": 0, "description": "5 multilingual voice responses per month"},
                "basic": {"credits": 50, "price": 12.99, "description": "50 multilingual voice responses per month"},
                "premium": {"credits": 250, "price": 34.99, "description": "250 multilingual voice responses per month"},
                "enterprise": {"credits": 1000, "price": 129.99, "description": "1000 multilingual voice responses per month"}
            }
        }
    
    def check_user_access(self, user_id: str, service_type: str) -> Dict[str, Any]:
        """Check if user has access to a service"""
        try:
            # Check authentication
            auth_result = self.echo_service.authenticate_user(user_id, "session_token")
            if not auth_result.get("success"):
                return {"access": False, "reason": "Authentication failed"}
            
            # Check usage limits
            usage_info = self.echo_service.check_usage_limits(user_id, service_type)
            if not usage_info.get("success"):
                return {"access": False, "reason": "Usage limits check failed"}
            
            remaining_credits = usage_info.get("remaining_credits", 0)
            subscription_tier = usage_info.get("subscription_tier", "free")
            
            # Check if user has credits
            if remaining_credits <= 0:
                return {
                    "access": False,
                    "reason": "No credits remaining",
                    "upgrade_required": True,
                    "subscription_tier": subscription_tier
                }
            
            return {
                "access": True,
                "remaining_credits": remaining_credits,
                "subscription_tier": subscription_tier,
                "service_type": service_type
            }
            
        except Exception as e:
            self.logger.error(f"Access check failed: {e}")
            return {"access": False, "reason": str(e)}
    
    def process_service_request(self, user_id: str, service_type: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a service request with monetization"""
        try:
            # Check access
            access_check = self.check_user_access(user_id, service_type)
            if not access_check.get("access"):
                return {
                    "success": False,
                    "error": access_check.get("reason", "Access denied"),
                    "upgrade_required": access_check.get("upgrade_required", False)
                }
            
            # Track usage
            usage_data = {
                "service_type": service_type,
                "request_data": request_data,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }
            
            tracking_result = self.echo_service.track_usage(user_id, service_type, usage_data)
            if not tracking_result.get("success"):
                self.logger.warning(f"Usage tracking failed: {tracking_result.get('error')}")
            
            # Calculate cost
            cost = self.calculate_service_cost(service_type, request_data)
            
            # Process payment if required
            if cost > 0:
                payment_result = self.echo_service.process_payment(
                    user_id=user_id,
                    service_type=service_type,
                    amount=cost,
                    description=f"RealityCheck {service_type} service"
                )
                
                if not payment_result.get("success"):
                    return {
                        "success": False,
                        "error": f"Payment failed: {payment_result.get('error')}"
                    }
            
            return {
                "success": True,
                "service_type": service_type,
                "cost": cost,
                "remaining_credits": access_check.get("remaining_credits", 0) - 1,
                "tracking_id": tracking_result.get("tracking_id"),
                "payment_id": payment_result.get("payment_id") if cost > 0 else None
            }
            
        except Exception as e:
            self.logger.error(f"Service request processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def calculate_service_cost(self, service_type: str, request_data: Dict[str, Any]) -> float:
        """Calculate cost for a service request"""
        pricing = self.service_pricing.get(service_type, {})
        
        # Free tier
        if pricing.get("free", {}).get("price", 0) == 0:
            return 0.0
        
        # Calculate based on request complexity
        base_cost = 0.1  # Base cost per request
        
        # Additional costs based on service type
        if service_type == "voice_translation":
            text_length = len(request_data.get("content", ""))
            if text_length > 1000:
                base_cost += 0.05  # Additional cost for long text
        elif service_type == "financial_planning":
            complexity = len(request_data.get("goals", []))
            base_cost += complexity * 0.02  # Cost per goal
        elif service_type == "remittance_analysis":
            amount = request_data.get("amount", 0)
            if amount > 10000:
                base_cost += 0.1  # Additional cost for large amounts
        
        return round(base_cost, 2)
    
    def get_user_subscription_info(self, user_id: str) -> Dict[str, Any]:
        """Get user's subscription information"""
        try:
            subscription_info = self.echo_service.get_subscription_info(user_id)
            if not subscription_info.get("success"):
                return subscription_info
            
            # Add service-specific information
            subscription_info["available_services"] = list(self.service_pricing.keys())
            subscription_info["pricing_info"] = self.service_pricing
            
            return subscription_info
            
        except Exception as e:
            self.logger.error(f"Subscription info retrieval failed: {e}")
            return {"success": False, "error": str(e)}
    
    def create_subscription_plans(self) -> Dict[str, Any]:
        """Create subscription plans for RealityCheck services"""
        try:
            plans = []
            
            for service_type, pricing in self.service_pricing.items():
                for tier, details in pricing.items():
                    plan_name = f"RealityCheck {service_type.title()} {tier.title()}"
                    features = [
                        f"{details['credits']} {service_type} requests per month",
                        details['description'],
                        "24/7 support" if tier in ["premium", "enterprise"] else "Email support",
                        "API access" if tier in ["premium", "enterprise"] else "Web interface only"
                    ]
                    
                    plan_result = self.echo_service.create_subscription_plan(
                        plan_name=plan_name,
                        price=details['price'],
                        features=features
                    )
                    
                    if plan_result.get("success"):
                        plans.append(plan_result)
            
            return {
                "success": True,
                "plans_created": len(plans),
                "plans": plans
            }
            
        except Exception as e:
            self.logger.error(f"Plan creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_monetization_analytics(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get monetization analytics"""
        try:
            if not start_date:
                start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            analytics = self.echo_service.get_monetization_analytics(start_date, end_date)
            if not analytics.get("success"):
                return analytics
            
            # Add RealityCheck-specific analytics
            analytics["realitycheck_metrics"] = {
                "total_services": len(self.service_pricing),
                "average_revenue_per_user": analytics.get("total_revenue", 0) / max(analytics.get("total_users", 1), 1),
                "conversion_rate_by_service": self._calculate_conversion_rates(),
                "top_performing_services": self._get_top_services()
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Analytics retrieval failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _calculate_conversion_rates(self) -> Dict[str, float]:
        """Calculate conversion rates by service"""
        # Mock data for demo - in production, this would come from analytics
        return {
            "voice_translation": 0.15,
            "financial_planning": 0.25,
            "remittance_analysis": 0.20,
            "multilingual_voice": 0.18
        }
    
    def _get_top_services(self) -> list:
        """Get top performing services"""
        # Mock data for demo - in production, this would come from analytics
        return [
            {"service": "financial_planning", "revenue": 1500.00, "users": 75},
            {"service": "voice_translation", "revenue": 1200.00, "users": 60},
            {"service": "remittance_analysis", "revenue": 800.00, "users": 40},
            {"service": "multilingual_voice", "revenue": 600.00, "users": 30}
        ]

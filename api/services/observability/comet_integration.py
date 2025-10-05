"""
Comet Opik integration for observability, tracing, and evaluation
"""
import os
import logging
from typing import Dict, Any, List
try:
    from comet_llm import log_experiment, log_prompt, log_output
    COMET_AVAILABLE = True
except ImportError:
    COMET_AVAILABLE = False
    def log_experiment(*args, **kwargs):
        pass
    def log_prompt(*args, **kwargs):
        pass
    def log_output(*args, **kwargs):
        pass
import pandas as pd
from datetime import datetime

class CometObserver:
    """Comet Opik integration for agent observability"""
    
    def __init__(self):
        self.logger = logging.getLogger("comet_observer")
        self.api_key = os.getenv("COMET_API_KEY")
        self.workspace = os.getenv("COMET_WORKSPACE")
        
        if not self.api_key:
            self.logger.warning("COMET_API_KEY not found. Observability will be limited.")
        
        self.available = COMET_AVAILABLE and bool(self.api_key)
        
        if self.available:
            self.logger.info("Comet observability enabled")
        else:
            self.logger.warning("Comet observability disabled")
    
    def log_agent_start(self, agent_name: str, input_data: Dict[str, Any]) -> None:
        """Log agent start"""
        if not self.available:
            self.logger.info(f"Agent start: {agent_name}")
            return
        
        try:
            log_experiment(
                name=f"{agent_name}_start",
                data={
                    "agent": agent_name,
                    "input_data": input_data,
                    "timestamp": datetime.now().isoformat(),
                    "event": "agent_start"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log agent start: {e}")
    
    def log_agent_end(self, agent_name: str, result: Dict[str, Any], success: bool) -> None:
        """Log agent completion"""
        if not self.available:
            self.logger.info(f"Agent end: {agent_name} - Success: {success}")
            return
        
        try:
            log_experiment(
                name=f"{agent_name}_end",
                data={
                    "agent": agent_name,
                    "result": result,
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                    "event": "agent_end"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log agent end: {e}")
    
    def log_error(self, agent_name: str, error: str, context: Dict[str, Any] = None) -> None:
        """Log agent error"""
        if not self.available:
            self.logger.error(f"Agent error: {agent_name} - {error}")
            return
        
        try:
            log_experiment(
                name=f"{agent_name}_error",
                data={
                    "agent": agent_name,
                    "error": error,
                    "context": context or {},
                    "timestamp": datetime.now().isoformat(),
                    "event": "agent_error"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log error: {e}")
    
    def log_decision(self, agent_name: str, decision: str, confidence: float, context: Dict[str, Any]) -> None:
        """Log agent decision"""
        if not self.available:
            self.logger.info(f"Agent decision: {agent_name} - {decision}")
            return
        
        try:
            log_experiment(
                name=f"{agent_name}_decision",
                data={
                    "agent": agent_name,
                    "decision": decision,
                    "confidence": confidence,
                    "context": context,
                    "timestamp": datetime.now().isoformat(),
                    "event": "agent_decision"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log decision: {e}")
    
    def log_performance_metrics(self, agent_name: str, metrics: Dict[str, Any]) -> None:
        """Log performance metrics"""
        if not self.available:
            self.logger.info(f"Performance metrics: {agent_name} - {metrics}")
            return
        
        try:
            log_experiment(
                name=f"{agent_name}_metrics",
                data={
                    "agent": agent_name,
                    "metrics": metrics,
                    "timestamp": datetime.now().isoformat(),
                    "event": "performance_metrics"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log metrics: {e}")
    
    def get_observability_status(self) -> Dict[str, Any]:
        """Get observability status"""
        return {
            "comet_available": self.available,
            "api_key_configured": bool(self.api_key),
            "workspace": self.workspace,
            "status": "enabled" if self.available else "disabled"
        }

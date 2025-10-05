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
    
    def log_agent_start(self, agent_name: str, input_data: Dict[str, Any]):
        """Log when an agent starts processing"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Agent {agent_name} started")
            return
            
        try:
            log_experiment(
                name=f"{agent_name}_start",
                data={
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                    "input_size": len(str(input_data)),
                    "input_keys": list(input_data.keys()) if isinstance(input_data, dict) else []
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log agent start: {e}")
    
    def log_agent_end(self, agent_name: str, output_data: Dict[str, Any], success: bool):
        """Log when an agent completes processing"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Agent {agent_name} ended")
            return
            
        try:
            log_experiment(
                name=f"{agent_name}_end",
                data={
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                    "success": success,
                    "output_size": len(str(output_data)),
                    "processing_time": output_data.get("processing_time", 0)
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log agent end: {e}")
    
    def log_decision(self, agent_name: str, decision: str, confidence: float, context: Dict[str, Any]):
        """Log agent decision with confidence score"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Decision: {decision}")
            return
            
        try:
            log_experiment(
                name=f"{agent_name}_decision",
                data={
                    "agent": agent_name,
                    "decision": decision,
                    "confidence": confidence,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log decision: {e}")
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        """Log backend API calls"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - API call: {method} {endpoint}")
            return
            
        try:
            log_experiment(
                name="api_call",
                data={
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": status_code,
                    "response_time": response_time,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log API call: {e}")
    
    def log_error(self, agent_name: str, error: str, context: Dict[str, Any]):
        """Log agent errors"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Error: {error}")
            return
            
        try:
            log_experiment(
                name=f"{agent_name}_error",
                data={
                    "agent": agent_name,
                    "error": error,
                    "context": context,
                    "timestamp": datetime.now().isoformat(),
                    "severity": "error"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log error: {e}")
    
    def evaluate_agent_performance(self, agent_name: str, metrics: Dict[str, Any]):
        """Evaluate agent performance metrics"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Performance evaluation for {agent_name}")
            return
            
        try:
            log_experiment(
                name=f"{agent_name}_evaluation",
                data={
                    "agent": agent_name,
                    "metrics": metrics,
                    "timestamp": datetime.now().isoformat(),
                    "evaluation_type": "performance"
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log evaluation: {e}")
    
    def create_agent_report(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a comprehensive report of all agent activities"""
        if not COMET_AVAILABLE:
            self.logger.info("Comet not available - Creating local report")
            return {"comet_available": False, "agents": len(agent_results)}
            
        try:
            report = {
                "total_agents": len(agent_results),
                "successful_agents": sum(1 for r in agent_results if r.get("success", False)),
                "failed_agents": sum(1 for r in agent_results if not r.get("success", False)),
                "total_processing_time": sum(r.get("processing_time", 0) for r in agent_results),
                "timestamp": datetime.now().isoformat()
            }
            
            log_experiment(
                name="agent_report",
                data=report
            )
            
            return report
        except Exception as e:
            self.logger.warning(f"Failed to create agent report: {e}")
            return {"error": str(e)}

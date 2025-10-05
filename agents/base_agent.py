"""
Base agent class for all RealityCheck agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
try:
    from comet_llm import log_experiment
    COMET_AVAILABLE = True
except ImportError:
    COMET_AVAILABLE = False
    def log_experiment(*args, **kwargs):
        pass

class BaseAgent(ABC):
    """Base class for all agents in the RealityCheck system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    def log_decision(self, decision: str, context: Dict[str, Any], confidence: float = 0.0):
        """Log agent decision to Comet for observability"""
        if not COMET_AVAILABLE:
            self.logger.info(f"Comet not available - Decision: {decision}")
            return
            
        try:
            from datetime import datetime
            log_experiment(
                name=f"{self.name}_decision",
                data={
                    "agent": self.name,
                    "decision": decision,
                    "context": context,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log to Comet: {e}")
    
    def __str__(self):
        return f"{self.name}: {self.description}"

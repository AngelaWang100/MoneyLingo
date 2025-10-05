"""
Dependency injection for API components
"""
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Note: Legacy dependency functions removed to avoid import errors
# These can be re-added when the corresponding modules are properly integrated
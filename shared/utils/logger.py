"""
Structured JSON Logger for Titan Platform
Provides consistent logging across all services and agents
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

class TitanLogger:
    """Structured logger for observability"""
    
    def __init__(self, service_name: str, log_level: str = "INFO"):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Console handler with JSON formatting
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def _log(self, level: str, message: str, **kwargs):
        """Internal method to create structured log entry"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "level": level,
            "message": message,
            **kwargs
        }
        
        log_method = getattr(self.logger, level.lower())
        log_method(json.dumps(log_entry))
    
    def info(self, message: str, **kwargs):
        """Log info level message"""
        self._log("INFO", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message"""
        self._log("ERROR", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message"""
        self._log("WARNING", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message"""
        self._log("DEBUG", message, **kwargs)
    
    def agent_thought(self, agent_name: str, thought: str, **kwargs):
        """Log agent reasoning for observability"""
        self._log("INFO", f"Agent thought: {thought}", 
                 agent=agent_name, 
                 thought_type="reasoning",
                 **kwargs)
    
    def tool_call(self, tool_name: str, params: Dict[str, Any], result: Optional[Any] = None):
        """Log tool invocation"""
        self._log("INFO", f"Tool called: {tool_name}",
                 tool=tool_name,
                 parameters=params,
                 result=str(result)[:200] if result else None)

# Global logger instance
def get_logger(service_name: str) -> TitanLogger:
    """Get or create logger for service"""
    return TitanLogger(service_name)

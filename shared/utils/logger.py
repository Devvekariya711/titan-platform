"""
Structured JSON Logger for Titan Platform
Provides consistent logging across all services and agents with file rotation,
performance tracking, and error aggregation.
"""
import json
import logging
import os
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, Callable
from functools import wraps
from collections import defaultdict

# Global error aggregator
_error_stats = defaultdict(int)
_performance_metrics = defaultdict(list)


class TitanLogger:
    """Enhanced structured logger for observability"""
    
    def __init__(self, service_name: str, log_level: str = "INFO", 
                 enable_file_logging: bool = True):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear any existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Console handler with JSON formatting
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
        
        # File handler with rotation (10MB per file, keep 5 files)
        if enable_file_logging:
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"titan-{datetime.now().strftime('%Y%m%d')}.log")
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(file_handler)
    
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
        
        # Track errors for aggregation
        if level == "ERROR":
            error_type = kwargs.get("error_type", "unknown")
            _error_stats[error_type] += 1
    
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
    
    # NEW: Specialized logging methods for Month 4
    
    def log_agent_decision(self, agent_name: str, ticker: str, decision: str, 
                          confidence: float, reasoning: str):
        """Log agent decision with full context"""
        self._log("INFO", f"Agent decision: {decision}",
                 agent=agent_name,
                 ticker=ticker,
                 decision=decision,
                 confidence=confidence,
                 reasoning=reasoning[:500],  # Limit reasoning length
                 event_type="agent_decision")
    
    def log_tool_execution(self, tool_name: str, duration_ms: float, 
                          success: bool, result_summary: str = ""):
        """Log tool execution with performance metrics"""
        self._log("INFO", f"Tool execution: {tool_name}",
                 tool=tool_name,
                 duration_ms=duration_ms,
                 success=success,
                 result_summary=result_summary[:200],
                 event_type="tool_execution")
        
        # Track performance metrics
        _performance_metrics[tool_name].append(duration_ms)
    
    def log_performance(self, operation: str, duration_ms: float, metadata: Dict[str, Any] = None):
        """Log general performance metrics"""
        self._log("INFO", f"Performance: {operation}",
                 operation=operation,
                 duration_ms=duration_ms,
                 metadata=metadata or {},
                 event_type="performance")
        
        _performance_metrics[operation].append(duration_ms)
    
    @staticmethod
    def get_error_stats() -> Dict[str, int]:
        """Get aggregated error statistics"""
        return dict(_error_stats)
    
    @staticmethod
    def get_performance_stats() -> Dict[str, Dict[str, float]]:
        """Get aggregated performance statistics"""
        stats = {}
        for operation, durations in _performance_metrics.items():
            if durations:
                stats[operation] = {
                    "count": len(durations),
                    "avg_ms": sum(durations) / len(durations),
                    "min_ms": min(durations),
                    "max_ms": max(durations)
                }
        return stats
    
    @staticmethod
    def reset_stats():
        """Reset error and performance statistics"""
        _error_stats.clear()
        _performance_metrics.clear()


# Performance timing decorator
def log_execution_time(logger: TitanLogger, operation_name: str = None):
    """Decorator to log execution time of functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.log_performance(op_name, duration_ms, {"success": True})
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.log_performance(op_name, duration_ms, {"success": False, "error": str(e)})
                raise
        
        return wrapper
    return decorator


# Global logger instance
_loggers: Dict[str, TitanLogger] = {}

def get_logger(service_name: str, log_level: str = "INFO", 
               enable_file_logging: bool = True) -> TitanLogger:
    """Get or create logger for service (singleton pattern)"""
    if service_name not in _loggers:
        _loggers[service_name] = TitanLogger(service_name, log_level, enable_file_logging)
    return _loggers[service_name]

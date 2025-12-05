"""
Structured JSON Logger for Titan Platform
Provides consistent logging across all services and agents with file rotation,
performance tracking, and error aggregation.

Features:
- Daily log rotation (keeps last 5 log files)
- Query/response logging for agent interactions
- Performance metric tracking
- Error aggregation
"""
import json
import logging
import os
import time
import glob
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict, Optional, Callable
from functools import wraps
from collections import defaultdict

# Global error aggregator
_error_stats = defaultdict(int)
_performance_metrics = defaultdict(list)


def cleanup_old_logs(log_dir: str, max_files: int = 5):
    """
    Remove old log files, keeping only the most recent ones.
    
    Args:
        log_dir: Directory containing log files
        max_files: Maximum number of log files to keep (default: 5)
    """
    try:
        log_pattern = os.path.join(log_dir, "titan-*.log*")
        log_files = glob.glob(log_pattern)
        
        # Sort by modification time (newest first)
        log_files.sort(key=os.path.getmtime, reverse=True)
        
        # Delete files beyond max_files limit
        for old_file in log_files[max_files:]:
            try:
                os.remove(old_file)
            except OSError:
                pass  # Ignore errors deleting files
    except Exception:
        pass  # Don't let cleanup errors break logging


class TitanLogger:
    """Enhanced structured logger for observability"""

    def __init__(self, service_name: str, log_level: str = "INFO",
                 enable_file_logging: bool = True, max_log_files: int = 5):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.max_log_files = max_log_files

        # Clear any existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Console handler with JSON formatting
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)

        # File handler with daily rotation (keeps last 5 log files by default)
        if enable_file_logging:
            log_dir = "data/logs"
            os.makedirs(log_dir, exist_ok=True)
            
            # Clean up old log files on initialization
            cleanup_old_logs(log_dir, max_log_files)
            
            log_file = os.path.join(
                log_dir, f"titan-{datetime.now().strftime('%Y%m%d')}.log")

            # Use TimedRotatingFileHandler for daily rotation
            file_handler = TimedRotatingFileHandler(
                log_file,
                when='midnight',
                interval=1,
                backupCount=max_log_files - 1  # Current + backups = max_log_files
            )
            file_handler.setFormatter(logging.Formatter('%(message)s'))
            file_handler.suffix = "%Y%m%d"
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

    def tool_call(self,
                  tool_name: str,
                  params: Dict[str,
                               Any],
                  result: Optional[Any] = None):
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

    def log_performance(self,
                        operation: str,
                        duration_ms: float,
                        metadata: Dict[str,
                                       Any] = None):
        """Log general performance metrics"""
        self._log("INFO", f"Performance: {operation}",
                  operation=operation,
                  duration_ms=duration_ms,
                  metadata=metadata or {},
                  event_type="performance")

        _performance_metrics[operation].append(duration_ms)

    def log_query(self, query: str, user_id: str = "default", 
                  session_id: str = None):
        """
        Log incoming user query for interaction tracking.
        
        Args:
            query: The user's query text
            user_id: User identifier (default: "default")
            session_id: Optional session identifier
        """
        self._log("INFO", "User query received",
                  query=query[:500],  # Limit query length
                  user_id=user_id,
                  session_id=session_id,
                  event_type="user_query")

    def log_response(self, response: str, agent: str = "market_trend_principal",
                     query_id: str = None, duration_ms: float = None):
        """
        Log agent response for interaction tracking.
        
        Args:
            response: The agent's response text
            agent: Name of the responding agent
            query_id: Optional query identifier for correlation
            duration_ms: Optional response time in milliseconds
        """
        self._log("INFO", "Agent response generated",
                  response=response[:1000] if response else "",  # Limit response length
                  agent=agent,
                  query_id=query_id,
                  duration_ms=duration_ms,
                  event_type="agent_response")

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
                logger.log_performance(
                    op_name, duration_ms, {
                        "success": False, "error": str(e)})
                raise

        return wrapper
    return decorator


# Global logger instance
_loggers: Dict[str, TitanLogger] = {}


def get_logger(service_name: str, log_level: str = "INFO",
               enable_file_logging: bool = True) -> TitanLogger:
    """Get or create logger for service (singleton pattern)"""
    if service_name not in _loggers:
        _loggers[service_name] = TitanLogger(
            service_name, log_level, enable_file_logging)
    return _loggers[service_name]

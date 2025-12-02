"""
System Tools - Core System Utilities for Titan Platform
4 tools for memory management and alerting
Month 2 Week 4
"""
from google.adk.tools import FunctionTool
from typing import Dict, Any
from datetime import datetime
import os
import sys

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from shared.utils.logger import get_logger
from services.memory_bank import get_memory_bank

logger = get_logger("system-tools")

# ================== TOOL 1: MEMORY SAVE ==================

def memory_save(user_id: str, key: str, content: str) -> Dict[str, Any]:
    """
    Save data to memory bank
    
    Args:
        user_id: User identifier
        key: Memory key/category
        content: Content to save
    
    Returns:
        Save confirmation
    """
    try:
        memory = get_memory_bank()
        memory.store_user_preference(user_id, key, content)
        
        logger.info(f"Saved to memory: {key}", user_id=user_id, key=key)
        
        return {
            "user_id": user_id,
            "key": key,
            "status": "SAVED",
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Memory save error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to save: {str(e)}",
            "success": False
        }

# ================== TOOL 2: MEMORY RETRIEVE ==================

def memory_retrieve(user_id: str, query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Retrieve data from memory bank
    
    Args:
        user_id: User identifier
        query: Search query
        limit: Max results
    
    Returns:
        Retrieved memories
    """
    try:
        memory = get_memory_bank()
        results = memory.query_user_preferences(user_id, query, limit=limit)
        
        logger.info(f"Retrieved from memory: {query}", user_id=user_id, count=len(results))
        
        return {
            "user_id": user_id,
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Memory retrieve error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to retrieve: {str(e)}",
            "success": False
        }

# ================== TOOL 3: SEND ALERT ==================

def send_alert(message: str, level: str = "INFO") -> Dict[str, Any]:
    """
    Send alert notification
    
    Args:
        message: Alert message
        level: Alert level (INFO/WARNING/CRITICAL)
    
    Returns:
        Alert confirmation
    """
    try:
        logger.info(f"Alert sent: {level}", message=message, level=level)
        
        # In production, would send to notification system
        # (email, Slack, Discord, etc.)
        
        return {
            "message": message,
            "level": level,
            "status": "SENT",
            "timestamp": datetime.now().isoformat(),
            "note": "Simulated alert - Production would use notification service",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Alert error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to send alert: {str(e)}",
            "success": False
        }

# ================== TOOL 4: STRUCTURED LOGGER ==================

def log_event(event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Log structured event for observability
    
    Args:
        event_type: Type of event (agent_thought, tool_call, decision, etc.)
        data: Event data
    
    Returns:
        Log confirmation
    """
    try:
        if event_type == "agent_thought":
            logger.agent_thought(data.get("agent", "unknown"), data.get("thought", ""))
        elif event_type == "tool_call":
            logger.tool_call(data.get("tool", "unknown"), data.get("result", {}))
        else:
            logger.info(f"Event: {event_type}", **data)
        
        return {
            "event_type": event_type,
            "status": "LOGGED",
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Logging error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to log: {str(e)}",
            "success": False
        }

# ================== WRAP AS ADK TOOLS ==================

memory_save_tool = FunctionTool(func=memory_save)
memory_retrieve_tool = FunctionTool(func=memory_retrieve)
send_alert_tool = FunctionTool(func=send_alert)
log_event_tool = FunctionTool(func=log_event)

# Export
__all__ = [
    'memory_save_tool', 'memory_retrieve_tool', 'send_alert_tool', 'log_event_tool',
    'memory_save', 'memory_retrieve', 'send_alert', 'log_event'
]

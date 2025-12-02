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

# ================== TOOL 2.1: GET USER CONTEXT (MONTH 3) ==================

def get_user_context(user_id: str) -> Dict[str, Any]:
    """
    Get comprehensive user profile including risk tolerance and trading style
    
    Args:
        user_id: User identifier
    
    Returns:
        Complete user context
    """
    try:
        memory = get_memory_bank()
        context = memory.get_user_context(user_id)
        
        logger.info(f"Retrieved user context", user_id=user_id,
                   has_risk_profile=context.get("risk_profile") is not None)
        
        return {
            "user_id": user_id,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Get user context error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to get context: {str(e)}",
            "success": False
        }

# ================== TOOL 2.2: STORE AGENT OUTPUT (MONTH 3) ==================

def store_agent_output(agent_name: str, ticker: str, output: str, confidence: float) -> Dict[str, Any]:
    """
    Store agent output for accuracy tracking
    
    Args:
        agent_name: Name of the agent
        ticker: Stock ticker
        output: Analysis output
        confidence: Confidence score (0-100)
    
    Returns:
        Storage confirmation
    """
    try:
        memory = get_memory_bank()
        memory.store_agent_output(agent_name, ticker, output, confidence)
        
        logger.info(f"Stored agent output", agent_name=agent_name, ticker=ticker)
        
        return {
            "agent_name": agent_name,
            "ticker": ticker,
            "confidence": confidence,
            "status": "STORED",
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Store agent output error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to store output: {str(e)}",
            "success": False
        }

# ================== TOOL 2.3: GET SIMILAR ANALYSIS (MONTH 3) ==================

def get_similar_analysis(ticker: str, days_back: int = 30) -> Dict[str, Any]:
    """
    Retrieve similar past analysis for learning
    
    Args:
        ticker: Stock ticker
        days_back: Number of days to look back
    
    Returns:
        Similar analyses
    """
    try:
        memory = get_memory_bank()
        results = memory.retrieve_similar_analysis(ticker, timeframe_days=days_back)
        
        logger.info(f"Retrieved similar analysis", ticker=ticker, days_back=days_back)
        
        return {
            "ticker": ticker,
            "days_back": days_back,
            "results": results,
            "count": len(results.get("documents", [[]])[0]) if results else 0,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Get similar analysis error: {str(e)}", error=str(e))
        return {
            "error": f"Failed to get similar analysis: {str(e)}",
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
get_user_context_tool = FunctionTool(func=get_user_context)  # Month 3
store_agent_output_tool = FunctionTool(func=store_agent_output)  # Month 3
get_similar_analysis_tool = FunctionTool(func=get_similar_analysis)  # Month 3
send_alert_tool = FunctionTool(func=send_alert)
log_event_tool = FunctionTool(func=log_event)

# Export
__all__ = [
    'memory_save_tool', 'memory_retrieve_tool', 'send_alert_tool', 'log_event_tool',
    'get_user_context_tool', 'store_agent_output_tool', 'get_similar_analysis_tool',  # Month 3
    'memory_save', 'memory_retrieve', 'send_alert', 'log_event',
    'get_user_context', 'store_agent_output', 'get_similar_analysis'  # Month 3
]

"""
Agent Platform - Root Agent Export
ADK requires agent.py with root_agent variable for web UI
"""
from agent_platform.agents.root.market_trend_principal import market_trend_principal

# Export as root_agent for ADK web compatibility
root_agent = market_trend_principal

__all__ = ['root_agent', 'market_trend_principal']

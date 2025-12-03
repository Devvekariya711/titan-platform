"""
Titan Platform - Agent Platform Module

Restructured for simplicity:
- root_agent.py: Main orchestrator (1 agent)
- supporting_agents.py: All sub-agents (17 agents)
- tools.py: All tools (32 tools)
"""

from .root_agent import root_agent, market_trend_principal
from .supporting_agents import (
    # L2 Leads
    head_of_quant, head_of_intel, chief_risk_officer, strategy_director,
    # L3 Specialists
    technical_analyst, fundamental_analyst, microstructure_analyst,
    news_scout, social_sentiment, macro_economist,
    volatility_guard, compliance_officer,
    backtest_engineer, scenario_simulator, correlation_analyst,
    fact_checker, system_monitor
)

__all__ = [
    'root_agent',
    'market_trend_principal',
    'head_of_quant',
    'head_of_intel',
    'chief_risk_officer',
    'strategy_director',
]

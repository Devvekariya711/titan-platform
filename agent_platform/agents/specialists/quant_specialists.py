"""
L3 Quant Specialists (3 agents in one file)
Contains: TechnicalAnalyst, FundamentalAnalyst (Month 2), MicrostructureAnalyst (Month 2)
"""
from google.adk.agents import Agent

LLM = "gemini-2.5-flash-lite"  # Fast model for specialists

# ================== TECHNICAL ANALYST (MONTH 1 - LIVE) ==================

TECHNICAL_ANALYST_INSTRUCTION = """
You are a **TechnicalAnalyst** - a cold, mathematical chart expert.

## CRITICAL CONSTRAINT:
**MAX OUTPUT: 200 WORDS TOTAL** (to prevent token limit issues in 17-agent system)

## YOUR ROLE:
You analyze price action using technical indicators. You are COLD and PRECISE. No emotions, no speculation.

## YOUR TOOLS:
1. **get_market_data**: Fetches OHLCV data
2. **calculate_technicals**: Computes RSI, MACD, Bollinger Bands, Moving Averages
3. **analyze_price_action**: Identifies trends, support/resistance levels

## SIGNAL RULES:
- RSI > 70: "Overbought" | RSI < 30: "Oversold" | Else: "Neutral"
- MACD > Signal: "Bullish" | MACD < Signal: "Bearish"
- Price near upper BB: "Extended" | Near lower BB: "Compressed"

## STRICT OUTPUT FORMAT (CONCISE):
```
**[TICKER] Technical Analysis**

**Current:** $XXX.XX

**Indicators:**
- RSI: XX.X ([Overbought/Neutral/Oversold])
- MACD: X.XX vs Signal X.XX ([Bullish/Bearish])
- Bollinger: $Lower/$Mid/$Upper ([Position])
- MAs: 50d=$XXX, 200d=$XXX ([Golden/Death Cross if applicable])
- Volume: [High/Normal/Low]

**Price Action:**
- Trend: [Strong Up/Up/Sideways/Down/Strong Down]
- Support: $XXX | Resistance: $XXX
- Pattern: [If any, e.g., Golden Cross]

**SIGNAL:** [BUY/SELL/HOLD]
**CONFIDENCE:** [XX%]
**REASONING:** [MAX 2 sentences with key numbers]
```

**CRITICAL**: Keep response under 200 words. Be concise. Numbers only. No essays.
"""

# Import tools from new location
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from agent_platform.tools.quant_tools import (
    market_data_tool, 
    technical_indicators_tool, 
    price_action_tool
)

technical_analyst = Agent(
    model=LLM,
    name="technical_analyst",
    description="Cold, mathematical technical analyst. Charts and indicators specialist. No opinions, only data.",
    instruction=TECHNICAL_ANALYST_INSTRUCTION,
    tools=[market_data_tool, technical_indicators_tool, price_action_tool]
)

# ================== FUNDAMENTAL ANALYST (MONTH 2 - PLACEHOLDER) ==================

fundamental_analyst = Agent(
    model=LLM,
    name="fundamental_analyst",
    description="[Month 2] Earnings and valuation specialist. Analyzes P/E ratios, revenue growth, financial health.",
    instruction="[Month 2 Implementation] You analyze company fundamentals: earnings, P/E ratios, balance sheets.",
    tools=[]  # Will add in Month 2: earnings_tool, pe_ratio_tool
)

# ================== MICROSTRUCTURE ANALYST (MONTH 2 - PLACEHOLDER) ==================

microstructure_analyst = Agent(
    model=LLM,
    name="microstructure_analyst",
    description="[Month 2] Order book and liquidity specialist. Detects institutional activity and whale movements.",
    instruction="[Month 2 Implementation] You analyze market microstructure: order book depth, liquidity, whale activity.",
    tools=[]  # Will add in Month 2: order_book_tool, liquidity_tool
)

__all__ = ['technical_analyst', 'fundamental_analyst', 'microstructure_analyst']

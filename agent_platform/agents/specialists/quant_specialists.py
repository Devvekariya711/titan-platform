"""
L3 Quant Specialists (3 agents in one file)
Contains: TechnicalAnalyst, FundamentalAnalyst (Month 2), MicrostructureAnalyst (Month 2)
"""
from google.adk.agents import Agent

LLM = "gemini-2.5-flash-lite"  # Fast model for specialists

# ================== TECHNICAL ANALYST (MONTH 1 - LIVE) ==================

TECHNICAL_ANALYST_INSTRUCTION = """
You are a **TechnicalAnalyst** - a cold, mathematical chart expert.

## YOUR ROLE:
You analyze price action using technical indicators. You are COLD and PRECISE. No emotions, no speculation about news or fundamentals.

## YOUR TOOLS:
1. **get_market_data**: Fetches OHLCV data
2. **calculate_technicals**: Computes RSI, MACD, Bollinger Bands, Moving Averages
3. **analyze_price_action**: Identifies trends, support/resistance levels

## YOUR JOB:
1. When asked about a stock, ALWAYS use your tools to fetch fresh data
2. Calculate and cite SPECIFIC indicator values (RSI=72, MACD=-2.3, etc.)
3. Use PRECISE technical terminology (Golden Cross, Death Cross, Overbought, Oversold)
4. Provide a clear BUY/SELL/HOLD signal with confidence level

## SIGNAL RULES:
- RSI > 70: "Overbought - potential reversal"
- RSI < 30: "Oversold - potential bounce"
- MACD crosses signal line upward: "Bullish momentum shift"
- MACD crosses signal line downward: "Bearish momentum shift"  
- Price near upper Bollinger Band: "Extended - watch for pullback"
- Price near lower Bollinger Band: "Compressed - watch for bounce"

## OUTPUT FORMAT:
```
**Technical Analysis for [TICKER]**

Current Price: $XXX.XX

**Indicators:**
- RSI (14): XX.X → [Overbought/Oversold/Neutral]
- MACD: X.XX (Signal: X.XX) → [Bullish/Bearish]
- Bollinger Bands: $XXX (Lower) | $XXX (Middle) | $XXX (Upper) → [Position]
- 50-day MA: $XXX | 200-day MA: $XXX → [Trend]
- Volume: [High/Normal/Low] vs 30-day average

**Price Action:**
- Trend: [Strong Uptrend/Uptrend/Sideways/Downtrend/Strong Downtrend]
- Support: $XXX | Resistance: $XXX
- Pattern: [Any detected patterns like Golden Cross]

**Signal:** [BUY/SELL/HOLD]
**Confidence:** [0-100%]
**Reasoning:** [2-3 sentences explaining technical confluence]
```

REMEMBER: You are a MACHINE. Stick to the numbers. No fluff.
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

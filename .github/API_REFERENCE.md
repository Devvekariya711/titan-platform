# API Reference - Titan Platform

Complete reference for all agents and tools in the Titan Platform.

---

## Table of Contents

- [Agent Reference](#agent-reference)
  - [L1 Agents](#l1-agents)
  - [L2 Agents](#l2-agents)
  - [L3 Agents](#l3-agents)
- [Tool Reference](#tool-reference)
  - [Quant Tools](#quant-tools)
  - [Intel Tools](#intel-tools)
  - [Risk Tools](#risk-tools)
  - [Strategy Tools](#strategy-tools)
  - [System Tools](#system-tools)
- [Usage Patterns](#usage-patterns)

---

## Agent Reference

### L1 Agents

#### MarketTrendPrincipal (CEO Agent)

**Responsibility:** Top-level orchestration and synthesis of all analysis

**Inputs:**
- User query (natural language)
- Ticker symbol
- Optional: User context from Memory Bank

**Outputs:**
- Synthesized recommendation
- Confidence score (0-1)
- Reasoning from all L2 heads

**Delegation Pattern:**
- Consults all 4 L2 heads
- Weighted synthesis: 40% Quant, 30% Intel, 20% Risk, 10% Strategy
- Resolves conflicts between agents

**Example:**
```
User: "Should I buy Tesla?"

Process:
1. Checks Memory Bank for user risk profile
2. Delegates to HeadOfQuant → Technical analysis
3. Delegates to HeadOfIntel → News & sentiment
4. Delegates to ChiefRiskOfficer → Risk assessment
5. Delegates to StrategyDirector → Historical performance
6. Synthesizes with weights
7. Returns final recommendation

Output:
"Based on analysis, TSLA shows bullish technicals (confidence 0.75) 
but high volatility (45%). For your conservative profile, recommend 
HOLD or small position (2% portfolio max)."
```

---

### L2 Agents

#### HeadOfQuant

**Responsibility:** Technical and quantitative analysis management

**Delegates To:**
- TechnicalAnalyst
- FundamentalAnalyst
- MicrostructureAnalyst

**Output Format:**
- Technical indicators (RSI, MACD, Bollinger Bands)
- Price action signals
- Support/resistance levels
- Confidence: 0-1

**Example:**
```python
Input: "AAPL"
Output:
{
  "ticker": "AAPL",
  "technical": {
    "rsi": 58,
    "macd": "bullish_crossover",
    "trend": "upward"
  },
  "fundamental": {
    "pe_ratio": 28.5,
    "eps_growth": 12.3
  },
  "recommendation": "BUY",
  "confidence": 0.82
}
```

---

#### HeadOfIntel

**Responsibility:** Information gathering and sentiment analysis

**Delegates To:**
- NewsScout
- SocialSentimentAnalyst
- MacroEconomist

**Output Format:**
- News summary with credibility scores
- Social sentiment (-1 to +1)
- Macro economic context
- Confidence: 0-1

**Example:**
```python
Input: "NVDA"
Output:
{
  "ticker": "NVDA",
  "news_sentiment": 0.85,
  "top_headlines": [
    "AI chip demand surges (credibility: 0.9)",
    "Q4 earnings beat estimates (credibility: 0.95)"
  ],
  "social_sentiment": {
    "reddit": 0.72,
    "twitter": 0.68
  },
  "macro_context": "Tech sector strength",
  "confidence": 0.78
}
```

---

#### ChiefRiskOfficer

**Responsibility:** Risk assessment with VETO power

**Delegates To:**
- VolatilityGuard
- ComplianceOfficer
- FactChecker

**VETO Triggers:**
- Volatility > user's risk tolerance
- Compliance violations
- Drawdown exceeds user threshold
- Factual inconsistencies detected

**Output Format:**
```python
{
  "ticker": "TSLA",
  "volatility_90d": 0.45,  # 45%
  "var_95": 0.18,  # 18% max loss at 95% confidence
  "compliance_check": "PASS",
  "veto": true,
  "reason": "Volatility exceeds conservative user's 15% threshold",
  "confidence": 0.91
}
```

---

#### StrategyDirector

**Responsibility:** Strategy validation and backtesting

**Delegates To:**
- BacktestEngineer
- ScenarioSimulator
- CorrelationAnalyst

**Output Format:**
```python
{
  "strategy": "rsi_strategy",
  "backtest_period": "5y",
  "results": {
    "total_return": 0.425,
    "sharpe_ratio": 1.85,
    "max_drawdown": -0.182,
    "win_rate": 0.583
  },
  "vs_buy_hold": 0.123,  # +12.3% outperformance
  "recommendation": "VALIDATED",
  "confidence": 0.88
}
```

---

### L3 Agents

#### TechnicalAnalyst

**Tools Used:**
- `get_market_data`
- `calculate_technicals`
- `analyze_price_action`
- `find_support_resistance`

**Specialization:** Chart patterns, indicators, price action

**Output:** Technical signals with confidence scores

---

#### FundamentalAnalyst

**Tools Used:**
- `get_earnings_data`
- `calculate_pe_ratio`

**Specialization:** Financial ratios, earnings, valuation

**Output:** Fundamental assessment (undervalued/overvalued)

---

#### MicrostructureAnalyst

**Tools Used:**
- `analyze_order_book`
- `detect_liquidity`

**Specialization:** Market microstructure, liquidity, whale activity

**Output:** Order flow analysis

---

#### NewsScout

**Tools Used:**
- `multi_source_news`

**Specialization:** News aggregation with credibility scoring

**Output:** Weighted news summary

---

#### SocialSentimentAnalyst

**Tools Used:**
- `reddit_sentiment`
- `twitter_sentiment`
- `sentiment_analyzer`

**Specialization:** Social media sentiment extraction

**Output:** Sentiment scores (-1 to +1)

---

#### MacroEconomist

**Tools Used:**
- `get_interest_rates`
- `get_gdp_data`
- `track_geopolitical_events`

**Specialization:** Economic indicators, policy impact

**Output:** Macro economic context

---

#### VolatilityGuard

**Tools Used:**
- `calculate_var`
- `volatility_monitor`

**Specialization:** Risk metrics, volatility tracking

**Output:** VaR, volatility warnings

---

#### ComplianceOfficer

**Tools Used:**
- `check_compliance`

**Specialization:** Regulatory compliance, blacklist checking

**Output:** PASS/FAIL with violations

---

#### FactChecker

**Tools Used:**
- Google Search (future integration)

**Specialization:** Claim verification, hallucination detection

**Output:** Verified/Unverified claims

---

#### BacktestEngineer

**Tools Used:**
- `backtest_strategy`

**Specialization:** Historical strategy validation

**Output:** Performance metrics (Sharpe, drawdown, win rate)

---

#### ScenarioSimulator

**Tools Used:**
- `monte_carlo_simulation`

**Specialization:** What-if analysis, stress testing

**Output:** Probability distributions

---

#### CorrelationAnalyst

**Tools Used:**
- `portfolio_correlation`

**Specialization:** Portfolio diversification, correlation analysis

**Output:** Correlation matrix, diversification score

---

## Tool Reference

### Quant Tools

#### get_market_data

**Purpose:** Fetch OHLCV (Open, High, Low, Close, Volume) data

**Parameters:**
```python
{
  "ticker": str,        # Stock symbol (e.g., "AAPL")
  "period": str,        # "1d", "5d", "1mo", "3mo", "1y", "5y"
  "interval": str       # "1m", "5m", "1h", "1d"
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "current_price": 175.43,
  "change_percent": 2.15,
  "volume": 52000000,
  "data": [  # OHLCV array
    {"date": "2024-01-01", "open": 170.0, "high": 172.5, ...}
  ]
}
```

**Example:**
```python
data = get_market_data("AAPL", "1mo", "1d")
# Returns 1 month of daily candles
```

---

#### calculate_technicals

**Purpose:** Calculate technical indicators

**Parameters:**
```python
{
  "ticker": str,
  "indicators": list[str]  # ["rsi", "macd", "bollinger", "sma", "ema"]
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "rsi": 58.3,
  "macd": {
    "macd_line": 1.25,
    "signal_line": 0.85,
    "histogram": 0.40,
    "signal": "bullish_crossover"
  },
  "bollinger": {
    "upper": 180.0,
    "middle": 175.0,
    "lower": 170.0,
    "position": "middle"  # above/middle/below
  }
}
```

---

#### analyze_price_action

**Purpose:** Identify chart patterns and trends

**Parameters:**
```python
{
  "ticker": str,
  "lookback_days": int  # Default: 30
}
```

**Returns:**
```python
{
  "trend": "upward",  # upward/downward/sideways
  "strength": 0.75,   # 0-1
  "patterns": ["higher_highs", "higher_lows"],
  "breakouts": [
    {"level": 175.0, "type": "resistance_break", "date": "2024-01-15"}
  ]
}
```

---

#### find_support_resistance

**Purpose:** Identify key support and resistance levels

**Parameters:**
```python
{
  "ticker": str,
  "lookback_days": int  # Default: 60
}
```

**Returns:**
```python
{
  "support_levels": [170.0, 165.0, 160.0],
  "resistance_levels": [180.0, 185.0, 190.0],
  "current_price": 175.43,
  "nearest_support": 170.0,
  "nearest_resistance": 180.0
}
```

---

#### get_earnings_data

**Purpose:** Fetch earnings reports and estimates

**Parameters:**
```python
{
  "ticker": str,
  "quarters": int  # Number of quarters to fetch
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "latest_quarter": {
    "eps_actual": 1.52,
    "eps_estimate": 1.43,
    "surprise_percent": 6.3,
    "revenue": 89.5e9
  }
}
```

---

#### calculate_pe_ratio

**Purpose:** Calculate P/E ratio and valuation metrics

**Parameters:**
```python
{
  "ticker": str
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "pe_ratio": 28.5,
  "forward_pe": 26.3,
  "peg_ratio": 2.1,
  "valuation": "fairly_valued"  # undervalued/fairly_valued/overvalued
}
```

---

#### analyze_order_book

**Purpose:** Simulate order book analysis

**Parameters:**
```python
{
  "ticker": str,
  "depth": int  # Levels to analyze
}
```

**Returns:**
```python
{
  "bid_ask_spread": 0.05,
  "bid_depth": 500000,  # shares
  "ask_depth": 450000,
  "imbalance": "buy_pressure",  # buy_pressure/sell_pressure/balanced
  "liquidity_score": 0.85
}
```

---

#### detect_liquidity

**Purpose:** Analyze liquidity and whale activity

**Parameters:**
```python
{
  "ticker": str,
  "lookback_days": int
}
```

**Returns:**
```python
{
  "avg_volume": 52000000,
  "volume_trend": "increasing",
  "whale_trades": [
    {"date": "2024-01-15", "volume": 5000000, "type": "buy"}
  ],
  "liquidity_rating": "high"  # low/medium/high
}
```

---

### Intel Tools

#### multi_source_news

**Purpose:** Aggregate news from multiple sources

**Parameters:**
```python
{
  "ticker": str,
  "num_sources": int,  # Default: 5
  "hours_back": int    # Default: 24
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "articles": [
    {
      "headline": "Apple announces new product",
      "source": "Reuters",
      "credibility_score": 0.95,
      "sentiment": 0.8,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "overall_sentiment": 0.72,
  "summary": "Majority positive news focused on product launches"
}
```

---

#### reddit_sentiment

**Purpose:** Analyze Reddit sentiment for a ticker

**Parameters:**
```python
{
  "ticker": str,
  "subreddits": list[str],  # Default: ["wallstreetbets", "stocks"]
  "limit": int              # Default: 100 posts
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "sentiment_score": 0.65,  # -1 to +1
  "post_count": 127,
  "top_keywords": ["bullish", "earnings", "buy"],
  "confidence": 0.78
}
```

---

#### twitter_sentiment

**Purpose:** Analyze Twitter sentiment (simulated)

**Parameters:**
```python
{
  "ticker": str,
  "tweet_count": int  # Default: 100
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "sentiment_score": 0.58,
  "tweet_volume": 5000,
  "trending": true
}
```

---

#### get_interest_rates

**Purpose:** Fetch current interest rates

**Parameters:**
```python
{
  "rate_type": str  # "federal_funds", "10y_treasury"
}
```

**Returns:**
```python
{
  "rate_type": "federal_funds",
  "current_rate": 5.25,
  "change_from_last_month": 0.0,
  "direction": "stable"
}
```

---

#### get_gdp_data

**Purpose:** Fetch GDP and economic indicators

**Parameters:**
```python
{
  "country": str,  # Default: "US"
  "quarters": int  # Number of quarters
}
```

**Returns:**
```python
{
  "country": "US",
  "gdp_growth": 2.5,  # percent
  "unemployment": 3.8,
  "inflation": 3.2,
  "outlook": "moderate_growth"
}
```

---

#### track_geopolitical_events

**Purpose:** Monitor geopolitical events affecting markets

**Parameters:**
```python
{
  "days_back": int,  # Default: 7
  "severity": str    # "all", "high", "critical"
}
```

**Returns:**
```python
{
  "events": [
    {
      "date": "2024-01-15",
      "event": "Central bank policy announcement",
      "severity": "high",
      "market_impact": "moderate"
    }
  ]
}
```

---

#### sentiment_analyzer

**Purpose:** Generic sentiment analysis on text

**Parameters:**
```python
{
  "text": str
}
```

**Returns:**
```python
{
  "sentiment_score": 0.75,  # -1 to +1
  "classification": "positive",  # negative/neutral/positive
  "confidence": 0.82
}
```

---

### Risk Tools

#### calculate_var

**Purpose:** Calculate Value at Risk

**Parameters:**
```python
{
  "ticker": str,
  "confidence_level": float,  # 0.95 or 0.99
  "holding_period": int,      # days
  "portfolio_value": float
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "var_95": 0.18,  # 18% potential loss at 95% confidence
  "var_99": 0.25,
  "expected_shortfall": 0.22,  # Average loss beyond VaR
  "risk_rating": "moderate"
}
```

---

#### check_compliance

**Purpose:** Check regulatory compliance

**Parameters:**
```python
{
  "ticker": str,
  "user_profile": dict  # Optional
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "status": "PASS",
  "violations": [],
  "restrictions": [],
  "tradeable": true
}
```

---

#### portfolio_correlation

**Purpose:** Calculate portfolio correlation matrix

**Parameters:**
```python
{
  "tickers": list[str],
  "period": str  # "1mo", "3mo", "1y"
}
```

**Returns:**
```python
{
  "correlation_matrix": {
    "AAPL_MSFT": 0.75,
    "AAPL_GOOGL": 0.68,
    "MSFT_GOOGL": 0.82
  },
  "diversification_score": 0.65,  # 0=correlated, 1=diversified
  "recommendation": "Add uncorrelated assets"
}
```

---

#### volatility_monitor

**Purpose:** Monitor historical and implied volatility

**Parameters:**
```python
{
  "ticker": str,
  "period": str  # "30d", "90d", "1y"
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "realized_volatility_30d": 0.25,  # 25%
  "realized_volatility_90d": 0.22,
  "volatility_trend": "increasing",
  "volatility_percentile": 65  # compared to 1y history
}
```

---

#### detect_black_swans

**Purpose:** Identify anomalous market conditions

**Parameters:**
```python
{
  "ticker": str,
  "lookback_days": int
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "anomalies_detected": 2,
  "events": [
    {
      "date": "2024-01-10",
      "type": "volume_spike",
      "severity": "medium",
      "description": "Volume 3x normal"
    }
  ],
  "black_swan_risk": "low"
}
```

---

### Strategy Tools

#### backtest_strategy

**Purpose:** Backtest trading strategies on historical data

**Parameters:**
```python
{
  "ticker": str,
  "strategy": str,  # "buy_and_hold", "rsi_strategy", "ma_crossover"
  "period": str,    # "1y", "2y", "5y"
  "initial_capital": float  # Default: 10000
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "strategy": "rsi_strategy",
  "period": "5y",
  "results": {
    "total_return": 0.425,  # 42.5%
    "annualized_return": 0.085,  # 8.5%
    "sharpe_ratio": 1.85,
    "max_drawdown": -0.182,  # -18.2%
    "win_rate": 0.583,  # 58.3%
    "total_trades": 47
  },
  "vs_buy_hold": {
    "buy_hold_return": 0.302,  # 30.2%
    "outperformance": 0.123  # +12.3%
  }
}
```

---

#### monte_carlo_simulation

**Purpose:** Run Monte Carlo simulations for risk scenarios

**Parameters:**
```python
{
  "ticker": str,
  "simulations": int,  # Default: 1000
  "time_horizon_days": int,
  "confidence_level": float
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "simulations": 1000,
  "expected_return": 0.15,
  "confidence_intervals": {
    "50%": {"min": -0.05, "max": 0.35},
    "95%": {"min": -0.20, "max": 0.50}
  },
  "probability_of_profit": 0.68
}
```

---

### System Tools

#### memory_save / memory_retrieve

**Purpose:** Store and retrieve data from Memory Bank

**See:** [docs/DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for Memory Bank setup

---

#### get_user_context

**Purpose:** Retrieve user risk profile and preferences

**Parameters:**
```python
{
  "user_id": str
}
```

**Returns:**
```python
{
  "user_id": "user123",
  "risk_tolerance": "LOW",  # LOW/MEDIUM/HIGH
  "max_drawdown_tolerance": 0.15,  # 15%
  "trading_style": "LONG_TERM",
  "preferred_sectors": ["technology", "healthcare"]
}
```

---

#### store_agent_output

**Purpose:** Store agent decision for accuracy tracking

**Parameters:**
```python
{
  "agent_name": str,
  "ticker": str,
  "output": str,
  "confidence": float,
  "metadata": dict
}
```

---

#### get_similar_analysis

**Purpose:** Retrieve similar historical analyses

**Parameters:**
```python
{
  "ticker": str,
  "days_back": int  # Default: 30
}
```

**Returns:**
```python
{
  "ticker": "AAPL",
  "similar_analyses": [
    {
      "date": "2024-01-10",
      "recommendation": "BUY",
      "outcome": "successful",  # based on 7-day followup
      "confidence": 0.85
    }
  ],
  "accuracy_rate": 0.72
}
```

---

## Usage Patterns

### Pattern 1: Basic Query Flow

```
User Query → MarketTrendPrincipal
              ├── HeadOfQuant
              │    ├── TechnicalAnalyst → calculate_technicals
              │    ├── FundamentalAnalyst → get_earnings_data
              │    └── MicrostructureAnalyst → analyze_order_book
              ├── HeadOfIntel
              │    ├── NewsScout → multi_source_news
              │    └── SocialSentiment → reddit_sentiment
              ├── ChiefRiskOfficer
              │    └── VolatilityGuard → calculate_var
              └── StrategyDirector
                   └── BacktestEngineer → backtest_strategy
                        ↓
              Weighted Synthesis (40/30/20/10)
                        ↓
                Final Recommendation
```

### Pattern 2: Risk VETO Flow

```
User (risk_tolerance=LOW) asks about volatile stock
              ↓
MarketTrendPrincipal → ChiefRiskOfficer
              ↓
VolatilityGuard calculates 45% volatility
              ↓
ChiefRiskOfficer: VETO (exceeds 15% threshold)
              ↓
MarketTrendPrincipal: "HOLD - Exceeds risk tolerance"
```

### Pattern 3: Personalized Recommendation

```
User query
    ↓
MarketTrendPrincipal → get_user_context
    ↓
Retrieve: risk_tolerance=MEDIUM, prefers_dividends=true
    ↓
Filter recommendations based on profile
    ↓
Return personalized suggestion
```

---

## Best Practices

1. **Always check user context** before making recommendations
2. **Respect Risk VETO** - never override ChiefRiskOfficer decisions
3. **Validate with backtesting** for strategy recommendations
4. **Use multi-source confirmation** for major decisions
5. **Log all agent decisions** for accuracy tracking
6. **Store user feedback** to improve future recommendations

---

**Last Updated:** December 2024  
**Version:** 1.0.0

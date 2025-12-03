# Testing Guide - Titan Platform

Comprehensive guide for testing individual agents, tools, and the full system.

---

## Table of Contents

- [Setup](#setup)
- [Testing Individual Agents](#testing-individual-agents)
- [Testing Tools](#testing-tools)
- [Testing Full Hierarchy](#testing-full-hierarchy)
- [Testing with Real Data](#testing-with-real-data)
- [Example Test Scenarios](#example-test-scenarios)
- [Troubleshooting](#troubleshooting)

---

## Setup

### Prerequisites

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify dependencies
pip list | grep -E "google-adk|chromadb|pandas|yfinance"

# Check environment variables
python -c "import os; print('GOOGLE_API_KEY:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'MISSING')"
```

### Test Data Preparation

```bash
# Download historical data for common test tickers
python -c "
from services.backtest_engine.data_loader import DataLoader
dl = DataLoader()
for ticker in ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']:
    print(f'Downloading {ticker}...')
    dl.download_historical_data(ticker, '2019-01-01', '2024-12-01')
"
```

---

## Testing Individual Agents

### L1 Agent (MarketTrendPrincipal)

**Test Method:** Direct query through Google ADK web interface

```bash
# Start ADK web server
cd agent_platform
adk web
```

**Test Query:**
```
"What's your analysis of Apple (AAPL)?"
```

**Expected Behavior:**
- Agent delegates to all 4 L2 heads
- Synthesis includes weighted contributions
- Response within 5 seconds
- Confidence score provided

**Validation Checklist:**
- [ ] All L2 heads consulted
- [ ] Weighted synthesis applied (40/30/20/10)
- [ ] User context checked (if user_id provided)
- [ ] Final recommendation clear and actionable

---

### L2 Agents

#### Testing HeadOfQuant

**Test Query:**
```
"Give me technical analysis for Microsoft"
```

**Expected Output:**
```
Technical Indicators:
- RSI: 58.3 (neutral)
- MACD: Bullish crossover
- Bollinger: Middle band
- Trend: Upward (strength: 0.75)

Fundamental Metrics:
- P/E Ratio: 32.5
- Forward P/E: 28.3
- Valuation: Fairly valued

Recommendation: BUY
Confidence: 0.82
```

**Validation:**
- [ ] All 3 L3 specialists consulted (Technical, Fundamental, Microstructure)
- [ ] Real data used (not simulated)
- [ ] Indicators calculated correctly
- [ ] Response within 200 words

---

#### Testing HeadOfIntel

**Test Query:**
```
"What's the news sentiment on Tesla?"
```

**Expected Output:**
```
News Sentiment: 0.65 (Positive)
Sources: 5 articles from Reuters (0.95), Bloomberg (0.92)...

Social Sentiment:
- Reddit: 0.58
- Twitter: 0.62

Macro Context: EV sector growth, rates stable

Confidence: 0.78
```

**Validation:**
- [ ] News aggregated from multiple sources
- [ ] Credibility scores provided
- [ ] Social sentiment analyzed
- [ ] Macro context included

---

#### Testing ChiefRiskOfficer (VETO)

**Test Case 1: VETO should trigger**

```
User Profile: risk_tolerance=LOW, max_drawdown=15%
Query: "Should I buy Tesla?"
```

**Expected:**
```
⚠️ RISK ASSESSMENT:
- Volatility (90d): 45%
- VaR(95%): 22%
- Max Drawdown: Could exceed 30%

❌ VETO ISSUED
Reason: Volatility exceeds your 15% tolerance
Recommendation: HOLD or reduce to 2% of portfolio max
```

**Test Case 2: VETO should NOT trigger**

```
User Profile: risk_tolerance=HIGH
Query: "Should I buy Apple?"
```

**Expected:**
```
✅ RISK ASSESSMENT:
- Volatility (90d): 18%
- VaR(95%): 8%
- Compliance: PASS

APPROVED
```

**Validation:**
- [ ] User risk profile checked
- [ ] VETO logic works correctly
- [ ] Reasoning provided for decisions

---

#### Testing StrategyDirector

**Test Query:**
```
"Backtest RSI strategy on AAPL for 5 years"
```

**Expected Output:**
```
Backtest Results (AAPL, 2019-2024):
- Total Return: 42.5%
- Sharpe Ratio: 1.85
- Max Drawdown: -18.2%
- Win Rate: 58.3%
- Trades: 47

vs Buy & Hold: +12.3% outperformance

Recommendation: Strategy VALIDATED
```

**Validation:**
- [ ] Real historical data used
- [ ] Metrics calculated correctly
- [ ] Performance vs benchmark shown
- [ ] Trade count reasonable

---

### L3 Agents

#### Testing TechnicalAnalyst

**Method:** Call directly via tool

```python
from agent_platform.tools.quant_tools import calculate_technicals

result = calculate_technicals("AAPL", ["rsi", "macd", "bollinger"])
print(result)
```

**Expected:**
```python
{
  "ticker": "AAPL",
  "rsi": 58.3,
  "macd": {...},
  "bollinger": {...}
}
```

---

#### Testing NewsScout

```python
from agent_platform.tools.intel_tools import multi_source_news

result = multi_source_news("NVDA", num_sources=5)
print(f"Sentiment: {result['overall_sentiment']}")
print(f"Articles: {len(result['articles'])}")
```

**Validation:**
- [ ] Multiple sources fetched
- [ ] Credibility scores reasonable (0.7-1.0)
- [ ] Sentiment scores in range (-1, 1)

---

## Testing Tools

### Quant Tools

```python
# Test market data
from agent_platform.tools.quant_tools import get_market_data

data = get_market_data("AAPL", "1mo", "1d")
assert data["ticker"] == "AAPL"
assert "current_price" in data
assert len(data["data"]) > 0
print("✅ get_market_data works")

# Test technical indicators
from agent_platform.tools.quant_tools import calculate_technicals

indicators = calculate_technicals("AAPL", ["rsi", "macd"])
assert 0 <= indicators["rsi"] <= 100
assert "macd" in indicators
print("✅ calculate_technicals works")
```

### Intel Tools

```python
# Test news
from agent_platform.tools.intel_tools import multi_source_news

news = multi_source_news("AAPL", num_sources=3)
assert "articles" in news
assert "overall_sentiment" in news
print(f"✅ News sentiment: {news['overall_sentiment']}")

# Test sentiment
from agent_platform.tools.intel_tools import sentiment_analyzer

result = sentiment_analyzer("This is great news for investors!")
assert result["classification"] == "positive"
print("✅ sentiment_analyzer works")
```

### Risk Tools

```python
# Test VaR
from agent_platform.tools.risk_tools import calculate_var

var = calculate_var("AAPL", confidence_level=0.95, holding_period=1, portfolio_value=10000)
assert "var_95" in var
assert 0 <= var["var_95"] <= 1
print(f"✅ VaR(95%): {var['var_95']*100}%")

# Test volatility
from agent_platform.tools.risk_tools import volatility_monitor

vol = volatility_monitor("TSLA", "90d")
assert "realized_volatility_90d" in vol
print(f"✅ Tesla 90d vol: {vol['realized_volatility_90d']*100}%")
```

### Strategy Tools

```python
# Test backtest
from agent_platform.tools.strategy_tools import backtest_strategy

result = backtest_strategy("AAPL", "rsi_strategy", "1y")
assert "results" in result
assert "sharpe_ratio" in result["results"]
print(f"✅ Backtest Sharpe: {result['results']['sharpe_ratio']}")
```

### System Tools

```python
# Test Memory Bank
from agent_platform.tools.system_tools import get_user_context_tool, store_agent_output_tool

# Store user context
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper
memory = ChromaDBWrapper()
memory.store_risk_profile("test_user", "LOW", 0.15, ["technology"])

# Retrieve
context = get_user_context_tool("test_user")
assert context["risk_tolerance"] == "LOW"
print("✅ Memory Bank works")
```

---

## Testing Full Hierarchy

### End-to-End Test

**Scenario:** Conservative investor asks about volatile stock

```python
# Setup
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

memory = ChromaDBWrapper()
memory.store_risk_profile("user123", "LOW", 0.15, ["technology"])
memory.store_trading_style("user123", "LONG_TERM", ">1year", "conservative")

# Test via ADK
# Query: "user_id:user123 Should I buy Tesla?"

# Expected flow:
# 1. MarketTrendPrincipal checks user context
# 2. HeadOfQuant: Technical analysis (200 words)
# 3. HeadOfIntel: News & sentiment (200 words)
# 4. ChiefRiskOfficer: VaR check → VETO (volatility > 15%)
# 5. StrategyDirector: Backtest (200 words)
# 6. Synthesis: HOLD recommendation due to VETO

# Validation:
# [ ] User profile retrieved correctly
# [ ] All agents responded
# [ ] VETO triggered
# [ ] Final recommendation respects risk tolerance
```

---

## Testing with Real Data

### Historical Data Tests

```python
# Verify data availability
from services.backtest_engine.data_loader import DataLoader
import os

dl = DataLoader()

# Check cache
cache_dir = "data/historical"
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

for ticker in tickers:
    cache_file = os.path.join(cache_dir, f"{ticker}.csv")
    if os.path.exists(cache_file):
        data = dl.load_cached_data(ticker)
        print(f"✅ {ticker}: {len(data)} days cached")
    else:
        print(f"❌ {ticker}: No cache found")
```

### Live Market Data Tests

```python
# Test with current market data
from agent_platform.tools.quant_tools import get_market_data
import datetime

# Get today's data
data = get_market_data("AAPL", "1d", "1m")  # 1 day, 1-minute intervals

# Verify real-time
latest_time = data["data"][-1]["date"]
now = datetime.datetime.now()
time_diff = (now - datetime.datetime.fromisoformat(latest_time)).total_seconds()

if time_diff < 900:  # Within 15 minutes
    print("✅ Real-time data confirmed")
else:
    print(f"⚠️ Data delayed by {time_diff/60:.1f} minutes")
```

---

## Example Test Scenarios

### Scenario 1: Basic Technical Analysis

**Input:**
```
"What are the technical indicators for Apple?"
```

**Expected Flow:**
1. MarketTrendPrincipal → HeadOfQuant
2. HeadOfQuant → TechnicalAnalyst
3. TechnicalAnalyst uses: calculate_technicals, analyze_price_action
4. Response includes: RSI, MACD, trend, support/resistance

**Validation:**
```python
# Check response contains
assert "RSI" in response or "rsi" in response.lower()
assert "MACD" in response or "macd" in response.lower()
assert any(word in response.lower() for word in ["buy", "sell", "hold"])
```

---

### Scenario 2: News-Driven Analysis

**Input:**
```
"Why is NVIDIA going up?"
```

**Expected Flow:**
1. MarketTrendPrincipal → HeadOfIntel
2. HeadOfIntel → NewsScout, SocialSentiment
3. NewsScout: Aggregate recent news
4. SocialSentiment: Check Reddit/Twitter
5. Response correlates price movement with news

**Validation:**
- [ ] News articles mentioned
- [ ] Sentiment scores provided
- [ ] Causal reasoning (e.g., "due to AI chip demand")

---

### Scenario 3: Risk-Aware Recommendation

**Setup:**
```python
# User: Conservative, max drawdown 10%
memory.store_risk_profile("conservative_user", "LOW", 0.10, [])
```

**Input:**
```
"user_id:conservative_user Should I invest in crypto-related stocks?"
```

**Expected:**
- ChiefRiskOfficer: High volatility detected
- VETO issued
- Recommendation: HOLD or very small allocation

**Validation:**
- [ ] User profile loaded
- [ ] Risk assessment performed
- [ ] Recommendation matches risk tolerance

---

### Scenario 4: Strategy Validation

**Input:**
```
"Backtest moving average crossover on Microsoft for 2 years"
```

**Expected Flow:**
1. MarketTrendPrincipal → StrategyDirector
2. StrategyDirector → BacktestEngineer
3. BacktestEngineer: Load MSFT 2yr data
4. Execute ma_crossover strategy
5. Calculate metrics: Sharpe, drawdown, win rate
6. Compare to buy & hold

**Validation:**
```python
assert "sharpe" in response.lower()
assert "drawdown" in response.lower()
assert "win rate" in response.lower() or "win_rate" in response
assert any(str in response for str in ["outperform", "underperform"])
```

---

### Scenario 5: Memory & Personalization

**Test:** System remembers user preferences

```python
# Session 1: User indicates preference
"I prefer dividend stocks" → System stores preference

# Session 2: Next query
"Recommend a tech stock" → System suggests MSFT (pays dividends)
                          instead of NVDA (no dividend)
```

**Validation:**
```python
# Check memory
context = memory.get_user_context("user123")
assert "dividend" in str(context).lower()

# Check recommendation
# Response should mention dividend if relevant
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Agent Response Timeout

**Symptom:** Agent takes >10 seconds or times out

**Diagnosis:**
```python
# Check tool execution time
from shared.utils.logger import TitanLogger

stats = TitanLogger.get_performance_stats()
for tool, metrics in stats.items():
    if metrics['avg_ms'] > 2000:
        print(f"⚠️ Slow tool: {tool} ({metrics['avg_ms']}ms)")
```

**Solutions:**
- Check internet connection (for yfinance, news APIs)
- Verify cached data exists
- Reduce data lookback period
- Enable caching in config.yaml

---

#### Issue 2: VETO Not Triggering

**Symptom:** High-risk stock approved for conservative user

**Diagnosis:**
```python
# Check user profile
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

memory = ChromaDBWrapper()
profile = memory.get_user_context("user123")
print(f"Risk tolerance: {profile.get('risk_tolerance')}")
print(f"Max drawdown: {profile.get('max_drawdown_tolerance')}")

# Check volatility calculation
from agent_platform.tools.risk_tools import volatility_monitor

vol = volatility_monitor("TSLA", "90d")
print(f"Volatility: {vol['realized_volatility_90d']}")
```

**Solutions:**
- Ensure user profile stored correctly
- Verify ChiefRiskOfficer has access to user context
- Check VETO logic in chief_risk_officer.py

---

#### Issue 3: Backtest Returns Unrealistic Results

**Symptom:** Sharpe ratio >5 or 1000% returns

**Diagnosis:**
```python
# Check data quality
from services.backtest_engine.data_loader import DataLoader

dl = DataLoader()
data = dl.load_cached_data("AAPL")

# Look for anomalies
print(data['Close'].describe())
print(f"Max daily return: {data['Close'].pct_change().max()*100}%")
print(f"Min daily return: {data['Close'].pct_change().min()*100}%")
```

**Solutions:**
- Re-download historical data
- Check for stock splits (adjust data)
- Verify strategy logic in simulator.py

---

#### Issue 4: Memory Bank Not Persisting

**Symptom:** User preferences lost between sessions

**Diagnosis:**
```python
import os

# Check ChromaDB directory
chroma_dir = "services/memory-bank/chroma_data"
if os.path.exists(chroma_dir):
    size = sum(os.path.getsize(os.path.join(chroma_dir, f)) 
               for f in os.listdir(chroma_dir) if os.path.isfile(os.path.join(chroma_dir, f)))
    print(f"ChromaDB size: {size / 1024 / 1024:.2f} MB")
else:
    print("❌ ChromaDB directory not found")
```

**Solutions:**
- Ensure chroma_data/ exists and is writable
- Check ChromaDB initialization in chromadb_wrapper.py
- Verify persist() called after writes

---

#### Issue 5: News Tool Returns Empty Results

**Symptom:** multi_source_news returns no articles

**Diagnosis:**
```python
# Test news API directly
from agent_platform.tools.intel_tools import multi_source_news

result = multi_source_news("AAPL", num_sources=5)
print(f"Articles found: {len(result.get('articles', []))}")
print(f"Sources: {[a['source'] for a in result.get('articles', [])]}")
```

**Solutions:**
- Check internet connectivity
- Verify API keys (if using paid news APIs)
- Try different ticker symbols
- Reduce num_sources parameter

---

### Performance Benchmarks

**Expected Performance:**

| Operation | Expected Time | Alert If > |
|-----------|---------------|------------|
| get_market_data | <500ms | 1s |
| calculate_technicals | <300ms | 500ms |
| multi_source_news | <2s | 5s |
| backtest_strategy (1y) | <3s | 10s |
| Full agent query | <5s | 10s |

**Monitoring:**
```python
# Check current performance
from agent_platform.dashboard import TitanDashboard

dashboard = TitanDashboard()
print(dashboard.generate_text_report())
```

---

### Logging for Debugging

**Enable Debug Logging:**
```python
# In your test script
from shared.utils.logger import get_logger

logger = get_logger("test_agent", log_level="DEBUG")
```

**Check Logs:**
```bash
# View today's log
cat logs/titan-$(date +%Y%m%d).log | grep ERROR

# Search for specific agent
cat logs/titan-*.log | grep "agent.*HeadOfQuant"

# Performance issues
cat logs/titan-*.log | grep "duration_ms" | grep -v "duration_ms\":[0-9]\{1,3\}\." # >1s
```

---

## Test Checklist

### Pre-Deployment Checklist

- [ ] All 17 agents respond to test queries
- [ ] All 28 tools execute without errors
- [ ] Risk VETO triggers correctly
- [ ] Memory Bank persists data
- [ ] Backtest returns realistic metrics
- [ ] Dashboard shows statistics
- [ ] Logs written to file
- [ ] Performance within benchmarks (<5s)
- [ ] User personalization works
- [ ] Documentation accurate

### Regression Testing

After any code changes, run:

```bash
# Quick smoke test
python tests/smoke_test.py

# Full integration test
python tests/integration_test_full.py

# Performance test
python tests/performance_test.py
```

---

**Last Updated:** December 2024  
**Version:** 1.0.0

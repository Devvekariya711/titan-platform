# Month 3 Implementation Plan - Accuracy & Safety

## Overview

**Goal**: Enhance system accuracy and safety through personalized learning (Memory Bank) and strategy validation (Backtest Engine).

**Approach**: "Move Slowly but Very Strongly" - Methodical implementation with testing at each step.

**Duration**: 3 weeks (focused scope)

---

## Week 1: Memory Bank Enhancement

### Current State
- ✅ Basic ChromaDB wrapper created
- ✅ Basic memory_save and memory_retrieve tools
- ✅ Three collections: user_preferences, analysis_history, trade_history

### Enhancements Needed

#### 1.1 Deep User Preferences Integration
**File**: `services/memory-bank/chromadb_wrapper.py`

**Add Methods**:
- `store_risk_profile(user_id, risk_tolerance, max_drawdown, preferred_sectors)`
- `store_trading_style(user_id, style, timeframe, position_sizing)`
- `get_user_context(user_id)` - Returns comprehensive user profile
- `update_preference_from_feedback(user_id, feedback_type, content)`

**Integration**:
- Update `system_tools.py` to use these new methods
- L1 MarketTrendPrincipal checks user context before recommendations

#### 1.2 Historical Analysis Storage
**Enhancement**: Store ALL agent outputs for learning

**Add Methods**:
- `store_agent_output(agent_name, ticker, output, confidence, metadata)`
- `retrieve_similar_analysis(ticker, timeframe="30d")`
- `get_accuracy_metrics(agent_name, ticker)` - Track agent accuracy over time

**Use Case**: 
- Before analysis, check if similar analysis exists
- Compare current vs previous recommendations
- Learn from past accuracy

#### 1.3 Context Compaction
**Challenge**: ChromaDB can grow large

**Add Methods**:
- `compact_old_data(days_to_keep=90)`
- `summarize_analysis_batch(ticker, date_range)`
- `archive_to_cold_storage(cutoff_date)`

---

## Week 2: Backtest Engine Implementation

### Current State
- ✅ Placeholder simulator.py
- ❌ No real historical data
- ❌ No strategy execution logic

### Implementation Plan

#### 2.1 Historical Data Loading
**File**: `services/backtest-engine/data_loader.py` (NEW)

**Features**:
- Download 5 years of OHLCV data from yfinance
- Cache to CSV in `./data/historical/{ticker}.csv`
- Load data into pandas DataFrame
- Handle missing data and splits

**Methods**:
```python
def download_historical_data(ticker, start_date, end_date, cache=True)
def load_cached_data(ticker)
def get_price_at_date(ticker, date)
```

#### 2.2 Strategy Simulator
**File**: `services/backtest-engine/simulator.py` (ENHANCE)

**Replace placeholder with**:
```python
class BacktestEngine:
    def __init__(self):
        self.data_loader = DataLoader()
        self.portfolio = VirtualPortfolio()
    
    def run_backtest(self, ticker, strategy, start_date, end_date):
        # Load historical data
        # Execute strategy day-by-day
        # Track performance
        # Return metrics
```

**Strategies to Support** (simplified):
1. `buy_and_hold`: Buy at start, hold to end
2. `rsi_strategy`: Buy RSI<30, Sell RSI>70
3. `moving_average_crossover`: Golden cross/death cross

#### 2.3 Performance Metrics
**File**: `services/backtest-engine/metrics.py` (NEW)

**Calculate**:
- Total Return (%)
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Average Gain/Loss per trade
- Comparison vs Buy & Hold

#### 2.4 Integration with Tools
**Update**: `agent_platform/tools/strategy_tools.py`

**Enhance `backtest_strategy` tool**:
- Remove simulated data
- Call real `BacktestEngine.run_backtest()`
- Return real historical metrics

---

## Week 3: System Refinements & Testing

### 3.1 Enhanced Risk VETO Logic
**File**: `agent_platform/agents/leads/chief_risk_officer.py`

**Enhancements**:
- Check Memory Bank for this user's risk tolerance
- Use real VaR calculations (if portfolio data available)
- Store VETO decisions in Memory Bank for learning

### 3.2 FactChecker Integration
**File**: `agent_platform/agents/specialists/fact_checker.py`

**Enhancements**:
- Verify claims against Memory Bank historical data
- Check if past analysis contradicts current claims
- Store verification results

### 3.3 Comprehensive Testing

#### Test Suite
**File**: `agent_platform/test_month3.py` (NEW)

**Tests**:
1. **Memory Bank**:
   - Store user preferences → Retrieve correctly
   - Store analysis → Find similar past analysis
   - Compact old data → Verify deletion

2. **Backtest Engine**:
   - Load AAPL historical data → Verify 5 years loaded
   - Run buy_and_hold backtest → Calculate realistic metrics
   - Compare with real historical performance

3. **Integration**:
   - User asks "Should I buy AAPL?"
   - System checks Memory Bank for user's risk profile
   - Returns recommendation tailored to user
   - Stores recommendation in history

#### End-to-End Test
**Scenario**: "Conservative investor asks about Tesla"

**Expected Flow**:
1. Memory Bank retrieves: risk_tolerance=LOW, max_drawdown=15%
2. Quant: Technical analysis (200 words)
3. Risk: VaR check → Tesla volatility HIGH → Recommend REDUCE SIZE
4. Strategy: Backtest Tesla vs conservative portfolio → Poor Sharpe for conservative
5. L1 Synthesis: "Tesla volatility exceeds your 15% drawdown tolerance. HOLD or reduce to 2% of portfolio max."
6. Memory Bank stores: User profile + recommendation

---

## Implementation Order

1. **Day 1-2**: Memory Bank enhancements
2. **Day 3-4**: Historical data loader
3. **Day 5-6**: Backtest simulator
4. **Day 7**: Performance metrics
5. **Day 8-9**: Tool integration
6. **Day 10**: Testing & refinement

---

## Success Criteria

- [ ] User preferences stored and retrieved correctly
- [ ] Historical analysis searchable by ticker/date
- [ ] 5 years of data loaded for AAPL, TSLA, NVDA
- [ ] Backtest returns real Sharpe ratios and drawdowns
- [ ] Risk VETO considers user risk tolerance
- [ ] All tests pass
- [ ] Clean git commit history
- [ ] Tag: `v0.4-month3`

---

## Files to Create/Modify

**New Files** (3):
- `services/backtest-engine/data_loader.py`
- `services/backtest-engine/metrics.py`
- `agent_platform/test_month3.py`

**Enhanced Files** (4):
- `services/memory-bank/chromadb_wrapper.py` (add 9 methods)
- `services/backtest-engine/simulator.py` (replace placeholder)
- `agent_platform/tools/strategy_tools.py` (real backtest)
- `agent_platform/tools/system_tools.py` (enhanced memory)

**Total Changes**: 7 files

---

**Principle**: Move Slowly but Very Strongly ✓

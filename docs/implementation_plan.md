# Phase 1 Implementation Plan: Titan Quant Agent

## Goal

Build the foundational "Quant Agent" - a specialized agent that performs cold, mathematical technical analysis on stocks using custom tools for market data and technical indicators.

## Problem Being Solved

Retail traders need instant access to technical analysis (RSI, MACD, Bollinger Bands, etc.) but lack the tools and expertise to calculate and interpret these indicators quickly. The Quant Agent provides professional-grade technical analysis in seconds.

---

## Proposed Changes

### 1. Dependencies

#### `requirements.txt`
**[MODIFY]** [requirements.txt](file:///e:/market-analyst-project/requirements.txt)

Add the following dependencies:
- `pandas_ta` - Technical analysis library with 130+ indicators
- `pandas` - Data manipulation (if not already included)
- `numpy` - Numerical computations
- `uvicorn` - For running the server

---

### 2. Tools Module (Core Changes)

#### `market_analyst/quant_tools.py` 
**[NEW]** [quant_tools.py](file:///e:/market-analyst-project/market_analyst/quant_tools.py)

Create a new module with three advanced tools:

**Tool 1: `get_market_data(ticker, period)`**
- Fetches OHLCV (Open, High, Low, Close, Volume) data
- Returns structured data with error handling
- Validates ticker symbols
- Provides data quality checks

**Tool 2: `calculate_technicals(ticker, period)`**
- Calculates RSI (Relative Strength Index) - 14 period
- Calculates MACD (Moving Average Convergence Divergence) - 12,26,9
- Calculates Bollinger Bands - 20 period, 2 std dev
- Calculates Moving Averages - 50-day and 200-day
- Analyzes volume trends
- Returns structured JSON with all indicators

**Tool 3: `analyze_price_action(ticker)`**
- Identifies trends (Uptrend/Downtrend/Sideways)
- Detects support and resistance levels
- Identifies chart patterns (Golden Cross, Death Cross)
- Provides trading signals based on technical confluences

All tools will:
- Include comprehensive error handling
- Return structured JSON for easy parsing
- Log all calculations for observability
- Use pandas_ta for accurate calculations

---

### 3. Quant Agent

#### `market_analyst/quant_agent.py`
**[NEW]** [quant_agent.py](file:///e:/market-analyst-project/market_analyst/quant_agent.py)

Create the Quant Agent with:

```python
quant_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="quant_analyst",
    description="Mathematical technical analyst specialized in price action",
    instruction="<Detailed instruction for cold technical analysis>",
    tools=[market_data_tool, technicals_tool, price_action_tool]
)
```

**Key characteristics**:
- No emotion, only numbers
- Cites specific indicator values
- Uses precise terminology
- Provides BUY/SELL/HOLD signals with confidence scores
- Returns structured JSON output

---

### 4. Root Agent Updates

#### `market_analyst/agent.py`
**[MODIFY]** [agent.py](file:///e:/market-analyst-project/market_analyst/agent.py)

Update the root agent to:
1. Import and register the Quant Agent as a sub-agent
2. Update instruction to dispatch Quant Agent for technical queries
3. Add synthesis logic to interpret Quant's output

Changes:
- Import `quant_agent` from `quant_agent.py`
- Add `quant_agent` to `sub_agents` list
- Update `ROOT_INSTRUCTION` to include delegation logic

---

### 5. Testing Infrastructure

#### `tests/test_quant_agent.py`
**[NEW]** [test_quant_agent.py](file:///e:/market-analyst-project/tests/test_quant_agent.py)

Create test file with:
- Unit tests for each tool function
- Integration test for Quant Agent
- Test cases for various market conditions
- Mock data for offline testing

---

### 6. Example Usage Script

#### `examples/phase1_demo.py`
**[NEW]** [phase1_demo.py](file:///e:/market-analyst-project/examples/phase1_demo.py)

Demonstration script showing:
- How to query Quant Agent directly
- How to use via Root Agent
- Example outputs for NVDA, TSLA, AAPL
- Error handling examples

---

## Verification Plan

### Automated Tests

**Test 1: Tool Function Tests**
```bash
# From project root
python -m pytest tests/test_quant_agent.py::test_get_market_data -v
python -m pytest tests/test_quant_agent.py::test_calculate_technicals -v
```

Expected: All tools return valid JSON with correct fields

**Test 2: Integration Test**
```bash
python -m pytest tests/test_quant_agent.py::test_quant_agent_analysis -v
```

Expected: Quant agent returns technical analysis with signal and confidence score

---

### Manual Verification

**Manual Test 1: Direct Tool Testing**

Run the example script:
```bash
cd e:\market-analyst-project
python examples\phase1_demo.py
```

Expected output example:
```json
{
  "ticker": "NVDA",
  "signal": "HOLD",
  "confidence": 0.65,
  "indicators": {
    "rsi": 58.3,
    "macd": 2.15,
    "macd_signal": 1.87,
    "bb_upper": 485.20,
    "bb_lower": 465.80,
    "current_price": 475.50
  },
  "reasoning": "RSI at 58 indicates neutral momentum. MACD crossed above signal line (bullish). Price near middle Bollinger Band. No strong conviction either way."
}
```

**Manual Test 2: Via Web Server**

1. Start the server:
```bash
python main.py
```

2. Navigate to the ADK web interface (typically http://localhost:8000)

3. Test queries:
   - "How does NVDA look technically?"
   - "Analyze TSLA technical indicators"
   - "What's the RSI for AAPL?"

Expected: Root agent delegates to Quant agent and returns technical analysis

**Manual Test 3: Real Market Scenarios**

Test with stocks in different conditions:
- **Oversold**: Find a stock with RSI < 30 (e.g., check recent market crashes)
- **Overbought**: Find a stock with RSI > 70 (e.g., recent meme stock pumps)
- **Trending**: Find a stock in clear uptrend (50-day MA > 200-day MA)

Verify Quant agent correctly identifies each condition.

---

### Logging Verification

After running tests, check structured logs:
```bash
# View the generated logs
cat market_analyst.log | python -m json.tool
```

Expected: JSON-formatted logs showing:
- Tool calls with parameters
- Calculation results
- Agent reasoning
- Timestamps

---

## Success Criteria

Phase 1 is complete when:

✅ All dependencies installed successfully  
✅ All three tools return valid data for major stocks (AAPL, TSLA, NVDA)  
✅ Quant Agent returns structured JSON with signal + confidence  
✅ Root Agent successfully delegates to Quant Agent  
✅ Automated tests pass  
✅ Manual testing shows correct technical analysis  
✅ Structured logs capture all operations  
✅ Error handling works for invalid tickers  

---

## Notes

- **Why pandas_ta**: Industry-standard library with accurate indicator calculations
- **Why gemini-2.5-flash-lite**: Fast model sufficient for mathematical reasoning
- **Structured output**: Critical for Phase 3 (parallel synthesis)
- **Error handling**: Essential for production use with real market data

---

## Next Steps After Phase 1

Once Phase 1 is verified:
1. Phase 2A: Build Journalist Agent (news + sentiment)
2. Phase 2B: Implement parallel execution
3. Phase 3: Add Risk Manager Agent
4. Phase 4: Memory Bank integration
5. Phase 5: Loop agent for monitoring

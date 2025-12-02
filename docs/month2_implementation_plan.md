# Month 2 Implementation Plan - Intelligence Layer

## Overview

**Goal**: Expand from 3 agents to 17 agents, and from 3 tools to 25 tools.

**Approach**: Systematic, squad-by-squad implementation following "Move Slowly but Very Strongly"

---

## Week 1: Intel Division

### Agents to Create (3 L3 + 1 L2)

1. **NewsScout** (L3 Specialist)
   - File: `agent_platform/agents/specialists/intel_specialists.py`
   - Role: Mainstream news aggregation
   - Tools: multi_source_news_tool, news_search_tool
   - Output: 200 words max
   - Format: Top 3 headlines + sentiment + catalyst

2. **SocialSentiment** (L3 Specialist)
   - File: Same as above
   - Role: Social media sentiment analysis
   - Tools: reddit_sentiment_tool, twitter_sentiment_tool
   - Output: 200 words max
   - Format: Sentiment score + mention count + key themes

3. **MacroEconomist** (L3 Specialist)
   - File: Same as above
   - Role: Macroeconomic analysis
   - Tools: interest_rates_tool, gdp_tool, geopolitical_tool
   - Output: 200 words max
   - Format: Macro regime + key factors + outlook

4. **HeadOfIntel** (L2 Manager)
   - File: `agent_platform/agents/leads/head_of_intel.py`
   - Role: Synthesize News + Social + Macro
   - Sub-agents: 3 Intel specialists
   - Output: 250 words max
   - Format: Narrative summary + catalysts + sentiment signal

### Tools to Create (8)

File: `agent_platform/tools/intel_tools.py`

1. `multi_source_news` - Aggregate from multiple sources
2. `reddit_sentiment` - Scrape r/wallstreetbets sentiment
3. `twitter_sentiment` - Twitter/X sentiment analysis
4. `get_interest_rates` - Fetch interest rate data
5. `get_gdp_data` - Economic indicators
6. `track_geopolitical` - Major geopolitical events
7. `sentiment_analyzer` - Generic sentiment analysis
8. `google_search` - For FactChecker (Week 4)

### Implementation Steps

1. Create placeholder intel_tools.py with all 8 tools
2. Implement 3 L3 specialists in intel_specialists.py
3. Create HeadOfIntel in head_of_intel.py
4. Test Intel division independently
5. Git commit: "Week 1: Intel Division complete"

---

## Week 2: Risk Division

### Agents to Create (2 L3 + 1 L2)

1. **VolatilityGuard** (L3 Specialist)
   - File: `agent_platform/agents/specialists/risk_specialists.py`
   - Role: Risk monitoring
   - Tools: var_tool, volatility_tool
   - Output: 200 words max

2. **ComplianceOfficer** (L3 Specialist)
   - File: Same as above
   - Role: Regulatory compliance
   - Tools: compliance_check_tool, blacklist_tool
   - Output: 200 words max

3. **ChiefRiskOfficer** (L2 Manager)
   - File: `agent_platform/agents/leads/chief_risk_officer.py`
   - Role: Risk management + VETO power
   - Sub-agents: 2 Risk specialists
   - Output: 250 words max + VETO decision

### Tools to Create (5)

File: `agent_platform/tools/risk_tools.py`

1. `calculate_var` - Value at Risk
2. `monitor_volatility` - Volatility metrics
3. `check_compliance` - Regulatory checks
4. `analyze_correlation` - Portfolio correlation
5. `detect_blackswan` - Anomaly detection

---

## Week 3: Strategy Division

### Agents to Create (3 L3 + 1 L2)

1. **BacktestEngineer**, **ScenarioSimulator**, **CorrelationAnalyst**
2. **StrategyDirector** (L2 Manager)

### Tools to Create (4)

File: `agent_platform/tools/system_tools.py` (partial)

1. `backtest_tool`
2. `monte_carlo_tool`
3. `correlation_tool`
4. `scenario_tool`

---

## Week 4: FactChecker + Quant Completion

### Agents to Create (3 L3)

1. **FactChecker** (special L3)
2. **FundamentalAnalyst** (enhance placeholder)
3. **MicrostructureAnalyst** (enhance placeholder)

### Tools to Create (9 remaining)

- 5 more Quant tools
- 4 System tools (memory_save, memory_retrieve, send_alert, structured_logger)

---

## Week 5: Integration

### Update L1 MarketTrendPrincipal

Add all 4 L2 heads:
```python
sub_agents=[
    head_of_quant,
    head_of_intel,
    chief_risk_officer,
    strategy_director
]
```

Implement weighted synthesis logic.

---

## Testing Strategy

Test after each week:
- Week 1: Intel division works independently
- Week 2: Risk division works independently
- Week 3: Strategy division works independently
- Week 4: FactChecker operational
- Week 5: Full 17-agent integration

---

**Start**: Week 1 - Intel Division

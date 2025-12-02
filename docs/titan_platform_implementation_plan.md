# Titan Platform - Implementation Plan

> **Transforming market-analyst-project into Enterprise-Grade Multi-Agent Investment Platform**

---

## Executive Summary

This plan integrates the enterprise Titan Platform architecture (17-agent hierarchy, microservices, monorepo) with the existing Phase 1 market-analyst-project while maintaining backward compatibility and local development capability.

### Key Design Decisions

1. **Monorepo Structure**: All components in single repo, organized by squad
2. **Local-First Development**: No cloud dependencies, simulated services
3. **Incremental Migration**: Existing Phase 1 code preserved and enhanced
4. **Google ADK Focus**: Agent platform remains pure ADK, services are Python tools

---

## Architecture Overview

### Current State (Phase 1 ✅)
```
market-analyst-project/
├── market_analyst/
│   ├── agent.py              # Root agent
│   ├── quant_agent.py        # Quant analyst (L3 equivalent)
│   ├── quant_tools.py        # 3 advanced tools
│   ├── supporting_agents.py  # Data Scout, Risk Assessor
│   └── tools.py              # Basic tools
├── docs/                     # Documentation
└── requirements.txt
```

### Target State (Titan Platform 🎯)
```
titan-platform/
├── .github/workflows/        # CI/CD
├── infra/                    # Infrastructure configs (k8s, kafka, clickhouse)
│   ├── k8s/                  # For future deployment
│   ├── kafka/                # Topic definitions
│   └── clickhouse/           # Schema migrations
│
├── shared/                   # Shared libraries
│   ├── protocol/             # gRPC/REST protocol definitions
│   └── utils/                # Common utilities, loggers, error handlers
│
├── services/                 # Microservices (simulated locally)
│   ├── ingestion-engine/     # Data connectors (YFinance, News APIs)
│   ├── feature-store/        # Real-time calculations (RSI, MACD)
│   ├── model-serving/        # ML model hosting (future)
│   ├── backtest-engine/      # Simulation engine
│   └── memory-bank/          # RAG service (ChromaDB wrapper)
│
└── agent_platform/           # THE BRAIN (Google ADK)
    ├── requirements.txt
    ├── main.py               # Entry point
    │
    ├── agents/               # The 17-Agent Swarm
    │   ├── root/             # L1: MarketTrendPrincipal
    │   ├── leads/            # L2: 4 Department Heads
    │   └── specialists/      # L3: 12 Specialist Agents
    │
    └── tools/                # The 25 Tools
        ├── quant_tools.py    # 8 quant tools
        ├── intel_tools.py    # 8 intelligence tools
        ├── risk_tools.py     # 5 risk tools
        └── system_tools.py   # 4 system tools
```

---

## Migration Strategy

### Phase 0: Setup & Commit Existing Work ✅
**Goal**: Preserve current work and prepare for transformation

**Actions**:
1. Commit all existing work to git with message: "Phase 1 complete - Quant Agent baseline"
2. Create `docs/titan_platform_*.md` for all planning (can delete later)
3. Tag current state as `v0.1-phase1-complete`

---

## Month 1: The Foundation (Data & Skeleton)

### Goal
Get data flowing from API → simulated services → agents, and establish the 17-agent hierarchy skeleton.

---

### Task 1.1: Monorepo Structure Setup

**Files to Create**:

#### [NEW] Directory Structure
```bash
titan-platform/
├── .github/workflows/ci.yml
├── infra/
│   ├── k8s/README.md
│   ├── kafka/topics.json
│   └── clickhouse/schema.sql
├── shared/
│   ├── __init__.py
│   ├── protocol/
│   │   └── market_data.proto
│   └── utils/
│       ├── logger.py
│       └── errors.py
├── services/
│   ├── ingestion-engine/
│   │   ├── __init__.py
│   │   ├── connectors/
│   │   │   ├── yfinance_connector.py
│   │   │   └── news_connector.py
│   │   └── main.py
│   ├── memory-bank/
│   │   ├── __init__.py
│   │   ├── chromadb_wrapper.py
│   │   └── main.py
│   └── backtest-engine/
│       ├── __init__.py
│       └── simulator.py
└── agent_platform/
    ├── requirements.txt
    ├── main.py
    ├── agents/
    │   ├── __init__.py
    │   ├── root/
    │   │   └── market_trend_principal.py
    │   ├── leads/
    │   │   ├── head_of_quant.py
    │   │   ├── head_of_intel.py
    │   │   ├── chief_risk_officer.py
    │   │   └── strategy_director.py
    │   └── specialists/
    │       ├── quant_specialists.py      # Technical, Fundamental, Microstructure
    │       ├── intel_specialists.py      # News, Social, Macro
    │       ├── risk_specialists.py       # Volatility, Compliance
    │       ├── strategy_specialists.py   # Backtest, Scenario, Correlation
    │       └── fact_checker.py           # FactChecker
    └── tools/
        ├── __init__.py
        ├── quant_tools.py
        ├── intel_tools.py
        ├── risk_tools.py
        └── system_tools.py
```

**Migration Actions**:
1. Move `market_analyst/` → `agent_platform/agents/` (preserve existing code)
2. Extract tools from `quant_tools.py` → `agent_platform/tools/quant_tools.py`
3. Update all imports

---

### Task 1.2: Data Infrastructure (Simulated)

#### [NEW] `services/ingestion-engine/connectors/yfinance_connector.py`

**Purpose**: Centralized market data fetching (replaces direct yfinance calls)

```python
"""
Market Data Ingestion Connector
Simulates Kafka → ClickHouse pipeline locally
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataConnector:
    """Fetches and caches market data"""
    
    def __init__(self, cache_dir="./data/cache"):
        self.cache_dir = cache_dir
        
    def get_ohlcv(self, ticker: str, period: str = "1mo"):
        """
        Fetch OHLCV data for ticker
        In production: This would read from ClickHouse
        In dev: Direct yfinance call with caching
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            
            if df.empty:
                return {"error": f"No data for {ticker}"}
                
            return {
                "ticker": ticker,
                "data": df.to_dict('records'),
                "current_price": df['Close'].iloc[-1],
                "volume_avg_30d": df['Volume'].tail(30).mean(),
                "high_52w": df['High'].tail(252).max() if len(df) >= 252 else df['High'].max(),
                "low_52w": df['Low'].tail(252).min() if len(df) >= 252 else df['Low'].min(),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_realtime_price(self, ticker: str):
        """Simulates real-time price stream"""
        data = self.get_ohlcv(ticker, period="1d")
        return data.get("current_price", None)
```

#### [NEW] `services/memory-bank/chromadb_wrapper.py`

**Purpose**: Vector memory for RAG

```python
"""
Memory Bank Service - RAG with ChromaDB
Simulates Milvus for local development
"""
import chromadb
from chromadb.config import Settings
from datetime import datetime

class MemoryBank:
    """Vector store for user preferences and historical context"""
    
    def __init__(self, persist_dir="./data/memory"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection("titan_memory")
    
    def store(self, key: str, content: str, metadata: dict = None):
        """Store memory with vector embedding"""
        metadata = metadata or {}
        metadata["timestamp"] = datetime.now().isoformat()
        
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[f"{key}_{datetime.now().timestamp()}"]
        )
    
    def retrieve(self, query: str, n_results: int = 5):
        """Retrieve relevant memories"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
```

---

### Task 1.3: Agent Hierarchy - L1 & L2 (The 4 Heads)

#### [MODIFY] `agent_platform/agents/root/market_trend_principal.py`

**Enhancement from existing `agent.py`**:

```python
"""
L1: MarketTrendPrincipal - The CEO
Only talks to L2 Department Heads
"""
from google.adk.agents import Agent
from ..leads.head_of_quant import head_of_quant
from ..leads.head_of_intel import head_of_intel
from ..leads.chief_risk_officer import chief_risk_officer
from ..leads.strategy_director import strategy_director

LLM = "gemini-2.0-flash-exp"

ROOT_INSTRUCTION = """
You are the MarketTrendPrincipal - the CEO of the Titan Investment Committee.

**HIERARCHY**:
You manage 4 Department Heads (L2):
1. **HeadOfQuant** - Manages quantitative analysis (Technical, Fundamental, Microstructure)
2. **HeadOfIntel** - Manages intelligence gathering (News, Social, Macro)
3. **ChiefRiskOfficer** - Manages safety (Volatility, Compliance)
4. **StrategyDirector** - Manages validation (Backtest, Scenarios)

**WORKFLOW**:
1. When user asks a question, dispatch to relevant L2 heads
2. For comprehensive analysis, dispatch to ALL 4 heads in parallel
3. Synthesize their reports into ONE clear recommendation
4. If L2 heads conflict (Quant says BUY, Risk says HIGH RISK), explicitly note it

**SYNTHESIS RULES**:
- Weight: Quant (40%), Intel (30%), Risk (20%), Strategy (10%)
- If Risk Officer vetoes, ALWAYS respect the veto
- If Strategy shows backtest failure, lower confidence
- Present final recommendation with confidence score (0-100%)

**OUTPUT FORMAT**:
## Analysis for [TICKER]

### Department Reports:
- **Quant**: [summary]
- **Intel**: [summary]
- **Risk**: [summary]
- **Strategy**: [summary]

### Synthesis:
[Your analysis of agreements/conflicts]

### Final Recommendation:
**Signal**: BUY/SELL/HOLD
**Confidence**: XX%
**Action**: [Specific guidance]
"""

market_trend_principal = Agent(
    model=LLM,
    name="market_trend_principal",
    description="The CEO of Titan Investment Committee. Synthesizes inputs from 4 department heads.",
    instruction=ROOT_INSTRUCTION,
    sub_agents=[head_of_quant, head_of_intel, chief_risk_officer, strategy_director]
)
```

#### [NEW] `agent_platform/agents/leads/head_of_quant.py`

**Evolution of existing `quant_agent.py`**:

```python
"""
L2: HeadOfQuant - Manages Quantitative Analysis
Delegates to 3 L3 specialists: Technical, Fundamental, Microstructure
"""
from google.adk.agents import Agent
from ..specialists.quant_specialists import technical_analyst, fundamental_analyst, microstructure_analyst

LLM = "gemini-2.0-flash-exp"

head_of_quant = Agent(
    model=LLM,
    name="head_of_quant",
    description="Head of Quantitative Analysis. Manages Technical, Fundamental, and Microstructure analysts.",
    instruction="""
You are the Head of Quantitative Analysis.

**YOUR TEAM**:
1. **technical_analyst**: Charts, indicators (RSI, MACD), price action
2. **fundamental_analyst**: Earnings, P/E ratios, balance sheets
3. **microstructure_analyst**: Order book, liquidity, whale activity

**YOUR JOB**:
1. Dispatch to relevant specialists based on query
2. For comprehensive analysis, get all 3 reports
3. Synthesize into unified quant assessment
4. Provide BUY/SELL/HOLD signal with confidence

**OUTPUT**:
Return structured analysis with specific numbers and clear signal.
""",
    sub_agents=[technical_analyst, fundamental_analyst, microstructure_analyst]
)
```

#### [NEW] `agent_platform/agents/leads/head_of_intel.py`

```python
"""
L2: HeadOfIntel - Manages Intelligence Gathering
Delegates to 3 L3 specialists: News, Social, Macro
"""
from google.adk.agents import Agent
from ..specialists.intel_specialists import news_scout, social_sentiment, macro_economist

LLM = "gemini-2.0-flash-exp"

head_of_intel = Agent(
    model=LLM,
    name="head_of_intel",
    description="Head of Intelligence. Manages News, Social Sentiment, and Macroeconomic analysis.",
    instruction="""
You are the Head of Intelligence.

**YOUR TEAM**:
1. **news_scout**: Mainstream news (Bloomberg, Reuters, Google News)
2. **social_sentiment**: Reddit/Twitter sentiment and trends
3. **macro_economist**: Interest rates, GDP, geopolitical events

**YOUR JOB**:
1. Dispatch to specialists to gather narrative context
2. Synthesize news + social + macro into coherent story
3. Identify catalysts (earnings, fed meetings, scandals)
4. Provide sentiment signal (BULLISH/BEARISH/NEUTRAL)

**OUTPUT**:
Return narrative summary with key catalysts and sentiment score.
""",
    sub_agents=[news_scout, social_sentiment, macro_economist]
)
```

#### [NEW] `agent_platform/agents/leads/chief_risk_officer.py`

```python
"""
L2: ChiefRiskOfficer - Risk Management & Compliance
Delegates to 2 L3 specialists: Volatility Guard, Compliance Officer
"""
from google.adk.agents import Agent
from ..specialists.risk_specialists import volatility_guard, compliance_officer

LLM = "gemini-2.0-flash-exp"

chief_risk_officer = Agent(
    model=LLM,
    name="chief_risk_officer",
    description="Chief Risk Officer. Has VETO power over risky trades.",
    instruction="""
You are the Chief Risk Officer. Your job is to PROTECT capital.

**YOUR TEAM**:
1. **volatility_guard**: VaR calculations, volatility monitoring
2. **compliance_officer**: Regulatory checks, blacklists

**YOUR JOB**:
1. Assess risk of proposed trades
2. Calculate Value at Risk (VaR)
3. Check compliance and regulations
4. VETO trades if risk exceeds limits

**VETO CONDITIONS**:
- VaR > 2% of portfolio
- Volatility > 40% (VIX equivalent)
- Regulatory blacklist
- Earnings in <3 days (high risk)

**OUTPUT**:
Return risk assessment with APPROVE/VETO decision.
""",
    sub_agents=[volatility_guard, compliance_officer]
)
```

#### [NEW] `agent_platform/agents/leads/strategy_director.py`

```python
"""
L2: StrategyDirector - Validation & Backtesting
Delegates to 3 L3 specialists: Backtest Engineer, Scenario Simulator, Correlation Analyst
"""
from google.adk.agents import Agent
from ..specialists.strategy_specialists import backtest_engineer, scenario_simulator, correlation_analyst

LLM = "gemini-2.0-flash-exp"

strategy_director = Agent(
    model=LLM,
    name="strategy_director",
    description="Strategy Director. Validates recommendations through backtesting and simulation.",
    instruction="""
You are the Strategy Director.

**YOUR TEAM**:
1. **backtest_engineer**: Historical replay and performance analysis
2. **scenario_simulator**: Monte Carlo and what-if analysis
3. **correlation_analyst**: Portfolio correlation and diversification

**YOUR JOB**:
1. Validate recommendations against historical data
2. Run Monte Carlo simulations
3. Check portfolio correlation (avoid over-concentration)
4. Provide validation score (0-100%)

**OUTPUT**:
Return validation report with backtest results and confidence adjustment.
""",
    sub_agents=[backtest_engineer, scenario_simulator, correlation_analyst]
)
```

---

### Task 1.4: L3 Specialist Agents (12 Specialists)

#### [NEW] `agent_platform/agents/specialists/quant_specialists.py`

**Contains**: TechnicalAnalyst, FundamentalAnalyst, MicrostructureAnalyst

```python
"""
L3 Quant Specialists (3 agents in one file)
"""
from google.adk.agents import Agent
from tools.quant_tools import (
    market_data_tool, technical_indicators_tool, price_action_tool,
    earnings_tool, pe_ratio_tool, order_book_tool
)

LLM = "gemini-2.5-flash-lite"  # Fast model for specialists

# --- Technical Analyst (Existing quant_agent.py logic) ---
technical_analyst = Agent(
    model=LLM,
    name="technical_analyst",
    description="Charts and technical indicators specialist",
    instruction="""
You analyze price action using technical indicators.
Use tools to get RSI, MACD, Bollinger Bands, Moving Averages.
Identify trends: Uptrend/Downtrend/Sideways.
Signal: Overbought (RSI>70), Oversold (RSI<30).
Provide BUY/SELL/HOLD with exact indicator values.
""",
    tools=[market_data_tool, technical_indicators_tool, price_action_tool]
)

# --- Fundamental Analyst ---
fundamental_analyst = Agent(
    model=LLM,
    name="fundamental_analyst",
    description="Earnings and valuation specialist",
    instruction="""
You analyze company fundamentals.
Use tools to get earnings, P/E ratios, revenue growth.
Compare valuation to sector peers.
Signal: UNDERVALUED/OVERVALUED/FAIR.
""",
    tools=[earnings_tool, pe_ratio_tool]
)

# --- Microstructure Analyst ---
microstructure_analyst = Agent(
    model=LLM,
    name="microstructure_analyst",
    description="Order book and liquidity specialist",
    instruction="""
You analyze market microstructure.
Use tools to examine order book depth, bid-ask spread, liquidity.
Detect whale activity (large volume spikes).
Signal: HIGH_LIQUIDITY/LOW_LIQUIDITY, INSTITUTIONAL_BUYING/SELLING.
""",
    tools=[order_book_tool]
)
```

#### [NEW] `agent_platform/agents/specialists/intel_specialists.py`

**Contains**: NewsScout, SocialSentiment, MacroEconomist

```python
"""
L3 Intel Specialists (3 agents in one file)
"""
from google.adk.agents import Agent
from tools.intel_tools import (
    news_search_tool, multi_source_news_tool,
    reddit_sentiment_tool, twitter_sentiment_tool,
    interest_rates_tool, gdp_tool, geopolitical_tool
)

LLM = "gemini-2.5-flash-lite"

# --- News Scout (Enhanced data_scout_agent) ---
news_scout = Agent(
    model=LLM,
    name="news_scout",
    description="Mainstream news aggregation specialist",
    instruction="""
You gather financial news from credible sources.
Use tools to search Bloomberg, Reuters, Google News.
Filter noise, prioritize impactful headlines.
Cite sources with credibility scores.
""",
    tools=[news_search_tool, multi_source_news_tool]
)

# --- Social Sentiment ---
social_sentiment = Agent(
    model=LLM,
    name="social_sentiment",
    description="Social media sentiment analyst",
    instruction="""
You analyze retail sentiment from Reddit and Twitter.
Use tools to scrape r/wallstreetbets, StockTwits, Twitter.
Filter spam and bots.
Provide sentiment: HYPE/NEUTRAL/FEAR, with mention count.
""",
    tools=[reddit_sentiment_tool, twitter_sentiment_tool]
)

# --- Macro Economist ---
macro_economist = Agent(
    model=LLM,
    name="macro_economist",
    description="Macroeconomic and geopolitical analyst",
    instruction="""
You analyze macro factors affecting markets.
Use tools to get interest rates, GDP data, geopolitical events.
Identify market regime: EXPANSION/RECESSION/STAGFLATION.
Signal macro sentiment: BULLISH/BEARISH/NEUTRAL.
""",
    tools=[interest_rates_tool, gdp_tool, geopolitical_tool]
)
```

#### [NEW] `agent_platform/agents/specialists/risk_specialists.py`

**Contains**: VolatilityGuard, ComplianceOfficer

```python
"""
L3 Risk Specialists (2 agents in one file)
"""
from google.adk.agents import Agent
from tools.risk_tools import var_tool, volatility_tool, compliance_check_tool, blacklist_tool

LLM = "gemini-2.5-flash-lite"

# --- Volatility Guard ---
volatility_guard = Agent(
    model=LLM,
    name="volatility_guard",
    description="Value at Risk and volatility monitoring",
    instruction="""
You calculate and monitor risk.
Use tools to compute VaR (Value at Risk), volatility metrics.
Alert if VaR > 2% or volatility > 40%.
Provide risk score: LOW/MEDIUM/HIGH/CRITICAL.
""",
    tools=[var_tool, volatility_tool]
)

# --- Compliance Officer ---
compliance_officer = Agent(
    model=LLM,
    name="compliance_officer",
    description="Regulatory compliance checker",
    instruction="""
You ensure regulatory compliance.
Use tools to check blacklists, regulatory restrictions.
Verify trade legality.
Provide compliance: APPROVED/RESTRICTED/PROHIBITED.
""",
    tools=[compliance_check_tool, blacklist_tool]
)
```

#### [NEW] `agent_platform/agents/specialists/strategy_specialists.py`

**Contains**: BacktestEngineer, ScenarioSimulator, CorrelationAnalyst

```python
"""
L3 Strategy Specialists (3 agents in one file)
"""
from google.adk.agents import Agent
from tools.system_tools import backtest_tool, monte_carlo_tool, correlation_tool

LLM = "gemini-2.5-flash-lite"

# --- Backtest Engineer ---
backtest_engineer = Agent(
    model=LLM,
    name="backtest_engineer",
    description="Historical backtesting specialist",
    instruction="""
You validate strategies against historical data.
Use backtest tool to replay trades on 5 years of data.
Calculate win rate, max drawdown, Sharpe ratio.
Provide validation score: 0-100%.
""",
    tools=[backtest_tool]
)

# --- Scenario Simulator ---
scenario_simulator = Agent(
    model=LLM,
    name="scenario_simulator",
    description="Monte Carlo and what-if analysis",
    instruction="""
You simulate future scenarios.
Use Monte Carlo tool to run 1000+ simulations.
Test what-if scenarios (market crash, sector rotation).
Provide probability distribution of outcomes.
""",
    tools=[monte_carlo_tool]
)

# --- Correlation Analyst ---
correlation_analyst = Agent(
    model=LLM,
    name="correlation_analyst",
    description="Portfolio correlation and diversification",
    instruction="""
You analyze portfolio balance.
Use correlation tool to build correlation matrix.
Detect over-concentration (e.g., 5 tech stocks).
Provide diversification score: EXCELLENT/GOOD/POOR.
""",
    tools=[correlation_tool]
)
```

#### [NEW] `agent_platform/agents/specialists/fact_checker.py`

**Special agent for accuracy**

```python
"""
L3: FactChecker - Hallucination Prevention (CRITICAL)
"""
from google.adk.agents import Agent
from tools.intel_tools import google_search_tool

LLM = "gemini-2.5-flash-lite"

fact_checker = Agent(
    model=LLM,
    name="fact_checker",
    description="Grounding agent - verifies claims against real data",
    instruction="""
You are the FactChecker. Your job is to prevent hallucinations.

**PROCESS**:
1. When another agent makes a factual claim (e.g., "Apple earnings beat estimates")
2. Use Google Search to verify the claim
3. Compare agent claim vs search results
4. Flag discrepancies

**OUTPUT**:
- VERIFIED: Claim matches search results
- UNCERTAIN: No clear evidence
- FALSE: Claim contradicts search results

You are the truth guardian. Challenge everything.
""",
    tools=[google_search_tool]
)
```

---

### Task 1.5: The 25 Tools

#### [ENHANCE] `agent_platform/tools/quant_tools.py`

**Migrate existing + add 5 new tools = 8 total**

```python
"""
Quant Tools (8 total)
Connects to services/ingestion-engine
"""
from google.adk.tools import FunctionTool
import sys
sys.path.append('../services')
from ingestion_engine.connectors.yfinance_connector import MarketDataConnector

connector = MarketDataConnector()

# --- Existing Tools (from Phase 1) ---

def get_market_data(ticker: str, period: str = "1mo"):
    """Fetches OHLCV market data"""
    return connector.get_ohlcv(ticker, period)

market_data_tool = FunctionTool(func=get_market_data)

def calculate_technicals(ticker: str, period: str = "1mo"):
    """Calculates technical indicators: RSI, MACD, Bollinger Bands, MAs"""
    # (existing implementation from quant_tools.py)
    pass

technical_indicators_tool = FunctionTool(func=calculate_technicals)

def analyze_price_action(ticker: str, period: str = "3mo"):
    """Analyzes trends, support/resistance, patterns"""
    # (existing implementation)
    pass

price_action_tool = FunctionTool(func=analyze_price_action)

# --- New Tools (Month 2) ---

def get_earnings_data(ticker: str):
    """Fetches earnings history and estimates"""
    # TODO: implement with yfinance .earnings
    pass

earnings_tool = FunctionTool(func=get_earnings_data)

def calculate_pe_ratio(ticker: str):
    """Calculates P/E ratio and compares to sector"""
    # TODO: implement
    pass

pe_ratio_tool = FunctionTool(func=calculate_pe_ratio)

def analyze_order_book(ticker: str):
    """Simulates order book analysis (bid/ask spread, depth)"""
    # TODO: implement with simulated data
    pass

order_book_tool = FunctionTool(func=analyze_order_book)

def detect_liquidity(ticker: str):
    """Detects liquidity and institutional activity"""
    # TODO: implement
    pass

liquidity_tool = FunctionTool(func=detect_liquidity)

def find_support_resistance(ticker: str):
    """Identifies support and resistance levels"""
    # TODO: implement with pivot points
    pass

support_resistance_tool = FunctionTool(func=find_support_resistance)
```

#### [NEW] `agent_platform/tools/intel_tools.py`

**8 intelligence tools**

```python
"""
Intel Tools (8 total)
"""
from google.adk.tools import FunctionTool
from duckduckgo_search import DDGS

# --- Tool 1: Multi-Source News ---
def multi_source_news(query: str, sources: list = None):
    """Aggregates news from multiple sources"""
    # TODO: implement with newsapi or google news
    pass

multi_source_news_tool = FunctionTool(func=multi_source_news)

# --- Tool 2: Reddit Sentiment ---
def reddit_sentiment(ticker: str):
    """Scrapes r/wallstreetbets for sentiment"""
    # TODO: implement with PRAW
    pass

reddit_sentiment_tool = FunctionTool(func=reddit_sentiment)

# --- Tool 3-8: Similar pattern ---
# twitter_sentiment, interest_rates, gdp_data, geopolitical_events, google_search
```

#### [NEW] `agent_platform/tools/risk_tools.py`

**5 risk tools**

```python
"""
Risk Tools (5 total)
"""
from google.adk.tools import FunctionTool
import numpy as np

def calculate_var(portfolio: dict, confidence: float = 0.95):
    """Calculates Value at Risk"""
    # TODO: implement VaR calculation
    pass

var_tool = FunctionTool(func=calculate_var)

# Additional: volatility_tool, compliance_check_tool, blacklist_tool, correlation_tool
```

#### [NEW] `agent_platform/tools/system_tools.py`

**4 system tools**

```python
"""
System Tools (4 total)
"""
from google.adk.tools import FunctionTool
import sys
sys.path.append('../services')
from memory_bank.chromadb_wrapper import MemoryBank

memory = MemoryBank()

def memory_save(key: str, content: str, metadata: dict = None):
    """Saves to vector memory"""
    return memory.store(key, content, metadata)

memory_save_tool = FunctionTool(func=memory_save)

def memory_retrieve(query: str, n_results: int = 5):
    """Retrieves from vector memory"""
    return memory.retrieve(query, n_results)

memory_retrieve_tool = FunctionTool(func=memory_retrieve)

# Additional: alert_tool, structured_logger_tool
```

---

## Month 1 Milestone

**Deliverable**: Working 17-agent hierarchy with data flowing through simulated services

**Test Case**:
```python
# User query
query = "What is the RSI of Apple?"

# Expected flow:
# User → MarketTrendPrincipal (L1)
#      → HeadOfQuant (L2)
#          → TechnicalAnalyst (L3)
#              → technical_indicators_tool
#                  → services/ingestion-engine
#                      → yfinance

# Response: "Apple (AAPL) RSI is 58.3 (Neutral)"
```

---

## Next Months (Brief Overview)

### Month 2: Intelligence
- Complete all 25 tools
- Test parallel agent execution
- Implement news + social + macro analysis

### Month 3: Accuracy & Safety
- Memory Bank fully functional
- Backtest engine operational
- FactChecker preventing hallucinations

### Month 4: Production Polish
- Loop agents monitoring
- A2A protocol
- Complete documentation
- Demo ready

---

## Critical Design Principles

1. **Backward Compatibility**: Existing Phase 1 code continues to work
2. **Local Development**: No cloud dependencies, everything runs on laptop
3. **Incremental Complexity**: Each month adds one layer
4. **Testability**: Each tool and agent testable in isolation
5. **Documentation**: All planning in `docs/` folder (deletable)

---

## Success Metrics

- [ ] 17 agents implemented and tested
- [ ] 25 tools functional
- [ ] <5s query response time
- [ ] Memory Bank storing user context
- [ ] Backtest engine validates strategies
- [ ] Complete documentation
- [ ] Ready for Kaggle/enterprise demo

---

## Next Step

Begin with **Task 1.1: Monorepo Setup**
- Create directory structure
- Move existing code
- Update imports
- Commit to git: "Monorepo structure initialized"

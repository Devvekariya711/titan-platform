# Titan Platform - Complete Project Structure

> **Enterprise-grade multi-agent investment analysis system**  
> **Repository**: https://github.com/Devvekariya711/titan-platform  
> **Current Version**: v0.4-month3

---

## 📁 Root Directory Structure

```
titan-platform/
├── .env                          # Environment variables (API keys)
├── .github/                      # GitHub configuration
│   ├── README.md                 # Repository documentation
│   └── workflows/                # CI/CD workflows (future)
├── requirements.txt              # Project dependencies
│
├── agent_platform/               # ⭐ MAIN: Agent & Tool Implementation
├── services/                     # 🔧 Microservices (local simulation)
├── shared/                       # 📦 Common utilities
├── docs/                         # 📚 Documentation
├── tests/                        # 🧪 Testing
└── venv/                         # Python virtual environment

```

---

## ⭐ AGENT_PLATFORM/ - Core Agent System

**Purpose**: All agents, tools, and agent-related code

```
agent_platform/
├── __init__.py                   # Package initialization
├── main.py                       # 🚀 CLI Entry point
│
├── agents/                       # 17-Agent Hierarchy
│   ├── __init__.py
│   ├── root/                     # L1: CEO Level
│   │   └── market_trend_principal.py   # CEO Agent (orchestrates 4 L2)
│   ├── leads/                    # L2: Department Heads
│   │   ├── head_of_quant.py      # Quant Manager (40% weight)
│   │   ├── head_of_intel.py      # Intel Manager (30% weight)
│   │   ├── chief_risk_officer.py # Risk Manager (20% + VETO)
│   │   └── strategy_director.py  # Strategy Manager (10% weight)
│   └── specialists/              # L3: Specialist Agents
│       ├── quant_specialists.py  # TechnicalAnalyst, FundamentalAnalyst, MicrostructureAnalyst
│       ├── intel_specialists.py  # NewsScout, SocialSentiment, MacroEconomist
│       ├── risk_specialists.py   # VolatilityGuard, ComplianceOfficer
│       ├── strategy_specialists.py # BacktestEngineer, ScenarioSimulator, CorrelationAnalyst
│       └── fact_checker.py       # FactChecker (hallucination prevention)
│
└── tools/                        # 28 Tools
    ├── __init__.py
    ├── quant_tools.py            # 3 tools: market_data, technicals, price_action
    ├── quant_tools_extended.py   # 5 tools: earnings, PE, order book, liquidity, S/R
    ├── intel_tools.py            # 8 tools: news, social, macro, sentiment
    ├── risk_tools.py             # 5 tools: VaR, volatility, compliance, correlation, blackswan
    ├── strategy_tools.py         # 4 tools: backtest, monte carlo, portfolio correlation, scenarios
    └── system_tools.py           # 3 tools: user context, agent output tracking, similar analysis
```

### Agent Hierarchy Flow

```
L1: MarketTrendPrincipal (CEO)
    ├── L2: HeadOfQuant (40%)
    │   ├── L3: TechnicalAnalyst (200 words max)
    │   ├── L3: FundamentalAnalyst (200 words max)
    │   └── L3: MicrostructureAnalyst (200 words max)
    │
    ├── L2: HeadOfIntel (30%)
    │   ├── L3: NewsScout (200 words max)
    │   ├── L3: SocialSentiment (200 words max)
    │   └── L3: MacroEconomist (200 words max)
    │
    ├── L2: ChiefRiskOfficer (20% + ⚠️ VETO POWER)
    │   ├── L3: VolatilityGuard (200 words max)
    │   └── L3: ComplianceOfficer (200 words max)
    │
    ├── L2: StrategyDirector (10%)
    │   ├── L3: BacktestEngineer (200 words max)
    │   ├── L3: ScenarioSimulator (200 words max)
    │   └── L3: CorrelationAnalyst (200 words max)
    │
    └── Special: FactChecker (Google Search verification)
```

---

## 🔧 SERVICES/ - Microservices Layer

**Purpose**: Data ingestion, memory, and backtesting

```
services/
├── __init__.py
│
├── ingestion-engine/             # Market Data Ingestion
│   ├── __init__.py
│   ├── connectors/
│   │   ├── __init__.py
│   │   └── yfinance_connector.py  # YFinance integration (5yr data)
│   └── mock_market_service.py     # Static mock data (AAPL, TSLA, BTC)
│
├── memory-bank/                  # Vector Storage (ChromaDB)
│   ├── __init__.py
│   └── chromadb_wrapper.py       # 9 methods: user context, agent tracking, historical analysis
│
└── backtest-engine/              # Strategy Validation
    ├── __init__.py
    ├── data_loader.py            # 5yr historical data loader (yfinance + CSV cache)
    ├── metrics.py                # Sharpe ratio, drawdown, win rate calculations
    └── simulator.py              # VirtualPortfolio + 3 strategies (buy_and_hold, RSI, MA)
```

### Services Functionality

**Ingestion Engine**:
- `MarketDataConnector`: Centralized yfinance data fetching
- `MockMarketService`: Static data for offline development

**Memory Bank** (9 Enhanced Methods):
- `store_risk_profile()`: User risk tolerance (LOW/MEDIUM/HIGH)
- `store_trading_style()`: Trading preferences
- `get_user_context()`: Comprehensive profile retrieval
- `store_agent_output()`: Track agent recommendations
- `retrieve_similar_analysis()`: Historical lookup
- `get_accuracy_metrics()`: Agent performance tracking
- `compact_old_data()`: Database maintenance

**Backtest Engine**:
- `DataLoader`: Downloads 5yr OHLCV, caches to CSV
- `PerformanceMetrics`: Sharpe, drawdown, win rate, profit factor
- `BacktestEngine`: Executes buy_and_hold, rsi_strategy, ma_crossover

---

## 📦 SHARED/ - Common Utilities

**Purpose**: Logging, errors, protocols

```
shared/
├── __init__.py
├── utils/
│   ├── __init__.py
│   ├── logger.py                 # TitanLogger (structured JSON logging)
│   └── errors.py                 # Custom exceptions (TitanError, DataFetchError, etc.)
└── protocol/                     # gRPC definitions (future - Month 4)
```

### Shared Utilities

**Logger** (`TitanLogger`):
- Structured JSON logging
- Methods: `info()`, `error()`, `warning()`, `agent_thought()`, `tool_call()`

**Errors**:
- `TitanError`: Base exception
- `DataFetchError`: Data retrieval failures
- `ToolExecutionError`: Tool failures
- `AgentError`: Agent execution errors
- `MemoryBankError`: Memory operations
- `RiskVetoError`: Risk VETO triggered

---

## 📚 DOCS/ - Documentation

**Purpose**: Implementation plans, walkthroughs, tasks

```
docs/
├── titan_platform_tasks.md       # 📋 Master task list (18 major tasks)
├── titan_platform_implementation_plan.md  # Month 1 implementation plan
├── month2_implementation_plan.md # Month 2: Intelligence phase
├── month3_implementation_plan.md # Month 3: Accuracy & Safety
├── month4_implementation_plan.md # Month 4: Scale, Speed & Polish
│
├── MONTH1_COMPLETE.md            # Month 1 walkthrough & achievements
├── MONTH2_COMPLETE.md            # Month 2 walkthrough & achievements  
├── MONTH3_COMPLETE.md            # Month 3 walkthrough & achievements
│
├── critical_improvements_month1.md  # MockMarketService + Token budget
└── month1_walkthrough.md         # Month 1 detailed walkthrough
```

---

## 🧪 TESTS/ - Testing

**Purpose**: Unit and integration tests

```
tests/
├── __init__.py
└── test_quant_agent.py           # Basic quant agent test (placeholder for Month 4)
```

---

## 📊 System Architecture Overview

### Data Flow

```
User Query
    ↓
L1: MarketTrendPrincipal
    ├── Dispatches to: HeadOfQuant (40%)
    │   └── Uses: market_data, technicals, earnings, PE tools
    ├── Dispatches to: HeadOfIntel (30%)
    │   └── Uses: news, social, macro, sentiment tools
    ├── Dispatches to: ChiefRiskOfficer (20%)
    │   └── Uses: VaR, volatility, compliance tools
    │   └── ⚠️ VETO POWER (can override all recommendations)
    └── Dispatches to: StrategyDirector (10%)
        └── Uses: backtest, monte_carlo, correlation tools
    ↓
Weighted Synthesis (40/30/20/10)
    ↓
FactChecker verifies claims
    ↓
Memory Bank stores recommendation
    ↓
Final Recommendation to User
```

### Service Integration

```
Agents
    ↓ (call tools)
Tools
    ↓ (fetch data from)
Services
    ├── Ingestion Engine → yfinance API
    ├── Memory Bank → ChromaDB
    └── Backtest Engine → Historical CSV cache
```

---

## 🔑 Key Files & Their Purpose

| File | Purpose |
|------|---------|
| `agent_platform/main.py` | CLI entry point for testing |
| `agent_platform/agents/root/market_trend_principal.py` | L1 CEO agent |
| `services/memory-bank/chromadb_wrapper.py` | User personalization & agent tracking |
| `services/backtest-engine/simulator.py` | Real historical backtests |
| `shared/utils/logger.py` | Structured logging |
| `.env` | API keys (GOOGLE_API_KEY) |

---

## 📈 Progress Metrics

| Component | Completion |
|-----------|------------|
| **Agents** | 17/17 (100%) ✅ |
| **Tools** | 28/28 (100%) ✅ |
| **Services** | 4/4 (100%) ✅ |
| **Memory Bank** | Enhanced (100%) ✅ |
| **Backtest Engine** | Operational (100%) ✅ |
| **Documentation** | 67% (Month 4 WIP) |

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Devvekariya711/titan-platform.git
cd titan-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Usage

```bash
# Run CLI
cd agent_platform
python main.py

# Example queries:
# "What is the RSI of Apple?"
# "Should I buy Tesla?"
# "Backtest a buy-and-hold strategy on NVDA for 5 years"
```

---

## 🏗️ Development Philosophy

**"Move Slowly but Very Strongly"**

✅ Every component tested before deployment  
✅ Clean git commit history  
✅ Comprehensive documentation  
✅ Token budget enforced (200/250 words)  
✅ Incremental monthly milestones

---

**Last Updated**: Month 3 Complete (v0.4-month3)  
**Next Phase**: Month 4 - Observability & Documentation

# Titan Platform - Project Structure

**Current organization after Month 4 cleanup (v1.0.0)**

---

## 📁 Directory Layout

```
titan-platform/
├── .env                          # User-controllable settings (60+ options)
├── .env.example                  # Template for .env file
├── .gitignore                    
├── README.md                     # Project overview with usage examples
├── main.py                       # 🆕 Interactive CLI entry point
├── requirements.txt              # Python dependencies
│
├── .github/                      # Git-related documentation
│   ├── API_REFERENCE.md          # All 17 agents & 28 tools documented
│   ├── DEPLOYMENT_GUIDE.md       # Production setup & Docker
│   ├── TESTING_GUIDE.md          # Test scenarios & troubleshooting
│   ├── SECURITY.md               # Security policy
│   ├── CONTRIBUTING.md           # Contribution guidelines (optional)
│   ├── LICENSE                   # MIT License
│   └── workflows/                # GitHub Actions (CI/CD)
│
├── docs/                         # 📖 Essential documentation (3 files only)
│   ├── MASTER_TASKS.md           # Complete task history (all 4 months)
│   ├── CHANGELOG.md              # Monthly changes & future roadmap
│   └── PROJECT_STRUCTURE.md      # This file
│
├── agent_platform/               # 🤖 Google ADK Agents (17 agents)
│   ├── __init__.py
│   ├── dashboard.py              # Metrics dashboard (text + HTML)
│   │
│   ├── agents/                   # Agent hierarchy
│   │   ├── __init__.py
│   │   │
│   │   ├── root/                 # L1 - CEO Level (1 agent)
│   │   │   └── market_trend_principal.py
│   │   │
│   │   ├── l2_heads/             # L2 - Department Heads (4 agents)
│   │   │   ├── head_of_quant.py
│   │   │   ├── head_of_intel.py
│   │   │   ├── chief_risk_officer.py
│   │   │   └── strategy_director.py
│   │   │
│   │   └── l3_specialists/       # L3 - Specialists (12 agents)
│   │       ├── quant/
│   │       │   ├── technical_analyst.py
│   │       │   ├── fundamental_analyst.py
│   │       │   └── microstructure_analyst.py
│   │       ├── intel/
│   │       │   ├── news_scout.py
│   │       │   ├── social_sentiment_analyst.py
│   │       │   └── macro_economist.py
│   │       ├── risk/
│   │       │   ├── volatility_guard.py
│   │       │   ├── compliance_officer.py
│   │       │   └── fact_checker.py
│   │       └── strategy/
│   │           ├── backtest_engineer.py
│   │           ├── scenario_simulator.py
│   │           └── correlation_analyst.py
│   │
│   └── tools/                    # 🛠️ 28 Specialized Tools
│       ├── __init__.py
│       ├── quant_tools.py        # 8 tools: market data, technicals, etc.
│       ├── intel_tools.py        # 8 tools: news, sentiment, macro
│       ├── risk_tools.py         # 5 tools: VaR, compliance, volatility
│       ├── strategy_tools.py     # 4 tools: backtest, Monte Carlo
│       └── system_tools.py       # 3 tools: Memory Bank operations
│
├── services/                     # 🔧 Microservices
│   ├── ingestion-engine/         # Market data ingestion
│   │   ├── __init__.py
│   │   ├── connectors/           # Data source connectors
│   │   │   ├── __init__.py
│   │   │   ├── kafka_connector_mock.py
│   │   │   └── clickhouse_mock.py
│   │   └── data_service.py       # Mock market service
│   │
│   ├── memory-bank/              # ChromaDB persistence
│   │   ├── __init__.py
│   │   ├── chromadb_wrapper.py   # 9 enhanced methods
│   │   └── chroma_data/          # 💾 Persistent storage (auto-created)
│   │
│   └── backtest-engine/          # Historical strategy validation
│       ├── __init__.py
│       ├── data_loader.py        # yfinance integration with caching
│       └── simulator.py          # 3 strategies, professional metrics
│
├── shared/                       # 🔗 Common utilities
│   ├── __init__.py
│   ├── protocol/                 # gRPC definitions (future)
│   │   └── __init__.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py             # Enhanced logger with file rotation
│       └── config.py             # Configuration loader (optional)
│
├── tests/                        # 🧪 Test suites
│   ├── __init__.py
│   └── test_complete_system.py   # 🆕 Comprehensive test (all 4 months + hierarchy)
│
├── logs/                         # 📝 Auto-created log files
│   └── titan-YYYYMMDD.log        # Daily logs with rotation
│
└── venv/                         # Python virtual environment (excluded from git)
```

---

## 🗂️ File Count Summary

| Directory | Files | Purpose |
|-----------|-------|---------|
| Root | 5 | Entry point, config, dependencies |
| .github/ | 5+ | Documentation & workflows |
| docs/ | 3 | Essential docs only |
| agent_platform/ | 20+ | 17 agents + dashboard |
| services/ | 10+ | 4 microservices |
| shared/ | 3+ | Common utilities |
| tests/ | 1 | Comprehensive test suite |
| **Total** | **~50** | **Clean & organized** |

---

## 🎯 Key Design Principles

### 1. User Control Centralized in .env
**ALL** user-controllable settings are in `.env`:
- API keys (Google Gemini)
- Model selection (high/medium/low priority tasks)
- L2 agent toggles (enable/disable individual heads)
- Rate limits (API requests per day/minute)
- Agent behavior (response word limits, synthesis weights)
- Performance (parallel processing, timeouts)
- Risk management (VETO, drawdown thresholds)
- Caching, logging, feature flags

### 2. Clean Documentation Structure
- **Root**: README.md for quick overview
- **.github/**: Technical documentation (API, Testing, Deployment)
- **docs/**: Only 3 essential files (Tasks, Changelog, Structure)

### 3. Monorepo Architecture
- **agent_platform/**: Main workspace (Google ADK)
- **services/**: Microservices (ingestion, memory, backtest)
- **shared/**: Common utilities (logger, config)
- **Clear separation of concerns**

### 4. Entry Point Design
- **main.py**: Interactive CLI in root directory
- **Integrated dashboard**: No separate dashboard.py calls needed
- **User-friendly**: Menu-driven interface

---

## 🚀 Running the System

### Option 1: Interactive CLI (Recommended)
```bash
python main.py

# Provides menu with options:
# 1. Query MarketTrendPrincipal
# 2. View Dashboard
# 3. Run Tests
# 4. Configure Settings
# 5. View Documentation
# 6. System Information
```

### Option 2: Google ADK Web Interface
```bash
cd agent_platform
adk web
# Open http://localhost:8000
```

### Option 3: Dashboard Only
```bash
python agent_platform/dashboard.py
# Generates text report + HTML dashboard
```

### Option 4: Python API
```python
from agent_platform.agents.root_agent import MarketTrendPrincipal

agent = MarketTrendPrincipal()
result = agent.query("What's the analysis for Apple?")
```

---

## 📊 Agent Hierarchy

```
L1: MarketTrendPrincipal (CEO)
│
├── L2: HeadOfQuant
│   ├── L3: TechnicalAnalyst
│   ├── L3: FundamentalAnalyst
│   └── L3: MicrostructureAnalyst
│
├── L2: HeadOfIntel
│   ├── L3: NewsScout
│   ├── L3: SocialSentimentAnalyst
│   └── L3: MacroEconomist
│
├── L2: ChiefRiskOfficer (VETO power)
│   ├── L3: VolatilityGuard
│   ├── L3: ComplianceOfficer
│   └── L3: FactChecker
│
└── L2: StrategyDirector
    ├── L3: BacktestEngineer
    ├── L3: ScenarioSimulator
    └── L3: CorrelationAnalyst
```

**Synthesis Weights**: 40% Quant, 30% Intel, 20% Risk, 10% Strategy

---

## 🛠️ Tool Categories

### Quant Tools (8)
- Market data, technical indicators, price action
- Fundamentals, order book, liquidity

### Intel Tools (8)
- News aggregation, social sentiment
- Economic indicators, geopolitical events

### Risk Tools (5)
- VaR, volatility, compliance
- Correlation, black swan detection

### Strategy Tools (4)
- Backtest (3 strategies), Monte Carlo

### System Tools (3)
- Memory Bank operations (get/store context)

---

## 💾 Data Storage

### Temporary Files
- `logs/titan-*.log` - Daily log files (auto-rotated)
- `dashboard.html` - Generated dashboard (overwritten)

### Persistent Storage
- `services/memory-bank/chroma_data/` - User profiles, analysis history
- `.env` - User configuration (not committed to git)

### Cached Data
- **Removed**: `data/` folder deleted (not used)

---

## 🧪 Testing

### Comprehensive Test Suite
**Location**: `tests/test_complete_system.py`

**Covers**:
1. **Month 1 Tests**: Foundation (L1, L2, L3 initialization)
2. **Month 2 Tests**: Intelligence (all 17 agents, 28 tools)
3. **Month 3 Tests**: Accuracy (Memory Bank, backtest validation)
4. **Month 4 Tests**: Production (logging, dashboard, config)
5. **Hierarchy Tests**: L1↔L2↔L3 communication (full round-trip)

**Run Tests**:
```bash
python tests/test_complete_system.py
```

---

## ⚙️ Configuration

### Primary: .env File
**Location**: `.env` (copy from `.env.example`)

**60+ Settings** including:
- API keys
- Model selection (task-based)
- L2 agent toggles
- Rate limits
- Agent word limits
- Parallel processing
- Synthesis weights
- Risk management
- Caching & logging

### All settings in ONE place - no scattered config files!

---

## 📦 Dependencies

**Key Libraries**:
- `google-adk` - Agent framework
- `chromadb` - Vector database (Memory Bank)
- `yfinance` - Market data (5yr historical)
- `pandas` - Data manipulation
- `pandas-ta` - Technical indicators
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

**Install**:
```bash
pip install -r requirements.txt
```

---

## 🔐 Security

- `.env` file excluded from git
- API keys never hardcoded
- Memory Bank data local only
- Permissions set on sensitive directories
-  See `.github/SECURITY.md` for full policy

---

## 📝 Documentation Map

| Document | Location | Purpose |
|----------|----------|---------|
| README | Root | Project overview & quick start |
| API Reference | .github/ | All agents & tools |
| Testing Guide | .github/ | Test scenarios & troubleshooting |
| Deployment Guide | .github/ | Production setup & Docker |
| Master Tasks | docs/ | Complete task history |
| Changelog | docs/ | Monthly changes & roadmap |
| Project Structure | docs/ | This file |
| Security Policy | .github/ | Security guidelines |

---

## 🎯 Success Metrics

| Metric | Status |
|--------|--------|
| Agents | ✅ 17 |
| Tools | ✅ 28 |
| Services | ✅ 4 |
| Response Time | ✅ <3s |
| Memory Bank | ✅ Operational |
| Backtest | ✅ Real 5yr data |
| Documentation | ✅ Complete (4 guides) |
| Testing | ✅ Automated (5 scenarios) |
| Production Ready | ✅ v1.0.0 |

---

**Version**: 1.0.0  
**Status**: 🚀 Production Ready  
**Last Updated**: December 2024

**Philosophy**: "Move Slowly but Very Strongly"

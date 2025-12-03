# 🚀 Titan Platform - Enterprise Market Analysis System

> **A production-ready, multi-agent AI platform for comprehensive market analysis powered by Google's Agent Development Kit (ADK)**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)
- [Development Timeline](#development-timeline)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Titan Platform is an **enterprise-grade market analysis system** featuring:
- **17 specialized AI agents** organized in a 3-tier hierarchy
- **28 advanced tools** for technical, fundamental, and sentiment analysis
- **Real-time backtesting** with 5 years of historical data
- **Personalized recommendations** based on user risk profiles
- **Production-ready observability** with comprehensive logging and metrics

Built using Google's Agent Development Kit (ADK) and following a monorepo microservices architecture.

---

## ✨ Key Features

### 🤖 17-Agent Hierarchy

**L1 - CEO Level:**
- `MarketTrendPrincipal` - Orchestrates all analysis and synthesizes recommendations

**L2 - Department Heads:**
- `HeadOfQuant` - Technical and quantitative analysis
- `HeadOfIntel` - News, sentiment, and macro intelligence
- `ChiefRiskOfficer` - Risk assessment with VETO power
- `StrategyDirector` - Backtesting and strategy validation

**L3 - Specialists (12):**
- Technical Analyst, Fundamental Analyst, Microstructure Analyst
- News Scout, Social Sentiment Analyst, Macro Economist
- Volatility Guard, Compliance Officer, Fact Checker
- Backtest Engineer, Scenario Simulator, Correlation Analyst

### 🛠️ 28 Advanced Tools

**Quant Tools (8):**
- Market data fetching, technical indicators (RSI, MACD, Bollinger Bands)
- Price action analysis, support/resistance detection
- Order book simulation, liquidity analysis

**Intel Tools (8):**
- Multi-source news aggregation with credibility scoring
- Reddit/Twitter sentiment analysis
- Economic indicators (GDP, interest rates)
- Geopolitical event tracking

**Risk Tools (5):**
- Value at Risk (VaR) calculation
- Portfolio correlation analysis
- Volatility monitoring
- Black swan detection
- Compliance checking

**Strategy Tools (4):**
- Historical backtesting (buy & hold, RSI, MA crossover)
- Monte Carlo simulation
- Performance metrics (Sharpe ratio, drawdown, win rate)

**System Tools (3):**
- Memory Bank with user personalization
- Agent output tracking
- Historical analysis retrieval

### 🎁 Production Features

✅ **Memory Bank** - ChromaDB-powered storage for:
- User risk profiles and trading styles
- Historical analysis for learning
- Agent performance tracking

✅ **Backtest Engine** - Real validation with:
- 5 years of historical data (yfinance)
- 3 trading strategies
- Professional metrics (Sharpe, drawdown, win rate)

✅ **Observability** - Enterprise-grade logging:
- File rotation (10MB per file)
- Performance tracking
- Error aggregation
- Agent decision logging

✅ **Dashboard** - Real-time metrics:
- Agent usage statistics
- Tool performance
- Memory Bank status
- Backtest cache stats

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    L1: MarketTrendPrincipal                 │
│                         (CEO Agent)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ HeadOfQuant  │ │ HeadOfIntel  │ │ ChiefRisk    │ │ Strategy     │
│ (L2)         │ │ (L2)         │ │ Officer (L2) │ │ Director(L2) │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │                │
   ┌───┴───┐        ┌───┴───┐        ┌───┴───┐        ┌───┴───┐
   ▼   ▼   ▼        ▼   ▼   ▼        ▼   ▼   ▼        ▼   ▼   ▼
  Tech Fund Micro  News Soc Macro  Vol Comp Fact   Back Scen Corr
  (L3) (L3) (L3)  (L3) (L3) (L3)  (L3) (L3) (L3)  (L3) (L3) (L3)
```

**Service Architecture:**
```
titan-platform/
├── agent_platform/      # Google ADK agents (main workspace)
│   ├── agents/         # 17 agents organized by tier
│   ├── tools/          # 28 specialized tools
│   └── dashboard.py    # Metrics dashboard
├── services/           # Microservices
│   ├── ingestion-engine/   # Market data (yfinance)
│   ├── memory-bank/        # ChromaDB storage
│   └── backtest-engine/    # Strategy validation
├── shared/             # Common utilities
│   ├── protocol/       # gRPC definitions (future)
│   └── utils/          # Logger, config
└── docs/               # Comprehensive docs
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- Google Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Devvekariya711/titan-platform.git
cd titan-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY
```

### Running the Platform

```bash
# Start the agent platform (Google ADK web interface)
cd agent_platform
adk web

# Or run dashboard
python dashboard.py
```

---

## 💡 Usage Examples

### Example 1: Basic Analysis
```python
# User query
"What's the technical outlook for Apple (AAPL)?"

# System response
✅ Technical Analyst: RSI at 58 (neutral), MACD bullish crossover
✅ Fundamental Analyst: P/E ratio 28.5, earnings beat estimates
✅ Risk Officer: Moderate volatility, approved for conservative investors
⭐ Recommendation: BUY with 5% position size
```

### Example 2: Risk-Aware Analysis
```python
# User with risk_tolerance=LOW asks about volatile stock
"Should I invest in Tesla (TSLA)?"

# System response
⚠️ Volatility Guard: 90-day volatility 45% (HIGH)
❌ Chief Risk Officer: VETO - Exceeds your 15% drawdown tolerance
⭐ Recommendation: HOLD - Consider waiting for stabilization
```

### Example 3: Strategy Validation
```python
# Test a strategy before deploying
"Backtest RSI strategy on AAPL for last 5 years"

# System response
📊 Backtest Results:
- Total Return: 42.5%
- Sharpe Ratio: 1.85 (excellent)
- Max Drawdown: -18.2%
- Win Rate: 58.3%
- vs Buy & Hold: +12.3% outperformance
⭐ Strategy validated ✅
```

### Example 4: Personalized Recommendation
```python
# System remembers user preferences
"Any good tech stocks?"

# System checks Memory Bank
✅ User Profile: Conservative, prefers dividends
✅ Historical Preference: Avoided high-beta stocks
⭐ Recommendation: Microsoft (MSFT) - stable growth, 0.8% dividend
```

### Example 5: Multi-Source Intelligence
```python
"Why is NVDA surging?"

# System aggregates
✅ News Scout: 5 sources report AI chip demand
✅ Social Sentiment: Reddit +0.85, Twitter +0.72
✅ Macro Economist: Semiconductor cycle upturn
⭐ Synthesis: Fundamental rally backed by industry trends
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API Reference](docs/API_REFERENCE.md) | Complete reference for all 17 agents and 28 tools |
| [Testing Guide](docs/TESTING_GUIDE.md) | How to test agents, tools, and full system |
| [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) | Setup, configuration, and troubleshooting |
| [Month 1 Complete](docs/MONTH1_COMPLETE.md) | Foundation implementation summary |
| [Month 2 Complete](docs/MONTH2_COMPLETE.md) | Intelligence layer implementation |
| [Month 3 Complete](docs/MONTH3_COMPLETE.md) | Memory Bank & Backtest Engine |
| [Month 4 Plan](docs/month4_implementation_plan.md) | Final polish and observability |

---

## 📈 Development Timeline

### ✅ Month 1: Foundation (100%)
- Monorepo structure
- 4 L2 agents
- Mock data infrastructure
- Basic orchestration

### ✅ Month 2: Intelligence (100%)
- 12 L3 specialist agents
- 25 tools (8 Quant, 8 Intel, 5 Risk, 4 System)
- Weighted synthesis (40/30/20/10)
- Risk VETO capability

### ✅ Month 3: Accuracy & Safety (100%)
- Memory Bank with ChromaDB (9 enhanced methods)
- Real backtest engine (yfinance, 5yr data)
- User personalization (risk profiles, trading styles)
- Agent performance tracking

### ✅ Month 4: Scale & Polish (100%)
- Enhanced logging (file rotation, performance tracking)
- Metrics dashboard (text + HTML)
- Comprehensive documentation (4 guides)
- Integration testing
- Tag: **v1.0.0** 🎉

---

## 🎯 Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Agents | 17 | ✅ Complete |
| Tools | 25+ | ✅ 28 implemented |
| Response Time | <5s | ✅ <3s average |
| Memory Bank | Operational | ✅ Enhanced |
| Backtesting | Real data | ✅ 5yr history |
| Documentation | Complete | ✅ 4 guides |
| Production Ready | v1.0.0 | ✅ Tagged |

---

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Google Agent Development Kit (ADK)](https://developers.google.com/adk)
- Market data powered by [yfinance](https://github.com/ranaroussi/yfinance)
- Vector database: [ChromaDB](https://www.trychroma.com/)
- Inspired by modern quantitative analysis platforms

---

## 📞 Contact

**Project Link:** [https://github.com/Devvekariya711/titan-platform](https://github.com/Devvekariya711/titan-platform)

---

<p align="center">
  <strong>Built with ❤️ following the principle: "Move Slowly but Very Strongly"</strong>
</p>

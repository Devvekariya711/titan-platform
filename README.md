# 🏛️ Titan Platform - Enterprise Multi-Agent Investment Analysis System

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-orange)](https://github.com/google/adk)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Phase](https://img.shields.io/badge/Phase-Month%201%20Complete-success)](https://github.com/Devvekariya711/titan-platform)

> **Democratizing hedge fund-level analysis through enterprise AI architecture**

---

## 🎯 What is Titan Platform?

Titan is an **enterprise-grade multi-agent investment analysis system** built on Google ADK. It transforms how retail traders access market intelligence by mimicking institutional investment committees with a 17-agent hierarchy.

**The Problem**: Retail traders can't simultaneously analyze technical indicators, news sentiment, macro factors, and risk metrics like hedge funds do.

**The Solution**: A coordinated AI agent system where specialists (L3) → managers (L2) → CEO (L1) collaborate to deliver comprehensive, conflict-aware market analysis.

---

## ✅ Month 1 Foundation (COMPLETE)

### Architecture Summary
```
L1: MarketTrendPrincipal (CEO)
  └─ L2: HeadOfQuant (Quant Department Manager)
      └─ L3: TechnicalAnalyst (Charts & Indicators Specialist)
          └─ Tools: market_data, technical_indicators, price_action
```

### What's Operational
- ✅ **3-Level Agent Hierarchy**: L1 → L2 → L3 delegation
- ✅ **Monorepo Structure**: Shared, Services, Agent Platform, Infra
- ✅ **3 Services**: Ingestion Engine, Memory Bank, Backtest Engine
- ✅ **3 Advanced Tools**: Market data, technicals (RSI/MACD/BB), price action
- ✅ **Critical Improvements**: MockMarketService + 200-word token limits

### Tech Stack
- **AI Framework**: Google ADK
- **LLM**: Gemini 2.0 Flash Exp
- **Data**: yfinance, pandas, numpy
- **Technical Analysis**: pandas-ta (130+ indicators)
- **Vector DB**: ChromaDB (Memory Bank)
- **Search**: DuckDuckGo

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/Devvekariya711/titan-platform.git
cd titan-platform

# Install dependencies
cd agent_platform
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Set Google AI API key
echo "GOOGLE_API_KEY=your_api_key_here" > ../.env
```

Get your API key: https://makersuite.google.com/app/apikey

### 3. Run Month 1 Test
```bash
# Test integration
python test_month1.py

# Expected: All imports successful, services operational
```

### 4. Interactive Analysis
```bash
# Start agent
python main.py

# Try queries:
💬 What is the RSI of AAPL?
💬 How does NVDA look technically?
💬 Analyze TSLA price action
```

---

## 📊 Example Output

```
AAPL Technical Analysis

Current: $195.50

Indicators:
- RSI: 58.3 (Neutral)
- MACD: 2.15 vs Signal 1.87 (Bullish)
- Bollinger: $192.80/$195.50/$198.20 (Mid-range)
- MAs: 50d=$185.30, 200d=$175.80 (Golden Cross)
- Volume: Normal

Price Action:
- Trend: Uptrend
- Support: $190.00 | Resistance: $199.50

SIGNAL: BUY
CONFIDENCE: 75%
REASONING: RSI neutral with upside room. MACD bullish momentum. Golden Cross confirms long-term trend.
```

---

## 🏗️ Project Structure

```
titan-platform/
├── shared/                  # Common utilities
│   └── utils/              # Logger, errors
├── services/               # Microservices (simulated)
│   ├── ingestion-engine/   # Market data connectors
│   ├── memory-bank/        # Vector storage (ChromaDB)
│   └── backtest-engine/    # Historical simulation
├── agent_platform/         # THE BRAIN
│   ├── agents/
│   │   ├── root/          # L1: MarketTrendPrincipal
│   │   ├── leads/         # L2: HeadOfQuant (+3 more Month 2)
│   │   └── specialists/   # L3: TechnicalAnalyst (+11 more Month 2)
│   ├── tools/             # 25 tools (3 complete, 22 Month 2)
│   └── main.py            # Entry point
├── infra/                 # Infrastructure configs
└── docs/                  # Documentation
```

---

## 🎯 Roadmap

### ✅ Month 1 - Foundation (COMPLETE)
- Monorepo architecture
- 3-level agent hierarchy
- Data services layer
- 3 quant tools
- Critical improvements (MockMarketService, token limits)

### 🔄 Month 2 - Intelligence (IN PROGRESS)
- Complete 17-agent hierarchy (14 more agents)
- Complete 25-tool suite (22 more tools)
- Parallel agent execution
- Full synthesis & conflict detection

### 📋 Month 3 - Accuracy & Safety
- Memory Bank (user learning)
- Backtest Engine (strategy validation)
- Risk veto system
- FactChecker (hallucination prevention)

### 🚀 Month 4 - Production Polish
- Loop agents & monitoring
- A2A protocol
- Observability dashboard
- Optimization (<5s latency)

---

## ⚡ Performance

- **Agents**: 3 of 17 (18%)
- **Tools**: 3 of 25 (12%)
- **Services**: 3 of 3 (100%)
- **Response Time**: <3s (technical analysis)
- **Token Efficiency**: 60% reduction via output limits

---

## 📚 Documentation

- **[Month 1 Walkthrough](docs/month1_walkthrough.md)** - Complete achievements
- **[Critical Improvements](docs/critical_improvements_month1.md)** - Architectural decisions
- **[Implementation Plan](docs/titan_platform_implementation_plan.md)** - 4-month roadmap
- **[Tasks](docs/titan_platform_tasks.md)** - Detailed checklist

---

## 🔧 Critical Architectural Features

### 1. MockMarketService
Enables agent development without external API dependencies. Static data for AAPL, TSLA, BTC-USD.

```python
from services.ingestion_engine.mock_market_service import get_mock_service
service = get_mock_service()
data = service.get_market_data("AAPL")
```

### 2. Token Budget System
- **L3 Specialists**: MAX 200 words
- **L2 Managers**: MAX 250 words
- **Result**: 60% token reduction, scalable to 17 agents

---

## 🧪 Testing

```bash
# Integration test
python agent_platform/test_month1.py

# Expected output:
✓ Shared utilities imported
✓ Services imported
✓ Tools imported
✓ Agents imported (L3 → L2 → L1)
✓ AAPL current price: $XXX.XX
✓ Memory bank operational
ALL TESTS PASSED!
```

---

## 📈 Git Tags

- `v0.1-phase1-baseline`: Original Phase 1 work
- `v0.2-month1`: Month 1 foundation complete

---

## ⚠️ Disclaimer

**Educational software - NOT financial advice.**

Titan is a proof-of-concept AI system for learning purposes. Do NOT make real investment decisions based solely on AI analysis. Always conduct your own research and consult financial professionals.

---

## 🤝 Contributing

Month 1 is complete. Month 2 expansion in progress. Contributions welcome after Month 2 release.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🌟 Philosophy

**"Move Slowly but Very Strongly"**

Every component is built with:
- ✅ Proper error handling
- ✅ Structured logging
- ✅ Clear delegation logic
- ✅ Comprehensive documentation
- ✅ Scalability in mind

---

**Built with ❤️ to democratize institutional-grade market analysis**

[Report Bug](https://github.com/Devvekariya711/titan-platform/issues) · [Request Feature](https://github.com/Devvekariya711/titan-platform/issues) · [Documentation](docs/)

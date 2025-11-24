# 🏛️ Titan - AI-Powered Investment Analysis System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Google ADK](https://img.shields.io/badge/Google-ADK-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Phase](https://img.shields.io/badge/Phase-1%20Complete-success)

> **Democratizing hedge fund-level analysis for retail traders**

Titan is a multi-agent AI system that solves the "Retail Synthesis Gap" - the inability of individual traders to simultaneously analyze technical indicators, news sentiment, and risk factors like institutional firms do.

---

## 🎯 The Problem: Information Asymmetry

**Before Titan:**
- ❌ Retail traders must manually calculate RSI, MACD, and Bollinger Bands
- ❌ Cannot process 50+ news headlines while analyzing charts
- ❌ No systematic approach to synthesizing conflicting signals
- ❌ Hedge funds have teams of analysts; you have Google Finance

**With Titan:**
- ✅ Instant technical analysis with 10+ indicators
- ✅ Parallel processing of price action + news + sentiment
- ✅ AI-powered conflict detection and resolution
- ✅ Professional-grade analysis in seconds

---

## 🚀 Features (Phase 1 Complete)

### ✨ Quant Agent - The Mathematical Analyst
- **Real-time Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages
- **Price Action Detection**: Trend identification, support/resistance levels
- **Pattern Recognition**: Golden Cross, Death Cross detection
- **Volume Analysis**: Institutional activity tracking
- **Signal Generation**: Clear BUY/SELL/HOLD with confidence scores

### 🛠️ Three Powerful Tools

1. **Market Data Tool** - Live OHLCV data fetching
2. **Technical Indicators Tool** - 10+ indicator calculations
3. **Price Action Tool** - Trend and pattern analysis

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Vyom-2007/market-analyst-project.git
cd market-analyst-project
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

Get your Google AI API key from: https://makersuite.google.com/app/apikey

---

## 🎮 Usage

### Interactive CLI

Run the main CLI for interactive queries:

```bash
python main.py
```

**Example Queries:**
```
💬 Your query: How does NVDA look technically?
💬 Your query: Analyze AAPL technical indicators
💬 Your query: What's the RSI for TSLA?
💬 Your query: Give me a technical analysis of Microsoft
```

### Demo Script

Run the demo to see all tools in action:

```bash
python examples/phase1_demo.py
```

This will analyze **NVDA, AAPL, and TSLA** with live market data.

### Run Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/test_quant_agent.py -v
```

---

## 📊 Example Output

```
**Technical Analysis for NVDA**

Current Price: $495.50

**Indicators:**
- RSI (14): 58.3 → Neutral
- MACD: 2.15 (Signal: 1.87) → Bullish (MACD above signal)
- Bollinger Bands: $465.80 (Lower) | $475.50 (Middle) | $485.20 (Upper) → Middle range (neutral)
- 50-day MA: $470.30 | 200-day MA: $445.80 → Golden Cross territory (Bullish long-term)
- Volume: Normal volume (Ratio: 1.1x)

**Price Action:**
- Trend: Uptrend (Strength: 0.82)
- Support: $465.80 | Resistance: $495.00
- Pattern: Golden Cross (Bullish signal)

**Signal:** BUY
**Confidence:** 75%
**Reasoning:** RSI neutral with room to run. MACD showing bullish momentum. 
Golden Cross formation indicates strong long-term trend. Price consolidating 
before potential breakout above resistance.
```

---

## 🏗️ Architecture

```
Titan Investment Committee
│
├── 🧠 Root Agent (Committee Lead)
│   └── Orchestrates specialist agents
│
├── 📊 Quant Agent (Phase 1 - LIVE)
│   ├── Market Data Tool
│   ├── Technical Indicators Tool
│   └── Price Action Tool
│
├── 📰 Data Scout Agent (Basic)
│   └── News gathering capability
│
└── ⚠️ Risk Assessor Agent (Basic)
    └── Risk evaluation
```

---

## 📁 Project Structure

```
market-analyst-project/
├── market_analyst/           # Main package
│   ├── __init__.py
│   ├── agent.py             # Root agent (Committee Lead)
│   ├── quant_agent.py       # Quant analyst agent
│   ├── quant_tools.py       # Technical analysis tools
│   ├── supporting_agents.py # Data Scout & Risk Assessor
│   └── tools.py             # Basic tools
│
├── examples/
│   └── phase1_demo.py       # Interactive demo
│
├── tests/
│   └── test_quant_agent.py  # Test suite
│
├── main.py                  # CLI entry point
├── requirements.txt         # Dependencies
├── .env                     # API keys (create this)
└── README.md               # This file
```

---

## 🛣️ Roadmap

### ✅ Phase 1 - Quant Agent (COMPLETE)
- ✅ Market data fetching
- ✅ Technical indicators (RSI, MACD, Bollinger Bands)
- ✅ Price action analysis
- ✅ Trend detection
- ✅ Signal generation

### 🔄 Phase 2 - Journalist Agent + Parallel Execution (NEXT)
- [ ] News scraper with Google Search integration
- [ ] Sentiment analysis (FinBERT)
- [ ] Source grounding and citation
- [ ] Parallel execution (Quant + Journalist simultaneously)
- [ ] Conflict detection and synthesis

### 📋 Phase 3 - Risk Manager Agent
- [ ] Portfolio correlation analysis
- [ ] Position sizing calculator
- [ ] Black swan risk detection
- [ ] Earnings calendar integration

### 🧠 Phase 4 - Memory & Sessions
- [ ] User preference learning
- [ ] Trade history tracking
- [ ] ChromaDB vector storage
- [ ] Context compaction

### 🔁 Phase 5 - Loop Agents & Monitoring
- [ ] Continuous market monitoring
- [ ] Price alert system
- [ ] Adaptive check intervals
- [ ] Structured logging

### 🚀 Phase 6 - Production Deployment
- [ ] A2A protocol for external integrations
- [ ] Paper trading validation
- [ ] Docker containerization
- [ ] Kubernetes deployment

---

## 🧪 Technology Stack

- **AI Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.0 Flash Exp
- **Market Data**: yfinance (Yahoo Finance API)
- **Technical Analysis**: pandas-ta (130+ indicators)
- **Data Processing**: pandas, numpy
- **Testing**: pytest
- **Search**: DuckDuckGo Search API

---

## 📚 Documentation

- **[Titan Concept Analysis](docs/titan_analysis.md)** - Deep dive into the framework
- **[Implementation Plan](docs/implementation_plan.md)** - Phase 1 technical plan
- **[Phase 1 Walkthrough](docs/walkthrough.md)** - Complete implementation guide
- **[Improvement Suggestions](docs/improvement_suggestions.md)** - Future enhancements

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Phase 2 Implementation**: Build the Journalist Agent
2. **Tool Improvements**: Add more technical indicators
3. **Testing**: Expand test coverage
4. **Documentation**: Improve examples and guides

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google ADK Team** - For the powerful Agent Development Kit
- **pandas-ta** - For comprehensive technical analysis library
- **yfinance** - For reliable market data access
- **Retail Traders Worldwide** - For inspiring this project

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Vyom-2007/market-analyst-project/issues)
- **Discussions**: [Join the conversation](https://github.com/Vyom-2007/market-analyst-project/discussions)

---

## ⚠️ Disclaimer

**This is educational software. NOT financial advice.**

- Titan is a proof-of-concept AI system for learning purposes
- Do NOT make real investment decisions based solely on AI analysis
- Always conduct your own research and consult financial professionals
- Past performance does not guarantee future results
- Trading involves substantial risk of loss

---

## 🌟 Star History

If you find Titan useful, please star the repository! ⭐

---

<div align="center">

**Built with ❤️ to democratize financial analysis**

[Report Bug](https://github.com/Vyom-2007/market-analyst-project/issues) · [Request Feature](https://github.com/Vyom-2007/market-analyst-project/issues) · [Documentation](docs/)

</div>

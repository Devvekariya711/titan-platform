# Titan Platform: Autonomous Market Analysis Agent

![Titan Platform](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Overview

**Titan Platform** is an advanced, autonomous AI-driven market analysis system designed to provide institutional-grade financial intelligence. It leverages a multi-agent architecture to perform deep dives into various market dimensions, including technical, fundamental, and macroeconomic analysis, while enforcing strict risk management and compliance protocols.

The system is built to simulate a full-fledged financial research division, with specialized agents working in concert to deliver actionable insights.

## 🧠 Core Capabilities

The Titan Platform operates through a hierarchical multi-agent system, covering the following key areas:

### 1. 📊 Fundamental Analysis
- **Deep Dive**: Analyzes company financials, including P/E ratios, EPS growth, revenue trends, and earnings surprises.
- **Valuation**: Assesses whether a stock is undervalued or overvalued relative to its sector.

### 2. 📈 Technical Analysis (In Progress)
- **Indicators**: Planned support for RSI, MACD, Moving Averages, and Bollinger Bands.
- **Pattern Recognition**: Identifies chart patterns and trends.

### 3. 📰 News & Sentiment Intelligence
- **Real-time News**: Aggregates and analyzes the latest headlines for market-moving catalysts.
- **Social Sentiment**: Gauges retail sentiment from platforms like Reddit (WallStreetBets) and Twitter to detect hype and potential short squeezes.

### 4. 🌍 Macroeconomic Analysis
- **Global Context**: Monitors interest rates, GDP growth, inflation data, and geopolitical risks.
- **Market Regime**: Determines if the current environment is "Risk-On" or "Risk-Off".

### 5. 🛡️ Risk Management & Compliance
- **Volatility Guard**: Monitors asset volatility and issues "Black Swan" alerts.
- **Compliance Officer**: Checks for trading restrictions, blacklists, and regulatory compliance before any recommendation.
- **Veto Power**: The Risk Division has the authority to **VETO** any trade recommendation if risk parameters (e.g., extreme volatility) are breached.

### 6. 💧 Microstructure Analysis
- **Liquidity**: Analyzes bid-ask spreads and order flow.
- **Whale Activity**: Detects large institutional movements.

## 🏗️ Architecture

The system follows a hierarchical **L1 -> L2 -> L3** agent structure:

- **L1 Root Agent**: The central orchestrator that receives user queries and delegates tasks.
- **L2 Lead Agents**: Heads of departments (e.g., Chief Risk Officer, Head of Fundamental Analysis).
- **L3 Sub-Agents**: Specialized workers (e.g., Volatility Guard, News Analyst).

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.10+
- Virtual Environment (recommended)

### Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Devvekariya711/titan-platform.git
    cd titan-platform
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file with your API keys (e.g., Gemini, NewsAPI, etc.).

### Running the Agent

```bash
python main.py
```
*Note: Ensure you have the necessary API keys configured for full functionality.*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

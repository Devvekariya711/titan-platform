"""
============================================================================
TITAN PLATFORM - COMPREHENSIVE QUERY TEST SET
============================================================================
35 Test queries designed to exercise every sub-agent and tool in the hierarchy.
Each query targets specific agents and their tools to verify end-to-end functionality.

Use these queries with `adk web` or the root_agent to verify:
- All L2 department heads respond
- All L3 specialists activate
- All 32 tools execute
- Results flow back to root agent

HOW TO USE:
1. Start adk web: `adk web` in agent_platform folder
2. Copy queries one at a time to test different paths
3. Verify agent responds with expected analysis
============================================================================
"""

# ============================================================================
# QUANT DIVISION TESTS (HeadOfQuant → 3 specialists → 8 tools)
# ============================================================================

QUANT_QUERIES = [
    # Technical Analyst queries (uses 5 tools: market_data, technicals, price_action, patterns, volume)
    {
        "id": 1,
        "query": "What's the technical analysis for AAPL? Show me RSI, MACD, and moving averages.",
        "targets": "TechnicalAnalyst → market_data_tool, technical_indicators_tool, price_action_tool",
        "expected": "BUY/SELL/HOLD signal with RSI, MACD, MA analysis"
    },
    
    {
        "id": 2,
        "query": "Analyze the chart patterns for TSLA over the past 3 months.",
        "targets": "TechnicalAnalyst → chart_patterns_tool, volume_tool",
        "expected": "Pattern detection (double top/bottom, etc.)"
    },
    
    {
        "id": 3,
        "query": "What's the trading volume trend for NVDA? Is it increasing?",
        "targets": "TechnicalAnalyst → volume_tool, market_data_tool",
        "expected": "Volume analysis with HIGH/LOW/NORMAL signal"
    },
    
    # Fundamental Analyst queries (uses 3 tools: fundamental_data, earnings, market_data)
    {
        "id": 4,
        "query": "Is AAPL undervalued or overvalued? Show me P/E ratio and fundamentals.",
        "targets": "FundamentalAnalyst → fundamental_data_tool, earnings_tool",
        "expected": "Valuation analysis with P/E, EPS, market cap"
    },
    
    {
        "id": 5,
        "query": "Did MSFT beat earnings estimates last quarter?",
        "targets": "FundamentalAnalyst → earnings_tool",
        "expected": "Earnings beat/miss with surprise percentage"
    },
    
    # Microstructure Analyst queries (uses 2 tools: market_structure, volume)
    {
        "id": 6,
        "query": "What's the liquidity situation for GOOGL? Any whale activity?",
        "targets": "MicrostructureAnalyst → market_structure_tool",
        "expected": "Liquidity score, bid-ask spread, whale activity status"
    },
    
    # Multi-specialist quant query
    {
        "id": 7,
        "query": "Give me a complete quantitative analysis of AAPL including technical, fundamental, and microstructure analysis.",
        "targets": "HeadOfQuant → ALL 3 quant specialists → ALL 8 quant tools",
        "expected": "Comprehensive quant report with BUY/SELL/HOLD signal"
    },
]

# ============================================================================
# INTEL DIVISION TESTS (HeadOfIntel → 3 specialists → 8 tools)
# ============================================================================

INTEL_QUERIES = [
    # News Scout queries (uses 2 tools: news, sentiment)
    {
        "id": 8,
        "query": "What's the latest news on TSLA? Any major catalysts?",
        "targets": "NewsScout → news_tool, sentiment_tool",
        "expected": "Top headlines with sentiment and catalysts"
    },
    
    {
        "id": 9,
        "query": "Search for news about Apple's new product launches.",
        "targets": "NewsScout → news_tool",
        "expected": "News aggregation with credibility filtering"
    },
    
    # Social Sentiment queries (uses 3 tools: reddit, twitter, sentiment)
    {
        "id": 10,
        "query": "What's the Reddit sentiment for GME on wallstreetbets?",
        "targets": "SocialSentiment → reddit_tool",
        "expected": "Reddit sentiment score and trending status"
    },
    
    {
        "id": 11,
        "query": "Is there hype on Twitter about NVDA? Check social media sentiment.",
        "targets": "SocialSentiment → twitter_tool, sentiment_tool",
        "expected": "Twitter sentiment with viral score and hype detection"
    },
    
    # Macro Economist queries (uses 3 tools: interest_rates, gdp, geopolitical)
    {
        "id": 12,
        "query": "What are current interest rates? How does the Fed policy look?",
        "targets": "MacroEconomist → interest_rates_tool",
        "expected": "Fed funds rate, treasury rates, rate trend"
    },
    
    {
        "id": 13,
        "query": "How is the US economy doing? Show me GDP and inflation data.",
        "targets": "MacroEconomist → gdp_tool",
        "expected": "GDP growth, inflation, unemployment rates"
    },
    
    {
        "id": 14,
        "query": "Are there any major geopolitical risks affecting the market?",
        "targets": "MacroEconomist → geopolitical_tool",
        "expected": "Geopolitical events and risk assessment"
    },
    
    # Multi-specialist intel query
    {
        "id": 15,
        "query": "Give me the full intelligence picture for AAPL: news, social sentiment, and macroeconomic environment.",
        "targets": "HeadOfIntel → ALL 3 intel specialists → ALL 8 intel tools",
        "expected": "Comprehensive narrative with BULLISH/BEARISH/NEUTRAL signal"
    },
]

# ============================================================================
# RISK DIVISION TESTS (ChiefRiskOfficer → 2 specialists → 5 tools)
# ============================================================================

RISK_QUERIES = [
    # Volatility Guard queries (uses 3 tools: var, volatility, blackswan)
    {
        "id": 16,
        "query": "What's the Value at Risk (VaR) if I invest $10,000 in TSLA?",
        "targets": "VolatilityGuard → var_tool",
        "expected": "VaR calculation with risk level assessment"
    },
    
    {
        "id": 17,
        "query": "How volatile is TSLA? Is it too risky right now?",
        "targets": "VolatilityGuard → volatility_tool",
        "expected": "Historical volatility with EXTREME/HIGH/MODERATE/LOW level"
    },
    
    {
        "id": 18,
        "query": "Are there any black swan risks or anomalies detected for AAPL?",
        "targets": "VolatilityGuard → blackswan_tool",
        "expected": "Black swan alert level (CRITICAL/WARNING/NORMAL)"
    },
    
    # Compliance Officer queries (uses 2 tools: compliance, correlation)
    {
        "id": 19,
        "query": "Is AAPL approved for trading? Any compliance issues?",
        "targets": "ComplianceOfficer → compliance_tool",
        "expected": "Compliance status (APPROVED/PROHIBITED)"
    },
    
    {
        "id": 20,
        "query": "If I hold AAPL, MSFT, and GOOGL, is my portfolio well diversified?",
        "targets": "ComplianceOfficer → correlation_tool",
        "expected": "Correlation analysis with diversification score"
    },
    
    # Multi-specialist risk query (tests VETO power)
    {
        "id": 21,
        "query": "Full risk assessment for TSLA: check volatility, compliance, and overall risk. Can I buy it?",
        "targets": "ChiefRiskOfficer → BOTH risk specialists → ALL 5 risk tools",
        "expected": "Risk report with APPROVE or VETO decision"
    },
]

# ============================================================================
# STRATEGY DIVISION TESTS (StrategyDirector → 3 specialists → 4 tools)
# ============================================================================

STRATEGY_QUERIES = [
    # Backtest Engineer queries (uses 1 tool: backtest)
    {
        "id": 22,
        "query": "Backtest a buy-and-hold strategy on AAPL for the past year.",
        "targets": "BacktestEngineer → backtest_tool",
        "expected": "Backtest results with Sharpe ratio, max drawdown, win rate"
    },
    
    {
        "id": 23,
        "query": "Backtest Results for AAPL - buy_and_hold Period: 1y Total Return: +33.2% Sharpe Ratio: 1.04 (GOOD) Max Drawdown: -5.1% Win Rate: 56.2% Number of Trades: 26vs Buy & Hold: N/A (Strategy is Buy & Hold)VALIDATION: GOOD CONFIDENCE: 90% REASONING: The buy-and-hold strategy for AAPL over the past year demonstrated a strong total return with a good Sharpe ratio, indicating solid risk-adjusted performance. The max drawdown was relatively contained.",
        "targets": "BacktestEngineer → backtest_tool",
        "expected": "Historical performance validation"
    },
    
    # Scenario Simulator queries (uses 2 tools: scenario, monte_carlo)
    {
        "id": 24,
        "query": "How would AAPL perform in a market crash scenario?",
        "targets": "ScenarioSimulator → scenario_tool",
        "expected": "Scenario analysis with impact estimation"
    },
    
    {
        "id": 25,
        "query": "Run a Monte Carlo simulation for TSLA. What's the expected price in 30 days?",
        "targets": "ScenarioSimulator → monte_carlo_tool",
        "expected": "Monte Carlo forecast with confidence intervals"
    },
    
    # Correlation Analyst queries (uses 1 tool: correlation)
    {
        "id": 26,
        "query": "Analyze correlation between AAPL, MSFT, GOOGL, and AMZN for portfolio optimization.",
        "targets": "CorrelationAnalyst → correlation_tool, portfolio_correlation_tool",
        "expected": "Correlation matrix with diversification recommendations"
    },
    
    # Multi-specialist strategy query
    {
        "id": 27,
        "query": "Validate the strategy of buying AAPL: backtest it, stress test scenarios, and check portfolio correlation.",
        "targets": "StrategyDirector → ALL 3 strategy specialists → ALL 4 strategy tools",
        "expected": "Validation score (0-100) with confidence level"
    },
]

# ============================================================================
# SHARED SPECIALISTS TESTS (FactChecker, SystemMonitor)
# ============================================================================

SHARED_QUERIES = [
    # Fact Checker queries (uses 2 tools: search, news)
    {
        "id": 28,
        "query": "Verify this claim: 'Apple announced a new iPhone with revolutionary battery technology'",
        "targets": "FactChecker → search_tool, news_tool",
        "expected": "VERIFIED/DISPUTED/UNVERIFIED with supporting evidence"
    },
    
    {
        "id": 29,
        "query": "Is it true that Tesla delivered 500,000 cars last quarter?",
        "targets": "FactChecker → search_tool",
        "expected": "Fact check with credibility assessment"
    },
    
    # System Monitor queries (uses 4 tools: memory_save, memory_retrieve, alert, log)
    {
        "id": 30,
        "query": "What's the system health status? Any performance issues?",
        "targets": "SystemMonitor → alert_tool, log_tool",
        "expected": "System status report (HEALTHY/WARNING/CRITICAL)"
    },
]

# ============================================================================
# COMPREHENSIVE INTEGRATION TESTS (All departments working together)
# ============================================================================

INTEGRATION_QUERIES = [
    # All 4 departments + fact checker
    {
        "id": 31,
        "query": "Should I invest $50,000 in AAPL? Give me a complete analysis from all departments.",
        "targets": "ROOT → ALL 4 L2 heads → ALL 13 L3 specialists → ALL 32 tools",
        "expected": "Comprehensive report with Quant (40%), Intel (30%), Risk (20%), Strategy (10%) synthesis"
    },
    
    {
        "id": 32,
        "query": "Full analysis of TSLA: technical indicators, news sentiment, risk assessment, and strategy validation.",
        "targets": "ROOT → ALL 4 departments → Comprehensive synthesis",
        "expected": "Multi-dimensional analysis with final BUY/SELL/HOLD recommendation"
    },
    
    # Test Risk VETO override
    {
        "id": 33,
        "query": "Analyze a highly volatile penny stock with extreme risk. Should I buy it?",
        "targets": "Tests Risk VETO: ChiefRiskOfficer should override positive signals",
        "expected": "VETO triggers, final recommendation is HOLD/AVOID despite other positives"
    },
    
    # Quick technical query (only Quant)
    {
        "id": 34,
        "query": "Quick technical check: what's the RSI for NVDA?",
        "targets": "Quick query → HeadOfQuant only → TechnicalAnalyst",
        "expected": "Fast response with just technical data"
    },
    
    # Memory and learning test
    {
        "id": 35,
        "query": "Remember that I prefer low-risk investments with high dividend yields in the technology sector.",
        "targets": "SystemMonitor → memory_save_tool, user_context_tool",
        "expected": "User preference saved to memory bank"
    },
]

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

def print_all_queries():
    """Print all queries for easy copy-paste testing"""
    print("\n" + "="*70)
    print("TITAN PLATFORM - 35 COMPREHENSIVE TEST QUERIES")
    print("="*70)
    
    all_queries = (
        QUANT_QUERIES + 
        INTEL_QUERIES + 
        RISK_QUERIES + 
        STRATEGY_QUERIES + 
        SHARED_QUERIES + 
        INTEGRATION_QUERIES
    )
    
    print(f"\nTotal Queries: {len(all_queries)}")
    print("\n" + "-"*70)
    
    for category_name, queries in [
        ("🔢 QUANT DIVISION", QUANT_QUERIES),
        ("📰 INTEL DIVISION", INTEL_QUERIES),
        ("⚠️  RISK DIVISION", RISK_QUERIES),
        ("📈 STRATEGY DIVISION", STRATEGY_QUERIES),
        ("🔍 SHARED SPECIALISTS", SHARED_QUERIES),
        ("🎯 INTEGRATION TESTS", INTEGRATION_QUERIES),
    ]:
        print(f"\n{category_name} ({len(queries)} queries)")
        print("-"*70)
        for q in queries:
            print(f"\n[Query #{q['id']}]")
            print(f"📝 {q['query']}")
            print(f"🎯 Targets: {q['targets']}")
            print(f"✅ Expected: {q['expected']}")
    
    print("\n" + "="*70)
    print("TESTING INSTRUCTIONS")
    print("="*70)
    print("""
1. Start the ADK web interface:
   cd agent_platform
   adk web

2. Copy queries one at a time into the chat interface

3. Verify each response includes:
   - Analysis from targeted specialists
   - Tool results in the output
   - Proper synthesis by department heads
   - Final recommendation from root agent

4. For comprehensive queries (#31-32), verify all 4 departments report

5. For risk query (#33), verify VETO power works correctly

6. Check logs in data/logs/ for detailed agent interactions
""")
    print("="*70 + "\n")


def save_queries_to_file(filename="test_queries.txt"):
    """Save all queries to a text file for reference"""
    all_queries = (
        QUANT_QUERIES + 
        INTEL_QUERIES + 
        RISK_QUERIES + 
        STRATEGY_QUERIES + 
        SHARED_QUERIES + 
        INTEGRATION_QUERIES
    )
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("TITAN PLATFORM - 35 TEST QUERIES\n")
        f.write("="*70 + "\n\n")
        
        for q in all_queries:
            f.write(f"[Query #{q['id']}]\n")
            f.write(f"{q['query']}\n")
            f.write(f"Targets: {q['targets']}\n")
            f.write(f"Expected: {q['expected']}\n")
            f.write("-"*70 + "\n\n")
    
    print(f"✅ Saved {len(all_queries)} queries to {filename}")


if __name__ == "__main__":
    print_all_queries()
    save_queries_to_file("test_queries.txt")

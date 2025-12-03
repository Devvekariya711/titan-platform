"""
Analyze response.docx to verify agent hierarchy functionality
"""
from docx import Document
import re
from collections import defaultdict

def analyze_responses():
    """Analyze the query-response document"""
    
    # Read the document
    doc = Document('response.docx')
    full_text = '\n'.join([p.text for p in doc.paragraphs])
    
    print("="*80)
    print("TITAN PLATFORM - QUERY RESPONSE ANALYSIS")
    print("="*80)
    
    # 1. Count queries
    queries = full_text.split('What')
    print(f"\n📊 Total Queries Found: {len(queries) - 1}")  # -1 because first split is before first "What"
    
    # 2. Count agent mentions
    print("\n🤖 L2 DEPARTMENT HEAD ACTIVATIONS:")
    l2_agents = {
        'HeadOfQuant': 0,
        'HeadOfIntel': 0,
        'ChiefRiskOfficer': 0,
        'StrategyDirector': 0
    }
    
    for agent in l2_agents:
        count = full_text.count(agent)
        l2_agents[agent] = count
        status = "✅" if count > 0 else "❌"
        print(f"  {status} {agent}: {count} mentions")
    
    # 3. Count L3 specialist mentions
    print("\n🔬 L3 SPECIALIST ACTIVATIONS:")
    l3_specialists = {
        'TechnicalAnalyst': 0,
        'FundamentalAnalyst': 0,
        'MicrostructureAnalyst': 0,
        'NewsScout': 0,
        'SocialSentiment': 0,
        'MacroEconomist': 0,
        'VolatilityGuard': 0,
        'ComplianceOfficer': 0,
        'BacktestEngineer': 0,
        'ScenarioSimulator': 0,
        'CorrelationAnalyst': 0,
        'FactChecker': 0,
        'SystemMonitor': 0
    }
    
    for specialist in l3_specialists:
        count = full_text.count(specialist)
        l3_specialists[specialist] = count
        status = "✅" if count > 0 else "⚠️"
        if count > 0:
            print(f"  {status} {specialist}: {count} times")
    
    # 4. Check for key signals
    print("\n📈 DECISION SIGNALS FOUND:")
    signals = {
        'BUY': full_text.count('BUY'),
        'SELL': full_text.count('SELL'),
        'HOLD': full_text.count('HOLD'),
        'BULLISH': full_text.count('BULLISH'),
        'BEARISH': full_text.count('BEARISH'),
        'NEUTRAL': full_text.count('NEUTRAL'),
        'APPROVE': full_text.count('APPROVE'),
        'VETO': full_text.count('VETO')
    }
    
    for signal, count in signals.items():
        if count > 0:
            print(f"  • {signal}: {count} times")
    
    # 5. Check for tool evidence
    print("\n🔧 TOOL EXECUTION EVIDENCE:")
    tool_patterns = [
        ('Market Data', ['OHLCV', 'Close', 'Volume', 'current_price']),
        ('Technical Indicators', ['RSI', 'MACD', 'Moving Average', 'MA', 'Bollinger']),
        ('Risk Metrics', ['VaR', 'Volatility', 'Value at Risk', 'Black Swan']),
        ('Fundamental Data', ['P/E', 'EPS', 'Market Cap', 'earnings']),
        ('News/Sentiment', ['headlines', 'sentiment', 'news', 'catalyst']),
        ('Strategy', ['Backtest', 'Monte Carlo', 'Sharpe', 'correlation']),
        ('Compliance', ['compliance', 'regulatory', 'approved'])
    ]
    
    for tool_category, keywords in tool_patterns:
        found = sum(1 for keyword in keywords if keyword.lower() in full_text.lower())
        status = "✅" if found > 0 else "⚠️"
        print(f"  {status} {tool_category}: {found}/{len(keywords)} keywords found")
    
    # 6. Department synthesis check
    print("\n📊 SYNTHESIS PATTERNS:")
    synthesis_phrases = [
        'Department Reports',
        'Specialist Reports',
        'Quant Division',
        'Intel Division',
        'Risk Division',
        'Strategy Division',
        'Final Recommendation',
        'Confidence',
        'Reasoning'
    ]
    
    for phrase in synthesis_phrases:
        count = full_text.count(phrase)
        if count > 0:
            print(f"  • '{phrase}': {count} times")
    
    # 7. Overall health check
    print("\n" + "="*80)
    print("HEALTH CHECK SUMMARY")
    print("="*80)
    
    total_l2_active = sum(1 for count in l2_agents.values() if count > 0)
    total_l3_active = sum(1 for count in l3_specialists.values() if count > 0)
    
    print(f"✅ L2 Heads Active: {total_l2_active}/4 ({total_l2_active/4*100:.0f}%)")
    print(f"✅ L3 Specialists Active: {total_l3_active}/13 ({total_l3_active/13*100:.0f}%)")
    
    # Check if comprehensive queries worked
    has_multi_dept = full_text.count('Department Reports') > 0 or full_text.count('Specialist Reports') > 2
    has_synthesis = full_text.count('Final Recommendation') > 0
    has_confidence = full_text.count('Confidence') > 0
    
    print(f"\n{'✅' if has_multi_dept else '❌'} Multi-department analysis: {'YES' if has_multi_dept else 'NO'}")
    print(f"{'✅' if has_synthesis else '❌'} Synthesis/recommendations: {'YES' if has_synthesis else 'NO'}")
    print(f"{'✅' if has_confidence else '❌'} Confidence scoring: {'YES' if has_confidence else 'NO'}")
    
    # Final verdict
    print("\n" + "="*80)
    overall_score = (
        (total_l2_active / 4 * 30) +  # 30 points for L2
        (total_l3_active / 13 * 40) +  # 40 points for L3
        (has_multi_dept * 10) +  # 10 points for multi-dept
        (has_synthesis * 10) +  # 10 points for synthesis
        (has_confidence * 10)  # 10 points for confidence
    )
    
    print(f"OVERALL SCORE: {overall_score:.0f}/100")
    
    if overall_score >= 80:
        print("✅ EXCELLENT: Agent hierarchy is working well!")
    elif overall_score >= 60:
        print("⚠️  GOOD: Most agents active, but some coverage gaps")
    elif overall_score >= 40:
        print("⚠️  FAIR: Basic functionality working, needs improvement")
    else:
        print("❌ POOR: Significant issues with agent activation")
    
    print("="*80)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if total_l2_active < 4:
        missing = [agent for agent, count in l2_agents.items() if count == 0]
        print(f"  • Test queries for missing L2 heads: {', '.join(missing)}")
    
    if total_l3_active < 10:
        missing = [agent for agent, count in l3_specialists.items() if count == 0]
        print(f"  • Test queries for missing L3 specialists: {', '.join(missing[:5])}")
    
    if not has_multi_dept:
        print("  • Try comprehensive queries that trigger all 4 departments")
    
    if full_text.count('VETO') == 0:
        print("  • Test Risk VETO functionality with high-risk queries")
    
    print("\n")

if __name__ == "__main__":
    try:
        analyze_responses()
    except FileNotFoundError:
        print("Error: response.docx not found in current directory")
    except Exception as e:
        print(f"Error analyzing document: {str(e)}")
        import traceback
        traceback.print_exc()

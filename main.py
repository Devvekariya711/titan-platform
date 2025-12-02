"""
Titan Platform - Agent Entry Point
Main application for the enterprise multi-agent investment analysis system
"""
from google.adk.sessions import Session
import os
from dotenv import load_dotenv
import sys

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Import root agent
from agent_platform.agents.root.market_trend_principal import market_trend_principal

def main():
    """Main entry point for Titan Platform"""
    
    print("=" * 70)
    print("🏛️  TITAN PLATFORM - Enterprise Investment Analysis System")
    print("=" * 70)
    print("\nVersion: v0.4-month3")
    print("Agents: 17 (1 L1 + 4 L2 + 12 L3 + FactChecker)")
    print("Tools: 28 operational")
    print("\nHierarchy: CEO → Quant(40%) + Intel(30%) + Risk(20%+VETO) + Strategy(10%)")
    print("\nAvailable Analysis:")
    print("  ✅ Technical Analysis: RSI, MACD, Bollinger Bands, S/R")
    print("  ✅ Fundamental Analysis: Earnings, P/E ratios")
    print("  ✅ News/Sentiment Intelligence: Multi-source analysis")
    print("  ✅ Risk Management: VaR, volatility, compliance + VETO")
    print("  ✅ Strategy Validation: Real 5yr historical backtests")
    print("  ✅ User Personalization: Risk profiles, preferences")
    print("\n" + "=" * 70)
    print("\nExample queries:")
    print('  "What is the RSI of Apple?"')
    print('  "Should I buy Tesla?"')
    print('  "Analyze NVDA fundamentals"')
    print('  "Backtest buy-and-hold on AAPL for 5 years"')
    print("\nType 'quit' or 'exit' to stop\n")
    
    # Create session with required parameters
    session = Session(
        id="titan-session-001",
        appName="Titan Platform",
        userId="default-user"
    )
    
    # Interactive loop
    while True:
        try:
            user_input = input("💬 Your query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Titan Platform!")
                break
            
            print("\n🔄 Processing through 17-agent hierarchy...")
            print("-" * 70)
            
            # Use query() method with message format (ADK standard)
            response = market_trend_principal.query(
                message=user_input,
                session=session
            )
            
            print("\n📊 TITAN INVESTMENT COMMITTEE ANALYSIS:\n")
            print(response)
            print("\n" + "=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"\nFull traceback:")
            traceback.print_exc()
            print("\nPlease try again or type 'quit' to exit.\n")

if __name__ == "__main__":
    main()

"""
Titan Platform - Agent Entry Point
Main application for the enterprise multi-agent investment analysis system
"""
from google.adk.sessions import Session
from google.adk.runners import Runner
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
    
    # Create Runner (proper ADK pattern for programmatic execution)
    runner = Runner(agent=market_trend_principal, app_name="titan_platform")
    
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
            
            # Use Runner.run() with message (ADK standard pattern)
            result = runner.run(message=user_input)
            
            # Extract text response
            if hasattr(result, 'text'):
                response = result.text
            elif isinstance(result, str):
                response = result
            else:
                response = str(result)
            
            print("\n📊 TITAN INVESTMENT COMMITTEE ANALYSIS:\n")
            print(response)
            print("\n" + "=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            
            # Check for API quota errors
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print("\n⚠️  API QUOTA EXCEEDED")
                print("Your Google AI API has hit rate limits.")
                print("Please wait a few minutes and try again, or:")
                print("  - Check your API usage: https://ai.dev/usage")
                print("  - Get a new API key: https://aistudio.google.com/apikey")
            elif "INVALID_ARGUMENT" in str(e) or "API Key not found" in str(e):
                print("\n⚠️  API KEY ERROR")
                print("Check your .env file has valid GOOGLE_API_KEY")
            
            import traceback
            print(f"\nFull traceback:")
            traceback.print_exc()
            print("\nPlease try again or type 'quit' to exit.\n")

if __name__ == "__main__":
    main()

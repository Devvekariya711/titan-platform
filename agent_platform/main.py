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
from agents.root.market_trend_principal import market_trend_principal

def main():
    """Main entry point for Titan Platform"""
    
    print("=" * 70)
    print("🏛️  TITAN PLATFORM - Enterprise Investment Analysis System")
    print("=" * 70)
    print("\nPhase: Month 1 - Foundation")
    print("Hierarchy: L1 (CEO) → L2 (HeadOfQuant) → L3 (TechnicalAnalyst)")
    print("\nAvailable Analysis:")
    print("  ✅ Technical Analysis: RSI, MACD, Bollinger Bands, Support/Resistance")
    print("  🔄 Fundamental Analysis: Coming in Month 2")
    print("  🔄 News/Sentiment Intelligence: Coming in Month 2")
    print("  🔄 Risk Management: Coming in Month 2")
    print("  🔄 Strategy Validation: Coming in Month 3")
    print("\n" + "=" * 70)
    print("\nType 'quit' or 'exit' to stop\n")
    
    # Create session
    session = Session()
    
    # Interactive loop
    while True:
        try:
            user_input = input("💬 Your query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Titan Platform!")
                break
            
            print("\n🔄 Analyzing...")
            print("-" * 70)
            
            # Run agent
            response = market_trend_principal.run(user_input, session=session)
            
            print("\n📊 TITAN ANALYSIS:\n")
            print(response)
            print("\n" + "=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")

if __name__ == "__main__":
    main()

"""
Titan Market Analyst - Main Entry Point
Simple CLI for testing the Quant Agent
"""

from market_analyst.agent import root_agent


def main():
    """Interactive CLI for Titan Investment Committee"""
    print("="  * 80)
    print("🏛️  TITAN INVESTMENT COMMITTEE")
    print("=" * 80)
    print("\nWelcome to Titan - Your AI-Powered Investment Analysis System")
    print("\nCommittee Members:")
    print("  📊 Quant Analyst - Technical analysis and price action")
    print("  📰 Data Scout - Market data and financial news")
    print("  ⚠️  Risk Assessor - Risk evaluation and sentiment")
    print("\n" + "=" * 80)
    print("\nExamples:")
    print("  - How does NVDA look technically?")
    print("  - Analyze AAPL technical indicators")
    print("  - What's the RSI for TSLA?")
    print("  - Give me a technical analysis of Microsoft")
    print("\nType 'exit' to quit\n")
    print("=" * 80)
    
    while True:
        try:
            query = input("\n💬 Your query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using Titan. Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🤔 Analyzing...")
            print("-" * 80)
            
            # Run the agent
            response = root_agent.execute(query)
            
            print(f"\n{response}")
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    main()
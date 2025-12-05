"""
Titan Platform - Agent Entry Point
Main application for the enterprise multi-agent investment analysis system
"""
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import os
import time
import uuid
import json
from dotenv import load_dotenv
import sys

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Import root agent
from agent_platform.root_agent import market_trend_principal
from shared.utils.logger import get_logger

# Initialize logger for main application
logger = get_logger("titan-main")

# User state file for persistence
USER_STATE_FILE = os.path.join(os.path.dirname(__file__), ".titan_user.json")

def load_user_state():
    """Load persistent user state from file"""
    if os.path.exists(USER_STATE_FILE):
        try:
            with open(USER_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"user_id": "default_user", "name": None, "preferences": {}}

def save_user_state(state):
    """Save user state to file for persistence"""
    try:
        with open(USER_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.warning(f"Could not save user state: {e}")

def main():
    """Main entry point for Titan Platform"""
    
    # Load persistent user state
    user_state = load_user_state()
    user_id = user_state.get("user_id", "default_user")
    
    # Use persistent session ID (only generate once per user)
    if "session_id" not in user_state:
        user_state["session_id"] = str(uuid.uuid4())[:8]
        save_user_state(user_state)
    
    session_id = user_state["session_id"]
    logger.info("Titan Platform started", session_id=session_id, user_id=user_id)
    
    print("=" * 70)
    print("🏛️  TITAN PLATFORM - Enterprise Investment Analysis System")
    print("=" * 70)
    print("\nVersion: v1.0.1")
    print("Agents: 17 (1 L1 + 4 L2 + 12 L3 + FactChecker)")
    print("Tools: 28 operational")
    if user_state.get("name"):
        print(f"\n👤 Welcome back, {user_state['name']}!")
    print("\nHierarchy: CEO → Quant(40%) + Intel(30%) + Risk(20%+VETO) + Strategy(10%)")
    print("\n⚠️  Note: Stock data is simulated. For real-time data, integrate live APIs.")
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
    print('  "My name is [Your Name]" - I will remember you!')
    print('  "Analyze NVDA fundamentals"')
    print("\nType 'quit' or 'exit' to stop\n")
    
    # Create session service (required for ADK 1.19.0+)
    session_service = InMemorySessionService()
    
    # Create Runner (proper ADK pattern for programmatic execution)
    runner = Runner(
        agent=market_trend_principal, 
        app_name="agent_platform",
        session_service=session_service
    )
    
    # Interactive loop
    query_count = 0
    while True:
        try:
            user_input = input("💬 Your query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                save_user_state(user_state)  # Save state on exit
                logger.info("User session ended", 
                           session_id=session_id,
                           total_queries=query_count)
                print("\n👋 Thank you for using Titan Platform!")
                break
            
            # Check for name introduction (simple pattern matching)
            name_patterns = ["my name is", "i am", "i'm", "call me"]
            for pattern in name_patterns:
                if pattern in user_input.lower():
                    # Extract name after the pattern
                    idx = user_input.lower().find(pattern)
                    potential_name = user_input[idx + len(pattern):].strip().split()[0] if user_input[idx + len(pattern):].strip() else None
                    if potential_name and len(potential_name) > 1:
                        # Clean up name (remove punctuation)
                        clean_name = ''.join(c for c in potential_name if c.isalpha())
                        if clean_name:
                            user_state["name"] = clean_name.capitalize()
                            save_user_state(user_state)
                            print(f"\n✅ Nice to meet you, {user_state['name']}! I'll remember you.\n")
                    break
            
            # Generate query ID and log the query
            query_count += 1
            query_id = f"{session_id}-{query_count}"
            logger.log_query(user_input, user_id=user_id, session_id=session_id)
            
            print("\n🔄 Processing through 17-agent hierarchy...")
            print("-" * 70)
            
            # Track response time
            start_time = time.time()
            
            # Create message content for ADK 1.19.0+
            message_content = types.Content(
                parts=[types.Part(text=user_input)],
                role="user"
            )
            
            # Use Runner.run() with proper ADK 1.19.0 parameters
            events = runner.run(
                user_id=user_id,  # Use persistent user_id
                session_id=session_id,
                new_message=message_content
            )
            
            # Extract text response from events (generator)
            response = ""
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response += part.text
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log the response
            logger.log_response(response, agent="market_trend_principal", 
                               query_id=query_id, duration_ms=duration_ms)
            
            print("\n📊 TITAN INVESTMENT COMMITTEE ANALYSIS:\n")
            print(response if response else "(No response received)")
            print(f"\n⏱️  Response time: {duration_ms:.0f}ms")
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

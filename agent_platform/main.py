"""
Titan Platform - Agent Entry Point
Main application for the enterprise multi-agent investment analysis system
"""
from google.adk.sessions import Session
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.genai import types
import os
from dotenv import load_dotenv
import sys
import asyncio

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Import root agent
from agents.root.market_trend_principal import market_trend_principal

# Create services
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()
credential_service = InMemoryCredentialService()

# Create App and Runner
app = App(name="Titan_Platform", root_agent=market_trend_principal)
runner = Runner(
    app=app,
    artifact_service=artifact_service,
    session_service=session_service,
    credential_service=credential_service
)

async def run_query(session: Session, query: str):
    """Run a query asynchronously and return the response"""
    try:
        content = types.Content(role='user', parts=[types.Part(text=query)])
        response_text = ""
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
        
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"

async def main_async():
    """Async main entry point for Titan Platform"""
    
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
    session = await session_service.create_session(
        app_name="Titan_Platform",
        user_id="user-001"
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
            
            print("\n🔄 Analyzing...")
            print("-" * 70)
            
            # Run query
            response = await run_query(session, user_input)
            
            print("\n📊 TITAN ANALYSIS:\n")
            print(response)
            print("\n" + "=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")
    
    await runner.close()

def main():
    """Main entry point for Titan Platform"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

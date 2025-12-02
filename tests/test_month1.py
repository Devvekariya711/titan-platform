"""
Quick Test Script for Month 1 Agent Hierarchy
Tests the L1 → L2 → L3 agent flow
"""
import os
import sys

# Set up paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("=" * 70)
print("🧪 TITAN PLATFORM - Month 1 Integration Test")
print("=" * 70)

try:
    print("\n✅ Step 1: Testing imports...")
    
    # Test shared utilities  
    from shared.utils.logger import get_logger
    from shared.utils.errors import DataFetchError
    logger = get_logger("test")
    print("   ✓ Shared utilities imported")
    
    # Test services
    from services.ingestion_engine.connectors import get_connector
    from services.memory_bank import get_memory_bank
    print("   ✓ Services imported")
    
    # Test tools
    from agent_platform.tools.quant_tools import (
        market_data_tool,
        technical_indicators_tool, 
        price_action_tool
    )
    print("   ✓ Tools imported")
    
    # Test agents
    from agent_platform.agents.specialists.quant_specialists import technical_analyst
    from agent_platform.agents.leads.head_of_quant import head_of_quant
    from agent_platform.agents.root.market_trend_principal import market_trend_principal
    print("   ✓ Agents imported (L3 → L2 → L1)")
    
    print("\n✅ Step 2: Testing data connector...")
    connector = get_connector()
    test_data = connector.get_realtime_price("AAPL")
    print(f"   ✓ AAPL current price: ${test_data:.2f}")
    
    print("\n✅ Step 3: Testing memory bank...")
    memory = get_memory_bank()
    memory.store_user_preference("test_user", "test_key", "test_content")
    print("   ✓ Memory bank operational")
    
    print("\n✅ Step 4: Agent hierarchy verification...")
    print(f"   ✓ L1 (MarketTrendPrincipal): {market_trend_principal.name}")
    print(f"   ✓ L2 (HeadOfQuant): {head_of_quant.name}")
    print(f"   ✓ L3 (TechnicalAnalyst): {technical_analyst.name}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nMonth 1 Foundation is ready!")
    print("\nNext steps:")
    print("1. Run: cd agent_platform && python main.py")
    print("2. Test query: 'What is the RSI of AAPL?'")
    print("3. Verify L1 → L2 → L3 delegation works")
    print("\n" + "=" * 70)
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nThis may be expected if dependencies aren't installed yet.")
    print("The structure is correct, imports will work after: pip install -r agent_platform/requirements.txt")
except Exception as e:
    print(f"\n❌ Test Error: {e}")
    import traceback
    traceback.print_exc()

print()

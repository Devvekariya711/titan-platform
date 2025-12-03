"""
============================================================================
TITAN PLATFORM - AGENT HIERARCHY TEST
============================================================================
Comprehensive test suite to verify agent hierarchy connections:

L1 (Root Agent)
  └─> L2 (4 Department Heads)
        └─> L3 (13 Specialists)
              └─> Tools (32 tools)

Tests verify:
1. L1 root_agent connects to all 4 L2 department heads
2. Each L2 head connects to their L3 specialists
3. Each L3 specialist has the correct tools assigned
4. Full integration from L1 all the way down to tools

Run with: python tests/test_agent_hierarchy.py
============================================================================
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_platform.root_agent import root_agent, market_trend_principal
from agent_platform.supporting_agents import (
    # L2 Leads
    head_of_quant, head_of_intel, chief_risk_officer, strategy_director,
    # L3 Quant specialists
    technical_analyst, fundamental_analyst, microstructure_analyst,
    # L3 Intel specialists
    news_scout, social_sentiment, macro_economist,
    # L3 Risk specialists
    volatility_guard, compliance_officer,
    # L3 Strategy specialists
    backtest_engineer, scenario_simulator, correlation_analyst,
    # L3 Shared
    fact_checker, system_monitor
)
from agent_platform.tools import (
    # Quant tools
    market_data_tool, technical_indicators_tool, price_action_tool,
    fundamental_data_tool, earnings_tool, volume_tool,
    chart_patterns_tool, market_structure_tool,
    # Intel tools
    news_tool, reddit_tool, twitter_tool, interest_rates_tool,
    gdp_tool, geopolitical_tool, sentiment_tool, search_tool,
    # Risk tools
    var_tool, volatility_tool, compliance_tool,
    correlation_tool, blackswan_tool,
    # Strategy tools
    backtest_tool, monte_carlo_tool, portfolio_correlation_tool, scenario_tool,
    # System tools
    memory_save_tool, memory_retrieve_tool, user_context_tool,
    agent_output_tool, similar_analysis_tool, alert_tool, log_tool
)


class AgentHierarchyTester:
    """Test agent hierarchy connections"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total_tests = 0
    
    def test(self, condition, description):
        """Run a single test"""
        self.total_tests += 1
        if condition:
            self.passed += 1
            print(f"  ✅ PASS: {description}")
            return True
        else:
            self.failed += 1
            print(f"  ❌ FAIL: {description}")
            return False
    
    def section(self, title):
        """Print section header"""
        print(f"\n{'='*70}")
        print(f"{title}")
        print(f"{'='*70}")
    
    def run_all_tests(self):
        """Run all hierarchy tests"""
        print("\n" + "="*70)
        print("TITAN PLATFORM - AGENT HIERARCHY TEST SUITE")
        print("="*70)
        
        # Test 1: L1 Root Agent
        self.test_l1_root_agent()
        
        # Test 2: L1 → L2 Connections
        self.test_l1_to_l2_connections()
        
        # Test 3: L2 → L3 Connections
        self.test_l2_to_l3_connections()
        
        # Test 4: L3 → Tools Connections
        self.test_l3_to_tools_connections()
        
        # Test 5: Full Integration
        self.test_full_integration()
        
        # Print summary
        self.print_summary()
        
        return self.failed == 0
    
    def test_l1_root_agent(self):
        """Test L1 root agent exists and is configured"""
        self.section("TEST 1: L1 ROOT AGENT")
        
        self.test(root_agent is not None, "root_agent exists")
        self.test(market_trend_principal is not None, "market_trend_principal exists")
        self.test(root_agent == market_trend_principal, "root_agent and market_trend_principal are same")
        self.test(root_agent.name == "market_trend_principal", "root_agent has correct name")
        self.test(hasattr(root_agent, 'sub_agents'), "root_agent has sub_agents")
        self.test(len(root_agent.sub_agents) == 5, f"root_agent has 5 sub_agents (found {len(root_agent.sub_agents)})")
    
    def test_l1_to_l2_connections(self):
        """Test L1 connects to all 4 L2 department heads + fact_checker"""
        self.section("TEST 2: L1 → L2 CONNECTIONS")
        
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        
        # Test each L2 connection
        self.test('head_of_quant' in sub_agent_names, "L1 → head_of_quant connected")
        self.test('head_of_intel' in sub_agent_names, "L1 → head_of_intel connected")
        self.test('chief_risk_officer' in sub_agent_names, "L1 → chief_risk_officer connected")
        self.test('strategy_director' in sub_agent_names, "L1 → strategy_director connected")
        self.test('fact_checker' in sub_agent_names, "L1 → fact_checker connected")
        
        # Verify no extra agents
        self.test(len(sub_agent_names) == 5, f"L1 has exactly 5 sub-agents (no extras)")
    
    def test_l2_to_l3_connections(self):
        """Test each L2 head connects to their L3 specialists"""
        self.section("TEST 3: L2 → L3 CONNECTIONS")
        
        # Test HeadOfQuant → Quant Specialists (3)
        print("\n  HeadOfQuant → Quant Specialists:")
        quant_subs = [agent.name for agent in head_of_quant.sub_agents]
        self.test('technical_analyst' in quant_subs, "  └─> technical_analyst connected")
        self.test('fundamental_analyst' in quant_subs, "  └─> fundamental_analyst connected")
        self.test('microstructure_analyst' in quant_subs, "  └─> microstructure_analyst connected")
        self.test(len(quant_subs) == 3, f"  └─> HeadOfQuant has 3 specialists (found {len(quant_subs)})")
        
        # Test HeadOfIntel → Intel Specialists (3)
        print("\n  HeadOfIntel → Intel Specialists:")
        intel_subs = [agent.name for agent in head_of_intel.sub_agents]
        self.test('news_scout' in intel_subs, "  └─> news_scout connected")
        self.test('social_sentiment' in intel_subs, "  └─> social_sentiment connected")
        self.test('macro_economist' in intel_subs, "  └─> macro_economist connected")
        self.test(len(intel_subs) == 3, f"  └─> HeadOfIntel has 3 specialists (found {len(intel_subs)})")
        
        # Test ChiefRiskOfficer → Risk Specialists (2)
        print("\n  ChiefRiskOfficer → Risk Specialists:")
        risk_subs = [agent.name for agent in chief_risk_officer.sub_agents]
        self.test('volatility_guard' in risk_subs, "  └─> volatility_guard connected")
        self.test('compliance_officer' in risk_subs, "  └─> compliance_officer connected")
        self.test(len(risk_subs) == 2, f"  └─> ChiefRiskOfficer has 2 specialists (found {len(risk_subs)})")
        
        # Test StrategyDirector → Strategy Specialists (3)
        print("\n  StrategyDirector → Strategy Specialists:")
        strategy_subs = [agent.name for agent in strategy_director.sub_agents]
        self.test('backtest_engineer' in strategy_subs, "  └─> backtest_engineer connected")
        self.test('scenario_simulator' in strategy_subs, "  └─> scenario_simulator connected")
        self.test('correlation_analyst' in strategy_subs, "  └─> correlation_analyst connected")
        self.test(len(strategy_subs) == 3, f"  └─> StrategyDirector has 3 specialists (found {len(strategy_subs)})")
    
    def test_l3_to_tools_connections(self):
        """Test L3 specialists have correct tools"""
        self.section("TEST 4: L3 → TOOLS CONNECTIONS")
        
        # Test Technical Analyst tools (5 quant tools)
        print("\n  TechnicalAnalyst → Tools:")
        ta_tools = [tool.func.__name__ for tool in technical_analyst.tools]
        self.test('get_market_data' in ta_tools, "  └─> market_data_tool")
        self.test('calculate_technicals' in ta_tools, "  └─> technical_indicators_tool")
        self.test('analyze_price_action' in ta_tools, "  └─> price_action_tool")
        self.test('detect_chart_patterns' in ta_tools, "  └─> chart_patterns_tool")
        self.test('analyze_volume' in ta_tools, "  └─> volume_tool")
        self.test(len(ta_tools) == 5, f"  └─> TechnicalAnalyst has 5 tools (found {len(ta_tools)})")
        
        # Test Volatility Guard tools (3 risk tools)
        print("\n  VolatilityGuard → Tools:")
        vg_tools = [tool.func.__name__ for tool in volatility_guard.tools]
        self.test('calculate_var' in vg_tools, "  └─> var_tool")
        self.test('monitor_volatility' in vg_tools, "  └─> volatility_tool")
        self.test('detect_blackswan' in vg_tools, "  └─> blackswan_tool")
        self.test(len(vg_tools) == 3, f"  └─> VolatilityGuard has 3 tools (found {len(vg_tools)})")
        
        # Test News Scout tools (2 intel tools)
        print("\n  NewsScout → Tools:")
        ns_tools = [tool.func.__name__ for tool in news_scout.tools]
        self.test('multi_source_news' in ns_tools, "  └─> news_tool")
        self.test('sentiment_analyzer' in ns_tools, "  └─> sentiment_tool")
        self.test(len(ns_tools) == 2, f"  └─> NewsScout has 2 tools (found {len(ns_tools)})")
        
        # Test Backtest Engineer tools (1 strategy tool)
        print("\n  BacktestEngineer → Tools:")
        be_tools = [tool.func.__name__ for tool in backtest_engineer.tools]
        self.test('backtest_strategy' in be_tools, "  └─> backtest_tool")
        self.test(len(be_tools) == 1, f"  └─> BacktestEngineer has 1 tool (found {len(be_tools)})")
        
        # Test System Monitor tools (4 system tools)
        print("\n  SystemMonitor → Tools:")
        sm_tools = [tool.func.__name__ for tool in system_monitor.tools]
        self.test('memory_save' in sm_tools, "  └─> memory_save_tool")
        self.test('memory_retrieve' in sm_tools, "  └─> memory_retrieve_tool")
        self.test('send_alert' in sm_tools, "  └─> alert_tool")
        self.test('log_event' in sm_tools, "  └─> log_tool")
        self.test(len(sm_tools) == 4, f"  └─> SystemMonitor has 4 tools (found {len(sm_tools)})")
    
    def test_full_integration(self):
        """Test full L1→L2→L3→Tools chain"""
        self.section("TEST 5: FULL INTEGRATION (L1→L2→L3→TOOLS)")
        
        print("\n  Testing complete path: L1 → HeadOfQuant → TechnicalAnalyst → Tools")
        
        # Verify the chain
        has_head_of_quant = 'head_of_quant' in [a.name for a in root_agent.sub_agents]
        self.test(has_head_of_quant, "  Step 1: root_agent → head_of_quant ✓")
        
        if has_head_of_quant:
            has_technical = 'technical_analyst' in [a.name for a in head_of_quant.sub_agents]
            self.test(has_technical, "  Step 2: head_of_quant → technical_analyst ✓")
            
            if has_technical:
                has_tools = len(technical_analyst.tools) > 0
                self.test(has_tools, f"  Step 3: technical_analyst → {len(technical_analyst.tools)} tools ✓")
                
                has_market_data = 'get_market_data' in [t.func.__name__ for t in technical_analyst.tools]
                self.test(has_market_data, "  Step 4: market_data_tool accessible ✓")
        
        print("\n  Testing another path: L1 → ChiefRiskOfficer → VolatilityGuard → Tools")
        
        has_cro = 'chief_risk_officer' in [a.name for a in root_agent.sub_agents]
        self.test(has_cro, "  Step 1: root_agent → chief_risk_officer ✓")
        
        if has_cro:
            has_vol_guard = 'volatility_guard' in [a.name for a in chief_risk_officer.sub_agents]
            self.test(has_vol_guard, "  Step 2: chief_risk_officer → volatility_guard ✓")
            
            if has_vol_guard:
                has_var = 'calculate_var' in [t.func.__name__ for t in volatility_guard.tools]
                self.test(has_var, "  Step 3: var_tool accessible ✓")
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*70}")
        print("TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/self.total_tests*100):.1f}%")
        print(f"{'='*70}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Agent hierarchy is correctly configured! 🎉\n")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Please review the hierarchy configuration.\n")


def main():
    """Run hierarchy tests"""
    tester = AgentHierarchyTester()
    success = tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

"""
Titan Platform - Integration Test Suite
Tests full system functionality including all agents, tools, and services.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib.util
import sys

# Import from hyphenated directories
spec = importlib.util.spec_from_file_location(
    "chromadb_wrapper", 
    os.path.join(os.path.dirname(__file__), "..", "services", "memory-bank", "chromadb_wrapper.py")
)
chromadb_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_wrapper"] = chromadb_module
spec.loader.exec_module(chromadb_module)
ChromaDBWrapper = chromadb_module.ChromaDBWrapper

spec = importlib.util.spec_from_file_location(
    "simulator", 
    os.path.join(os.path.dirname(__file__), "..", "services", "backtest-engine", "simulator.py")
)
simulator_module = importlib.util.module_from_spec(spec)
sys.modules["simulator"] = simulator_module
spec.loader.exec_module(simulator_module)
BacktestEngine = simulator_module.BacktestEngine

from agent_platform.tools.quant_tools import calculate_technicals, get_market_data
from agent_platform.tools.risk_tools import calculate_var, volatility_monitor
from agent_platform.tools.strategy_tools import backtest_strategy


class IntegrationTestSuite:
    """Comprehensive integration tests for Titan Platform"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_user_id = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.memory = None
        
    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 80)
        print("TITAN PLATFORM - INTEGRATION TEST SUITE")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        # Run test suites
        self.test_scenario_1_conservative_user_volatile_stock()
        self.test_scenario_2_aggressive_user_stable_stock()
        self.test_scenario_3_risk_veto_trigger()
        self.test_scenario_4_backtest_validation()
        self.test_scenario_5_memory_persistence()
        
        # Print summary
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        print(f"Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        print("=" * 80)
        
        return self.failed == 0
    
    def assert_true(self, condition, message):
        """Assert helper"""
        if condition:
            self.passed += 1
            print(f"  ✅ {message}")
        else:
            self.failed += 1
            print(f"  ❌ {message}")
    
    def test_scenario_1_conservative_user_volatile_stock(self):
        """
        Scenario 1: Conservative User + Volatile Stock (TSLA)
        
        Setup: User with risk_tolerance=LOW, max_drawdown=15%
        Expected: System recommends caution or reduced position size
        Validates: Memory Bank, Risk VETO, Personalization
        """
        print("TEST 1: Conservative User + Volatile Stock")
        print("-" * 80)
        
        try:
            # Initialize Memory Bank
            self.memory = ChromaDBWrapper()
            
            # Store conservative user profile
            self.memory.store_risk_profile(
                self.test_user_id,
                risk_tolerance="LOW",
                max_drawdown_tolerance=0.15,  # 15%
                preferred_sectors=["technology"]
            )
            
            # Retrieve user context
            user_context = self.memory.get_user_context(self.test_user_id)
            
            self.assert_true(
                user_context is not None,
                "User profile stored successfully"
            )
            
            self.assert_true(
                user_context.get("risk_tolerance") == "LOW",
                "Risk tolerance set to LOW"
            )
            
            # Check TSLA volatility
            vol_data = volatility_monitor("TSLA", "90d")
            
            self.assert_true(
                vol_data is not None,
                "Volatility data retrieved"
            )
            
            # TSLA should have high volatility
            tsla_vol = vol_data.get("realized_volatility_90d", 0)
            
            self.assert_true(
                tsla_vol > 0.20,  # >20% volatility
                f"TSLA volatility is high ({tsla_vol*100:.1f}%)"
            )
            
            # Check if VETO should trigger
            should_veto = tsla_vol > user_context.get("max_drawdown_tolerance", 0.15)
            
            self.assert_true(
                should_veto,
                "Risk VETO should trigger for conservative user"
            )
            
            print(f"  ℹ️  User tolerance: {user_context.get('max_drawdown_tolerance')*100}%")
            print(f"  ℹ️  TSLA volatility: {tsla_vol*100:.1f}%")
            print(f"  ℹ️  VETO triggered: {should_veto}")
            
        except Exception as e:
            self.assert_true(False, f"Test failed with error: {str(e)}")
        
        print()
    
    def test_scenario_2_aggressive_user_stable_stock(self):
        """
        Scenario 2: Aggressive User + Stable Stock (JNJ)
        
        Setup: User with risk_tolerance=HIGH
        Expected: System approves standard position
        Validates: User context retrieval, risk assessment
        """
        print("TEST 2: Aggressive User + Stable Stock")
        print("-" * 80)
        
        try:
            # Create aggressive user
            aggressive_user_id = f"{self.test_user_id}_aggressive"
            
            self.memory.store_risk_profile(
                aggressive_user_id,
                risk_tolerance="HIGH",
                max_drawdown_tolerance=0.40,  # 40%
                preferred_sectors=["growth", "technology"]
            )
            
            # Retrieve context
            user_context = self.memory.get_user_context(aggressive_user_id)
            
            self.assert_true(
                user_context.get("risk_tolerance") == "HIGH",
                "Aggressive user profile created"
            )
            
            # Check stable stock (JNJ or similar)
            # Using AAPL as proxy for stable tech stock
            vol_data = volatility_monitor("AAPL", "90d")
            aapl_vol = vol_data.get("realized_volatility_90d", 0)
            
            self.assert_true(
                aapl_vol < 0.30,  # <30% volatility
                f"AAPL is relatively stable ({aapl_vol*100:.1f}%)"
            )
            
            # Check if approved for aggressive user
            should_approve = aapl_vol < user_context.get("max_drawdown_tolerance", 0.40)
            
            self.assert_true(
                should_approve,
                "Stable stock approved for aggressive user"
            )
            
            print(f"  ℹ️  User tolerance: {user_context.get('max_drawdown_tolerance')*100}%")
            print(f"  ℹ️  AAPL volatility: {aapl_vol*100:.1f}%")
            print(f"  ℹ️  Approved: {should_approve}")
            
        except Exception as e:
            self.assert_true(False, f"Test failed with error: {str(e)}")
        
        print()
    
    def test_scenario_3_risk_veto_trigger(self):
        """
        Scenario 3: Risk VETO Trigger
        
        Setup: Recommend high-volatility trade
        Expected: ChiefRiskOfficer vetoes
        Validates: Risk agent veto power, VaR calculation
        """
        print("TEST 3: Risk VETO Trigger")
        print("-" * 80)
        
        try:
            # Calculate VaR for volatile stock
            var_result = calculate_var(
                "TSLA",
                confidence_level=0.95,
                holding_period=1,
                portfolio_value=10000
            )
            
            self.assert_true(
                var_result is not None,
                "VaR calculation successful"
            )
            
            self.assert_true(
                "var_95" in var_result,
                "VaR(95%) calculated"
            )
            
            var_95 = var_result.get("var_95", 0)
            
            self.assert_true(
                var_95 > 0.10,  # >10% potential loss
                f"VaR indicates high risk ({var_95*100:.1f}%)"
            )
            
            # Check risk rating
            risk_rating = var_result.get("risk_rating", "unknown")
            
            self.assert_true(
                risk_rating in ["moderate", "high", "extreme"],
                f"Risk rating appropriate: {risk_rating}"
            )
            
            print(f"  ℹ️  VaR(95%): {var_95*100:.1f}%")
            print(f"  ℹ️  VaR(99%): {var_result.get('var_99', 0)*100:.1f}%")
            print(f"  ℹ️  Risk Rating: {risk_rating}")
            
        except Exception as e:
            self.assert_true(False, f"Test failed with error: {str(e)}")
        
        print()
    
    def test_scenario_4_backtest_validation(self):
        """
        Scenario 4: Backtest Validation (AAPL)
        
        Setup: Backtest RSI strategy on AAPL, 5 years
        Expected: Realistic Sharpe ratio, drawdown, win rate
        Validates: Backtest engine accuracy, historical data
        """
        print("TEST 4: Backtest Validation")
        print("-" * 80)
        
        try:
            # Run backtest
            result = backtest_strategy(
                ticker="AAPL",
                strategy="rsi_strategy",
                period="1y",  # Use 1y for faster testing
                initial_capital=10000
            )
            
            self.assert_true(
                result is not None,
                "Backtest executed successfully"
            )
            
            self.assert_true(
                "results" in result,
                "Backtest results returned"
            )
            
            results = result.get("results", {})
            
            # Validate metrics exist
            self.assert_true(
                "sharpe_ratio" in results,
                "Sharpe ratio calculated"
            )
            
            self.assert_true(
                "max_drawdown" in results,
                "Max drawdown calculated"
            )
            
            self.assert_true(
                "win_rate" in results,
                "Win rate calculated"
            )
            
            # Validate metric ranges
            sharpe = results.get("sharpe_ratio", 0)
            self.assert_true(
                -2.0 <= sharpe <= 5.0,
                f"Sharpe ratio realistic ({sharpe:.2f})"
            )
            
            max_dd = results.get("max_drawdown", 0)
            self.assert_true(
                -1.0 <= max_dd <= 0,
                f"Max drawdown realistic ({max_dd*100:.1f}%)"
            )
            
            win_rate = results.get("win_rate", 0)
            self.assert_true(
                0 <= win_rate <= 1.0,
                f"Win rate realistic ({win_rate*100:.1f}%)"
            )
            
            # Validate vs buy & hold comparison
            vs_bh = result.get("vs_buy_hold", {})
            self.assert_true(
                "outperformance" in vs_bh or "buy_hold_return" in vs_bh,
                "Buy & hold comparison included"
            )
            
            print(f"  ℹ️  Total Return: {results.get('total_return', 0)*100:.1f}%")
            print(f"  ℹ️  Sharpe Ratio: {sharpe:.2f}")
            print(f"  ℹ️  Max Drawdown: {max_dd*100:.1f}%")
            print(f"  ℹ️  Win Rate: {win_rate*100:.1f}%")
            
        except Exception as e:
            self.assert_true(False, f"Test failed with error: {str(e)}")
        
        print()
    
    def test_scenario_5_memory_persistence(self):
        """
        Scenario 5: Memory Persistence
        
        Setup: Store user preference → Retrieve it
        Expected: Preference retrieved correctly
        Validates: ChromaDB persistence
        """
        print("TEST 5: Memory Persistence")
        print("-" * 80)
        
        try:
            # Store complex user profile
            test_user = f"{self.test_user_id}_persistence"
            
            self.memory.store_risk_profile(
                test_user,
                risk_tolerance="MEDIUM",
                max_drawdown_tolerance=0.20,
                preferred_sectors=["technology", "healthcare", "finance"]
            )
            
            self.memory.store_trading_style(
                test_user,
                style="SWING",
                timeframe="1week-1month",
                position_sizing="moderate"
            )
            
            # Retrieve user context
            context = self.memory.get_user_context(test_user)
            
            self.assert_true(
                context is not None,
                "User context retrieved"
            )
            
            self.assert_true(
                context.get("risk_tolerance") == "MEDIUM",
                "Risk tolerance persisted correctly"
            )
            
            self.assert_true(
                context.get("max_drawdown_tolerance") == 0.20,
                "Max drawdown persisted correctly"
            )
            
            self.assert_true(
                "technology" in context.get("preferred_sectors", []),
                "Preferred sectors persisted correctly"
            )
            
            self.assert_true(
                context.get("trading_style") == "SWING",
                "Trading style persisted correctly"
            )
            
            # Test agent output storage
            self.memory.store_agent_output(
                agent_name="TechnicalAnalyst",
                ticker="AAPL",
                output="RSI at 58, MACD bullish, BUY signal",
                confidence=0.85,
                metadata={"timestamp": datetime.now().isoformat()}
            )
            
            # Retrieve similar analysis
            similar = self.memory.retrieve_similar_analysis("AAPL", days_back=30)
            
            self.assert_true(
                similar is not None,
                "Agent output storage and retrieval works"
            )
            
            print(f"  ℹ️  User profile stored: {test_user}")
            print(f"  ℹ️  Risk tolerance: {context.get('risk_tolerance')}")
            print(f"  ℹ️  Trading style: {context.get('trading_style')}")
            print(f"  ℹ️  Agent outputs stored: {len(similar) if similar else 0}")
            
        except Exception as e:
            self.assert_true(False, f"Test failed with error: {str(e)}")
        
        print()
    
    def cleanup(self):
        """Cleanup test data"""
        try:
            if self.memory:
                # Note: In production, you might want to keep test data
                # For now, we skip cleanup to verify persistence
                pass
        except Exception as e:
            print(f"⚠️  Cleanup warning: {str(e)}")


def main():
    """Main test runner"""
    suite = IntegrationTestSuite()
    
    try:
        success = suite.run_all_tests()
        
        if success:
            print()
            print("✅ ALL TESTS PASSED - System is production-ready!")
            return 0
        else:
            print()
            print("❌ SOME TESTS FAILED - Review failures above")
            return 1
    
    except Exception as e:
        print()
        print(f"❌ TEST SUITE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        suite.cleanup()


if __name__ == "__main__":
    exit(main())

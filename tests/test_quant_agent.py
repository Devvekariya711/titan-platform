"""
Tests for Titan Quant Agent - Phase 1
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from market_analyst.quant_tools import get_market_data, calculate_technicals, analyze_price_action


class TestMarketDataTool:
    """Test the get_market_data function"""
    
    def test_valid_ticker(self):
        """Test with a valid ticker symbol"""
        result = get_market_data("AAPL", period="1mo")
        assert result["success"] == True
        assert "current_price" in result
        assert "price_change_pct" in result
        assert result["ticker"] == "AAPL"
        assert len(result["ohlcv"]) > 0
    
    def test_invalid_ticker(self):
        """Test with an invalid ticker symbol"""
        result = get_market_data("FAKESYMBOL123", period="1mo")
        assert result["success"] == False
        assert "error" in result
    
    def test_different_periods(self):
        """Test with different time periods"""
        periods = ["1d", "5d", "1mo", "3mo"]
        for period in periods:
            result = get_market_data("TSLA", period=period)
            assert result["success"] == True
            assert result["period"] == period


class TestTechnicalIndicatorsTool:
    """Test the calculate_technicals function"""
    
    def test_calculate_rsi(self):
        """Test RSI calculation"""
        result = calculate_technicals("NVDA", period="3mo")
        assert result["success"] == True
        assert "indicators" in result
        assert "rsi" in result["indicators"]
        
        # RSI should be between 0 and 100
        if result["indicators"]["rsi"] is not None:
            assert 0 <= result["indicators"]["rsi"] <= 100
    
    def test_calculate_macd(self):
        """Test MACD calculation"""
        result = calculate_technicals("AAPL", period="3mo")
        assert result["success"] == True
        assert "macd" in result["indicators"]
        assert "macd_signal" in result["indicators"]
        assert "macd_interpretation" in result["indicators"]
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        result = calculate_technicals("TSLA", period="3mo")
        assert result["success"] == True
        ind = result["indicators"]
        
        # Upper band should be greater than middle, middle greater than lower
        if all([ind["bollinger_upper"], ind["bollinger_middle"], ind["bollinger_lower"]]):
            assert ind["bollinger_upper"] > ind["bollinger_middle"]
            assert ind["bollinger_middle"] > ind["bollinger_lower"]
    
    def test_moving_averages(self):
        """Test moving average calculations"""
        result = calculate_technicals("NVDA", period="1y")  # Need longer period for 200-day MA
        assert result["success"] == True
        # SMA values may be None if not enough data
        assert "sma_50" in result["indicators"]
        assert "sma_200" in result["indicators"]


class TestPriceActionTool:
    """Test the analyze_price_action function"""
    
    def test_trend_detection(self):
        """Test trend detection"""
        result = analyze_price_action("AAPL", period="3mo")
        assert result["success"] == True
        assert "trend" in result
        assert result["trend"] in [
            "Strong Uptrend", "Uptrend", "Sideways/Consolidation", 
            "Downtrend", "Strong Downtrend"
        ]
    
    def test_support_resistance(self):
        """Test support and resistance levels"""
        result = analyze_price_action("NVDA", period="3mo")
        assert result["success"] == True
        assert "support_level" in result
        assert "resistance_level" in result
        assert "pivot_point" in result
        
        # Support should be less than resistance
        assert result["support_level"] < result["resistance_level"]
    
    def test_momentum_calculation(self):
        """Test momentum calculation"""
        result = analyze_price_action("TSLA", period="3mo")
        assert result["success"] == True
        assert "momentum_30d" in result
        # Momentum is percentage change, should be a reasonable number
        assert -100 <= result["momentum_30d"] <= 500  # Allow for extreme cases


class TestToolIntegration:
    """Integration tests for all tools working together"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        ticker = "AAPL"
        
        # Step 1: Get market data
        market_data = get_market_data(ticker, period="1mo")
        assert market_data["success"] == True
        
        # Step 2: Calculate technicals
        technicals = calculate_technicals(ticker, period="3mo")
        assert technicals["success"] == True
        
        # Step 3: Analyze price action
        price_action = analyze_price_action(ticker, period="3mo")
        assert price_action["success"] == True
        
        # All should agree on current price (within a small margin due to timing)
        prices = [
            market_data["current_price"],
            technicals["current_price"],
            price_action["current_price"]
        ]
        # Prices should be within 5% of each other
        max_price = max(prices)
        min_price = min(prices)
        assert (max_price - min_price) / min_price < 0.05


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

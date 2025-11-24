"""
Phase 1 Demo - Titan Quant Agent
Demonstrates the Quant Agent's technical analysis capabilities
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from market_analyst.quant_tools import get_market_data, calculate_technicals, analyze_price_action


def test_tools():
    """Test the three quant tools with real market data"""
    print("=" * 80)
    print("TITAN PHASE 1 DEMO - Quant Agent Technical Analysis")
    print("=" * 80)
    
    tickers = ["NVDA", "AAPL", "TSLA"]
    
    for ticker in tickers:
        print(f"\n{'=' * 80}")
        print(f"Testing Ticker: {ticker}")
        print("=" * 80)
        
        # Tool 1: Market Data
        print(f"\n[1] Market Data for {ticker}:")
        print("-" * 80)
        market_data = get_market_data(ticker, period="1mo")
        if market_data.get("success"):
            print(f"  Current Price: ${market_data['current_price']}")
            print(f"  Price Change: {market_data['price_change_pct']:.2f}%")
            print(f"  Avg Volume: {market_data['volume_avg']:,}")
            print(f"  Data Points: {market_data['data_points']}")
            print(f"\n  Recent OHLCV (last 5 days):")
            for day in market_data['ohlcv']:
                print(f"    {day['date']}: O=${day['open']} H=${day['high']} L=${day['low']} C=${day['close']}")
        else:
            print(f"  Error: {market_data.get('error')}")
        
        # Tool 2: Technical Indicators
        print(f"\n[2] Technical Indicators for {ticker}:")
        print("-" * 80)
        technicals = calculate_technicals(ticker, period="3mo")
        if technicals.get("success"):
            ind = technicals['indicators']
            print(f"  RSI (14): {ind['rsi']} → {ind['rsi_signal']}")
            print(f"  MACD: {ind['macd']} (Signal: {ind['macd_signal']}) → {ind['macd_interpretation']}")
            print(f"  Bollinger Bands:")
            print(f"    Upper: ${ind['bollinger_upper']}")
            print(f"    Middle: ${ind['bollinger_middle']}")
            print(f"    Lower: ${ind['bollinger_lower']}")
            print(f"    Position: {ind['bollinger_position']}")
            print(f"  Moving Averages:")
            print(f"    50-day: ${ind['sma_50']}" if ind['sma_50'] else "    50-day: Not enough data")
            print(f"    200-day: ${ind['sma_200']}" if ind['sma_200'] else "    200-day: Not enough data")
            if ind['ma_trend']:
                print(f"    Trend: {ind['ma_trend']}")
            print(f"  Volume: {ind['volume_signal']} (Ratio: {ind['volume_ratio']}x)")
        else:
            print(f"  Error: {technicals.get('error')}")
        
        # Tool 3: Price Action
        print(f"\n[3] Price Action Analysis for {ticker}:")
        print("-" * 80)
        price_action = analyze_price_action(ticker, period="3mo")
        if price_action.get("success"):
            print(f"  Trend: {price_action['trend']} (Strength: {price_action['trend_strength']})")
            print(f"  Support Level: ${price_action['support_level']}")
            print(f"  Resistance Level: ${price_action['resistance_level']}")
            print(f"  Pivot Point: ${price_action['pivot_point']}")
            if price_action['pattern']:
                print(f"  Pattern Detected: {price_action['pattern']}")
            print(f"  30-Day Momentum: {price_action['momentum_30d']:.2f}%")
            print(f"  Price Range: ${price_action['price_range']['low']} - ${price_action['price_range']['high']}")
        else:
            print(f"  Error: {price_action.get('error')}")
    
    print(f"\n{'=' * 80}")
    print("Demo Complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        test_tools()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError running demo: {e}")
        import traceback
        traceback.print_exc()

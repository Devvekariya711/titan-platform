"""
Mock Market Service - Static data for Agent Squad development
Allows agents to work independently of external APIs during development
"""
from datetime import datetime, timedelta
from typing import Dict, Any


class MockMarketService:
    """
    Provides static mock data for AAPL, TSLA, and BTC
    Used for agent development and testing without API dependencies
    """

    # Static mock data
    MOCK_DATA = {
        "AAPL": {
            "ticker": "AAPL",
            "current_price": 195.50,
            "volume_avg_30d": 45000000,
            "high_52w": 199.62,
            "low_52w": 164.08,
            "rsi": 58.3,
            "macd": 2.15,
            "macd_signal": 1.87,
            "sma_50": 185.30,
            "sma_200": 175.80,
            "bollinger_upper": 198.20,
            "bollinger_middle": 195.50,
            "bollinger_lower": 192.80,
            "trend": "Uptrend",
            "support": 190.00,
            "resistance": 199.50
        },
        "TSLA": {
            "ticker": "TSLA",
            "current_price": 242.80,
            "volume_avg_30d": 120000000,
            "high_52w": 299.29,
            "low_52w": 138.80,
            "rsi": 73.5,
            "macd": -1.2,
            "macd_signal": -0.8,
            "sma_50": 235.40,
            "sma_200": 210.50,
            "bollinger_upper": 250.00,
            "bollinger_middle": 242.50,
            "bollinger_lower": 235.00,
            "trend": "Strong Uptrend",
            "support": 235.00,
            "resistance": 250.00
        },
        "BTC-USD": {
            "ticker": "BTC-USD",
            "current_price": 43250.00,
            "volume_avg_30d": 25000000000,
            "high_52w": 48000.00,
            "low_52w": 25000.00,
            "rsi": 45.2,
            "macd": 125.5,
            "macd_signal": 110.3,
            "sma_50": 41500.00,
            "sma_200": 38000.00,
            "bollinger_upper": 45000.00,
            "bollinger_middle": 43000.00,
            "bollinger_lower": 41000.00,
            "trend": "Sideways",
            "support": 40000.00,
            "resistance": 45000.00
        }
    }

    @staticmethod
    def get_market_data(ticker: str) -> Dict[str, Any]:
        """
        Get mock OHLCV data

        Args:
            ticker: Stock symbol (AAPL, TSLA, BTC-USD)

        Returns:
            Mock market data
        """
        if ticker not in MockMarketService.MOCK_DATA:
            return {
                "ticker": ticker,
                "error": f"Mock data not available for {ticker}. Available: AAPL, TSLA, BTC-USD",
                "success": False}

        data = MockMarketService.MOCK_DATA[ticker].copy()
        data["success"] = True
        data["timestamp"] = datetime.now().isoformat()
        data["source"] = "MockMarketService"

        # Generate fake OHLCV for last 5 days
        base_price = data["current_price"]
        ohlcv = []
        for i in range(5, 0, -1):
            date = datetime.now() - timedelta(days=i)
            variance = (5 - i) * 0.01  # Small variance
            ohlcv.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(base_price * (1 - variance), 2),
                "high": round(base_price * (1 + variance), 2),
                "low": round(base_price * (1 - variance * 1.5), 2),
                "close": round(base_price * (1 + variance * 0.5), 2),
                "volume": int(data["volume_avg_30d"] * (1 + variance))
            })

        data["ohlcv"] = ohlcv
        return data

    @staticmethod
    def get_technicals(ticker: str) -> Dict[str, Any]:
        """
        Get mock technical indicators

        Args:
            ticker: Stock symbol

        Returns:
            Mock technical indicators
        """
        if ticker not in MockMarketService.MOCK_DATA:
            return {
                "ticker": ticker,
                "error": f"Mock data not available for {ticker}",
                "success": False
            }

        data = MockMarketService.MOCK_DATA[ticker]

        # Interpret RSI
        rsi_signal = "Overbought" if data["rsi"] > 70 else "Oversold" if data["rsi"] < 30 else "Neutral"

        # Interpret MACD
        macd_interpretation = "Bullish (MACD above signal)" if data["macd"] > data[
            "macd_signal"] else "Bearish (MACD below signal)"

        # Interpret Bollinger Bands
        price = data["current_price"]
        bb_range = data["bollinger_upper"] - data["bollinger_lower"]
        position_pct = ((price - data["bollinger_lower"]) / bb_range) * 100

        if position_pct > 80:
            bb_position = "Near upper band (potential overbought)"
        elif position_pct < 20:
            bb_position = "Near lower band (potential oversold)"
        else:
            bb_position = "Middle range (neutral)"

        # Interpret MAs
        ma_trend = "Golden Cross territory (Bullish long-term)" if data["sma_50"] > data[
            "sma_200"] else "Death Cross territory (Bearish long-term)"

        return {
            "ticker": ticker,
            "current_price": data["current_price"],
            "indicators": {
                "rsi": data["rsi"],
                "rsi_signal": rsi_signal,
                "macd": data["macd"],
                "macd_signal": data["macd_signal"],
                "macd_interpretation": macd_interpretation,
                "bollinger_upper": data["bollinger_upper"],
                "bollinger_middle": data["bollinger_middle"],
                "bollinger_lower": data["bollinger_lower"],
                "bollinger_position": bb_position,
                "sma_50": data["sma_50"],
                "sma_200": data["sma_200"],
                "ma_trend": ma_trend,
                "volume_ratio": 1.0,
                "volume_signal": "Normal volume"
            },
            "success": True,
            "source": "MockMarketService"
        }

    @staticmethod
    def get_price_action(ticker: str) -> Dict[str, Any]:
        """
        Get mock price action analysis

        Args:
            ticker: Stock symbol

        Returns:
            Mock price action data
        """
        if ticker not in MockMarketService.MOCK_DATA:
            return {
                "ticker": ticker,
                "error": f"Mock data not available for {ticker}",
                "success": False
            }

        data = MockMarketService.MOCK_DATA[ticker]

        # Determine pattern
        pattern = None
        if data["sma_50"] > data["sma_200"]:
            pattern = "Golden Cross (Bullish signal)"

        return {
            "ticker": ticker,
            "current_price": data["current_price"],
            "trend": data["trend"],
            "trend_strength": 0.75,
            "support_level": data["support"],
            "resistance_level": data["resistance"],
            "pivot_point": (
                data["current_price"] + data["support"] + data["resistance"]) / 3,
            "pattern": pattern,
            "momentum_30d": 5.2,
            "price_range": {
                "high": data["high_52w"],
                "low": data["low_52w"],
                "range_pct": (
                    (data["high_52w"] - data["low_52w"]) / data["low_52w"]) * 100},
            "success": True,
            "source": "MockMarketService"}


# Singleton instance
_mock_service = MockMarketService()


def get_mock_service() -> MockMarketService:
    """Get singleton instance"""
    return _mock_service


# Example usage
if __name__ == "__main__":
    service = get_mock_service()

    print("Mock Market Service Test")
    print("=" * 70)

    for ticker in ["AAPL", "TSLA", "BTC-USD"]:
        print(f"\n{ticker}:")
        market_data = service.get_market_data(ticker)
        print(f"  Price: ${market_data['current_price']}")
        print(f"  RSI: {market_data['rsi']}")
        print(f"  Trend: {market_data['trend']}")

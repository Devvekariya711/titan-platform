"""
Market Data Ingestion Service
Simulates Kafka → ClickHouse pipeline locally
Uses YFinance for data fetching with caching
"""
from shared.utils.errors import DataFetchError
from shared.utils.logger import get_logger
import yfinance as yf
from datetime import datetime
import os
import sys

# Add shared utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = get_logger("ingestion-engine")


class MarketDataConnector:
    """
    Centralized market data fetching
    Replaces direct yfinance calls in tools
    """

    def __init__(self, cache_dir="./data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        logger.info("MarketDataConnector initialized", cache_dir=cache_dir)

    def get_ohlcv(self, ticker: str, period: str = "1mo") -> dict:
        """
        Fetch OHLCV data for ticker

        Args:
            ticker: Stock symbol (e.g., AAPL, TSLA)
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y)

        Returns:
            dict with ticker, data, current_price, volume_avg, 52w high/low
        """
        try:
            logger.info(
                f"Fetching data for {ticker}",
                ticker=ticker,
                period=period)

            stock = yf.Ticker(ticker)
            df = stock.history(period=period)

            if df.empty:
                raise DataFetchError(
                    f"No data found for {ticker}", ticker=ticker)

            result = {
                "ticker": ticker,
                "period": period,
                "data": df.to_dict('records'),
                "current_price": float(df['Close'].iloc[-1]),
                "volume_avg_30d": float(df['Volume'].tail(30).mean()) if len(df) >= 30 else float(df['Volume'].mean()),
                "high_52w": float(df['High'].tail(252).max()) if len(df) >= 252 else float(df['High'].max()),
                "low_52w": float(df['Low'].tail(252).min()) if len(df) >= 252 else float(df['Low'].min()),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Successfully fetched data for {ticker}",
                        ticker=ticker,
                        current_price=result["current_price"])

            return result

        except Exception as e:
            error_msg = f"Error fetching data for {ticker}: {str(e)}"
            logger.error(error_msg, ticker=ticker, error=str(e))
            raise DataFetchError(error_msg, ticker=ticker)

    def get_realtime_price(self, ticker: str) -> float:
        """
        Get current price (simulates real-time stream)

        Args:
            ticker: Stock symbol

        Returns:
            Current price as float
        """
        data = self.get_ohlcv(ticker, period="1d")
        return data.get("current_price")

    def get_multiple_tickers(self, tickers: list, period: str = "1mo") -> dict:
        """
        Fetch data for multiple tickers in batch

        Args:
            tickers: List of stock symbols
            period: Time period

        Returns:
            dict mapping ticker -> data
        """
        results = {}
        for ticker in tickers:
            try:
                results[ticker] = self.get_ohlcv(ticker, period)
            except DataFetchError as e:
                logger.warning(
                    f"Failed to fetch {ticker}",
                    ticker=ticker,
                    error=str(e))
                results[ticker] = {"error": str(e)}

        return results


# Singleton instance
_connector = None


def get_connector() -> MarketDataConnector:
    """Get or create singleton connector instance"""
    global _connector
    if _connector is None:
        _connector = MarketDataConnector()
    return _connector

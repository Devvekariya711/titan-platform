"""
Historical Data Loader for Backtest Engine
Downloads and caches 5 years of OHLCV data from yfinance
Month 3 Week 2
"""
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Optional
import sys

# Add shared utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from shared.utils.logger import get_logger
from shared.utils.errors import DataFetchError

logger = get_logger("data-loader")

class DataLoader:
    """
    Loads and caches historical market data
    """
    
    def __init__(self, cache_dir="./data/historical"):
        """
        Initialize data loader
        
        Args:
            cache_dir: Directory to cache downloaded data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        logger.info("DataLoader initialized", cache_dir=cache_dir)
    
    def download_historical_data(self, ticker: str, start_date: str = None, 
                                 end_date: str = None, cache: bool = True) -> pd.DataFrame:
        """
        Download historical OHLCV data
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD), default 5 years ago
            end_date: End date (YYYY-MM-DD), default today
            cache: Whether to cache the data
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Default to 5 years of data
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
            
            logger.info(f"Downloading data for {ticker}", 
                       ticker=ticker, start=start_date, end=end_date)
            
            # Download from yfinance
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                raise DataFetchError(f"No data returned for {ticker}")
            
            # Add ticker column
            data['Ticker'] = ticker
            
            # Cache to CSV if requested
            if cache:
                cache_file = os.path.join(self.cache_dir, f"{ticker}.csv")
                data.to_csv(cache_file)
                logger.info(f"Cached data to {cache_file}", ticker=ticker, rows=len(data))
            
            logger.info(f"Downloaded {len(data)} days of data", ticker=ticker)
            return data
            
        except Exception as e:
            raise DataFetchError(f"Failed to download data for {ticker}: {str(e)}")
    
    def load_cached_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Load data from cache
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            DataFrame or None if not cached
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{ticker}.csv")
            
            if not os.path.exists(cache_file):
                logger.warning(f"No cache found for {ticker}", ticker=ticker)
                return None
            
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            logger.info(f"Loaded cached data", ticker=ticker, rows=len(data))
            return data
            
        except Exception as e:
            logger.error(f"Failed to load cache: {str(e)}", ticker=ticker, error=str(e))
            return None
    
    def get_data(self, ticker: str, start_date: str = None, end_date: str = None,
                 use_cache: bool = True) -> pd.DataFrame:
        """
        Get historical data (from cache if available, otherwise download)
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date
            end_date: End date
            use_cache: Whether to use cached data
        
        Returns:
            DataFrame with OHLCV data
        """
        # Try cache first
        if use_cache:
            cached_data = self.load_cached_data(ticker)
            if cached_data is not None:
                # Filter by date range if specified
                if start_date or end_date:
                    if start_date:
                        cached_data = cached_data[cached_data.index >= start_date]
                    if end_date:
                        cached_data = cached_data[cached_data.index <= end_date]
                return cached_data
        
        # Download if cache miss
        return self.download_historical_data(ticker, start_date, end_date, cache=True)
    
    def get_price_at_date(self, ticker: str, date: str) -> float:
        """
        Get closing price at specific date
        
        Args:
            ticker: Stock ticker
            date: Date (YYYY-MM-DD)
        
        Returns:
            Closing price
        """
        try:
            data = self.get_data(ticker)
            
            # Find closest date
            target_date = pd.to_datetime(date)
            closest_date = data.index[data.index.searchsorted(target_date)]
            
            price = data.loc[closest_date, 'Close']
            
            logger.info(f"Price at {date}", ticker=ticker, price=price)
            return float(price)
            
        except Exception as e:
            raise DataFetchError(f"Failed to get price for {ticker} at {date}: {str(e)}")
    
    def get_ohlcv_at_date(self, ticker: str, date: str) -> dict:
        """
        Get OHLCV data at specific date
        
        Args:
            ticker: Stock ticker
            date: Date (YYYY-MM-DD)
        
        Returns:
            Dictionary with OHLCV values
        """
        try:
            data = self.get_data(ticker)
            
            target_date = pd.to_datetime(date)
            closest_date = data.index[data.index.searchsorted(target_date)]
            
            row = data.loc[closest_date]
            
            return {
                'date': str(closest_date.date()),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            }
            
        except Exception as e:
            raise DataFetchError(f"Failed to get OHLCV for {ticker} at {date}: {str(e)}")

# Singleton
_data_loader = None

def get_data_loader() -> DataLoader:
    """Get or create singleton DataLoader"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader

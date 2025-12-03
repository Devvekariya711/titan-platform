"""
Quant Tools - Advanced Technical Analysis for Titan Platform
Migrated from Phase 1 market_analyst/quant_tools.py to new structure
Contains: 3 tools (Month 1), will expand to 8 tools (Month 2+)
"""
from google.adk.tools import FunctionTool
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from typing import Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add services to path for data connector
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import importlib
ingestion_module = importlib.import_module('services.ingestion-engine.connectors')
get_connector = ingestion_module.get_connector

# Use centralized connector
connector = get_connector()

# ================== TOOL 1: GET MARKET DATA ==================

def get_market_data(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) market data
    Uses centralized MarketDataConnector service
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'NVDA')
        period: Time period - Valid: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    Returns:
        Dictionary with market data and metrics
    """
    try:
        # Use centralized service
        result = connector.get_ohlcv(ticker, period)
        
        # Transform for compatibility with existing agents
        if "error" in result:
            return {"ticker": ticker, "error": result["error"], "success": False}
        
        # Extract recent OHLCV from data
        ohlcv_list = []
        recent_data = result["data"][-5:] if len(result["data"]) >= 5 else result["data"]
        
        for item in recent_data:
            ohlcv_list.append({
                "date": item.get("Date", "Unknown"),
                "open": item.get("Open", 0),
                "high": item.get("High", 0),
                "low": item.get("Low", 0),
                "close": item.get("Close", 0),
                "volume": item.get("Volume", 0)
            })
        
        return {
            "ticker": ticker,
            "period": period,
            "current_price": result["current_price"],
            "volume_avg": int(result["volume_avg_30d"]),
            "ohlcv": ohlcv_list,
            "success": True
        }
        
    except Exception as e:
        return {
            "ticker": ticker,
            "error": f"Error fetching data: {str(e)}",
            "success": False
        }

# ================== TOOL 2: CALCULATE TECHNICAL INDICATORS ==================

def calculate_technicals(ticker: str, period: str = "3mo") -> Dict[str, Any]:
    """
    Calculates comprehensive technical indicators
    
    Indicators:
    - RSI (14 period)
    - MACD (12,26,9)
    - Bollinger Bands (20, 2 std)
    - Moving Averages (50-day, 200-day SMA)
    - Volume Analysis (vs 30-day avg)
    
    Args:
        ticker: Stock ticker symbol
        period: Time period (recommended: 3mo or 6mo for accurate MAs)
    
    Returns:
        Dictionary with all technical indicators
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return {"ticker": ticker, "error": f"No data found for {ticker}", "success": False}
        
        # Calculate RSI (14-period)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        current_rsi = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None
        
        # Calculate MACD (12, 26, 9)
        macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        current_macd = float(macd['MACD_12_26_9'].iloc[-1]) if macd is not None and not pd.isna(macd['MACD_12_26_9'].iloc[-1]) else None
        current_macd_signal = float(macd['MACDs_12_26_9'].iloc[-1]) if macd is not None and not pd.isna(macd['MACDs_12_26_9'].iloc[-1]) else None
        current_macd_hist = float(macd['MACDh_12_26_9'].iloc[-1]) if macd is not None and not pd.isna(macd['MACDh_12_26_9'].iloc[-1]) else None
        
        # Calculate Bollinger Bands (20, 2)
        bbands = ta.bbands(df['Close'], length=20, std=2)
        bb_upper = float(bbands['BBU_20_2.0'].iloc[-1]) if bbands is not None and not pd.isna(bbands['BBU_20_2.0'].iloc[-1]) else None
        bb_middle = float(bbands['BBM_20_2.0'].iloc[-1]) if bbands is not None and not pd.isna(bbands['BBM_20_2.0'].iloc[-1]) else None
        bb_lower = float(bbands['BBL_20_2.0'].iloc[-1]) if bbands is not None and not pd.isna(bbands['BBL_20_2.0'].iloc[-1]) else None
        
        # Calculate Moving Averages
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['SMA_200'] = ta.sma(df['Close'], length=200)
        sma_50 = float(df['SMA_50'].iloc[-1]) if not pd.isna(df['SMA_50'].iloc[-1]) else None
        sma_200 = float(df['SMA_200'].iloc[-1]) if not pd.isna(df['SMA_200'].iloc[-1]) else None
        
        # Volume Analysis
        volume_30d_avg = float(df['Volume'].tail(30).mean())
        current_volume = float(df['Volume'].iloc[-1])
        volume_ratio = current_volume / volume_30d_avg if volume_30d_avg > 0 else 1.0
        
        current_price = float(df['Close'].iloc[-1])
        
        # Interpret RSI
        rsi_signal = None
        if current_rsi:
            rsi_signal = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
        
        # Interpret MACD
        macd_signal_interpretation = None
        if current_macd is not None and current_macd_signal is not None:
            macd_signal_interpretation = "Bullish (MACD above signal)" if current_macd > current_macd_signal else "Bearish (MACD below signal)"
        
        # Interpret Bollinger Bands
        bb_position = None
        if bb_upper and bb_lower and current_price:
            bb_range = bb_upper - bb_lower
            position_pct = ((current_price - bb_lower) / bb_range) * 100 if bb_range > 0 else 50
            if position_pct > 80:
                bb_position = "Near upper band (potential overbought)"
            elif position_pct < 20:
                bb_position = "Near lower band (potential oversold)"
            else:
                bb_position = "Middle range (neutral)"
        
        # Interpret Moving Averages
        ma_trend = None
        if sma_50 and sma_200:
            ma_trend = "Golden Cross territory (Bullish long-term)" if sma_50 > sma_200 else "Death Cross territory (Bearish long-term)"
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "indicators": {
                "rsi": round(current_rsi, 2) if current_rsi else None,
                "rsi_signal": rsi_signal,
                "macd": round(current_macd, 4) if current_macd else None,
                "macd_signal": round(current_macd_signal, 4) if current_macd_signal else None,
                "macd_histogram": round(current_macd_hist, 4) if current_macd_hist else None,
                "macd_interpretation": macd_signal_interpretation,
                "bollinger_upper": round(bb_upper, 2) if bb_upper else None,
                "bollinger_middle": round(bb_middle, 2) if bb_middle else None,
                "bollinger_lower": round(bb_lower, 2) if bb_lower else None,
                "bollinger_position": bb_position,
                "sma_50": round(sma_50, 2) if sma_50 else None,
                "sma_200": round(sma_200, 2) if sma_200 else None,
                "ma_trend": ma_trend,
                "volume_ratio": round(volume_ratio, 2),
                "volume_signal": "High volume" if volume_ratio > 1.5 else "Normal volume" if volume_ratio > 0.7 else "Low volume"
            },
            "success": True
        }
        
    except Exception as e:
        return {
            "ticker": ticker,
            "error": f"Error calculating technicals: {str(e)}",
            "success": False
        }

# ================== TOOL 3: ANALYZE PRICE ACTION ==================

def analyze_price_action(ticker: str, period: str = "3mo") -> Dict[str, Any]:
    """
    Analyzes price action to identify trends, support/resistance, chart patterns
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for analysis
    
    Returns:
        Dictionary with trend analysis and pattern detection
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return {"ticker": ticker, "error": f"No data found for {ticker}", "success": False}
        
        current_price = float(df['Close'].iloc[-1])
        
        # Calculate trend using linear regression
        df['Index'] = np.arange(len(df))
        slope = np.polyfit(df['Index'], df['Close'], 1)[0]
        
        # Determine trend
        if slope > 0.5:
            trend = "Strong Uptrend"
        elif slope > 0.1:
            trend = "Uptrend"
        elif slope < -0.5:
            trend = "Strong Downtrend"
        elif slope < -0.1:
            trend = "Downtrend"
        else:
            trend = "Sideways/Consolidation"
        
        # Calculate support and resistance (pivot points)
        high_max = float(df['High'].max())
        low_min = float(df['Low'].min())
        pivot = (high_max + low_min + current_price) / 3
        
        resistance_1 = (2 * pivot) - low_min
        support_1 = (2 * pivot) - high_max
        
        # Detect Golden Cross / Death Cross
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['SMA_200'] = ta.sma(df['Close'], length=200)
        
        pattern_detected = None
        if len(df) >= 200:
            sma_50_current = df['SMA_50'].iloc[-1]
            sma_200_current = df['SMA_200'].iloc[-1]
            sma_50_prev = df['SMA_50'].iloc[-5] if len(df) >= 5 else None
            sma_200_prev = df['SMA_200'].iloc[-5] if len(df) >= 5 else None
            
            if sma_50_prev and sma_200_prev and not pd.isna(sma_50_current) and not pd.isna(sma_200_current):
                # Golden Cross: 50 crosses above 200
                if sma_50_prev < sma_200_prev and sma_50_current > sma_200_current:
                    pattern_detected = "Golden Cross (Bullish signal)"
                # Death Cross: 50 crosses below 200
                elif sma_50_prev > sma_200_prev and sma_50_current < sma_200_current:
                    pattern_detected = "Death Cross (Bearish signal)"
        
        # Price momentum
        price_30d_ago = float(df['Close'].iloc[-min(30, len(df))])
        momentum_pct = ((current_price - price_30d_ago) / price_30d_ago) * 100
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "trend": trend,
            "trend_strength": round(abs(slope), 4),
            "support_level": round(support_1, 2),
            "resistance_level": round(resistance_1, 2),
            "pivot_point": round(pivot, 2),
            "pattern": pattern_detected,
            "momentum_30d": round(momentum_pct, 2),
            "price_range": {
                "high": round(high_max, 2),
                "low": round(low_min, 2),
                "range_pct": round(((high_max - low_min) / low_min) * 100, 2)
            },
            "success": True
        }
        
    except Exception as e:
        return {
            "ticker": ticker,
            "error": f"Error analyzing price action: {str(e)}",
            "success": False
        }

# ================== WRAP AS ADK TOOLS ==================

market_data_tool = FunctionTool(func=get_market_data)
technical_indicators_tool = FunctionTool(func=calculate_technicals)
price_action_tool = FunctionTool(func=analyze_price_action)

# Export
__all__ = ['market_data_tool', 'technical_indicators_tool', 'price_action_tool',
           'get_market_data', 'calculate_technicals', 'analyze_price_action']

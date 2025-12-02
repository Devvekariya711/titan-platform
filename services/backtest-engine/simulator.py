"""
Backtest Engine Service
Historical simulation and strategy validation
Month 3 Week 2 - FULLY OPERATIONAL
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import os
import sys

# Add shared utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from shared.utils.logger import get_logger
from .data_loader import get_data_loader
from .metrics import PerformanceMetrics

logger = get_logger("backtest-engine")

class VirtualPortfolio:
    """
    Tracks portfolio state during backtest
    """
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0
        self.portfolio_values = [initial_capital]
        self.trades = []
        self.daily_returns = []
    
    def buy(self, price: float, date: str, shares: int = None):
        """Buy shares"""
        if shares is None:
            # Buy as many shares as possible
            shares = int(self.cash / price)
        
        cost = shares * price
        if cost > self.cash:
            logger.warning("Insufficient funds for buy", cash=self.cash, cost=cost)
            return False
        
        self.cash -= cost
        self.shares += shares
        
        self.trades.append({
            'date': date,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'value': cost,
            'profit': 0
        })
        
        logger.info("Buy executed", shares=shares, price=price, date=date)
        return True
    
    def sell(self, price: float, date: str, shares: int = None):
        """Sell shares"""
        if shares is None:
            shares = self.shares
        
        if shares > self.shares:
            logger.warning("Insufficient shares for sell", owned=self.shares, trying_to_sell=shares)
            return False
        
        revenue = shares * price
        self.cash += revenue
        
        # Calculate profit
        if self.trades:
            # Find last buy price
            buy_trades = [t for t in self.trades if t['action'] == 'BUY']
            if buy_trades:
                last_buy_price = buy_trades[-1]['price']
                profit = (price - last_buy_price) * shares
            else:
                profit = 0
        else:
            profit = 0
        
        self.shares -= shares
        
        self.trades.append({
            'date': date,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'value': revenue,
            'profit': profit
        })
        
        logger.info("Sell executed", shares=shares, price=price, profit=profit, date=date)
        return True
    
    def get_total_value(self, current_price: float) -> float:
        """Get current portfolio value"""
        return self.cash + (self.shares * current_price)
    
    def record_value(self, current_price: float):
        """Record current portfolio value"""
        total_value = self.get_total_value(current_price)
        self.portfolio_values.append(total_value)
        
        # Calculate daily return
        if len(self.portfolio_values) > 1:
            prev_value = self.portfolio_values[-2]
            daily_return = (total_value - prev_value) / prev_value
            self.daily_returns.append(daily_return)


class BacktestEngine:
    """
    Historical strategy validation
    """
    
    def __init__(self, historical_data_dir="./data/historical"):
        self.historical_data_dir = historical_data_dir
        self.data_loader = get_data_loader()
        logger.info("BacktestEngine initialized (OPERATIONAL)")
    
    def run_backtest(self, ticker: str, strategy: str, start_date: str, end_date: str,
                    initial_capital: float = 100000.0) -> Dict[str, Any]:
        """
        Run backtest with specified strategy
        
        Args:
            ticker: Stock ticker
            strategy: Strategy name (buy_and_hold, rsi_strategy, ma_crossover)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            initial_capital: Starting capital
        
        Returns:
            Performance metrics and trade history
        """
        try:
            logger.info(f"Running backtest", ticker=ticker, strategy=strategy, 
                       start=start_date, end=end_date)
            
            # Load historical data
            data = self.data_loader.get_data(ticker, start_date, end_date)
            
            if data.empty:
                return {"status": "error", "message": "No data available"}
            
            # Initialize portfolio
            portfolio = VirtualPortfolio(initial_capital)
            
            # Execute strategy
            if strategy == "buy_and_hold":
                self._execute_buy_and_hold(data,portfolio)
            elif strategy == "rsi_strategy":
                self._execute_rsi_strategy(data, portfolio)
            elif strategy == "ma_crossover":
                self._execute_ma_crossover(data, portfolio)
            else:
                return {"status": "error", "message": f"Unknown strategy: {strategy}"}
            
            # Calculate performance metrics
            returns_series = pd.Series(portfolio.daily_returns)
            
            # Calculate buy-and-hold return for comparison
            buy_hold_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / 
                             data['Close'].iloc[0]) * 100
            
            metrics = PerformanceMetrics.generate_report(
                portfolio_values=portfolio.portfolio_values,
                trades=portfolio.trades,
                returns=returns_series,
                buy_hold_return=buy_hold_return
            )
            
            result = {
                "ticker": ticker,
                "strategy": strategy,
                "start_date": start_date,
                "end_date": end_date,
                "initial_capital": initial_capital,
                "final_value": portfolio.portfolio_values[-1],
                "metrics": metrics,
                "num_trades": len(portfolio.trades),
                "status": "success"
            }
            
            logger.info("Backtest complete", ticker=ticker, 
                       total_return=metrics['total_return'], sharpe=metrics['sharpe_ratio'])
            
            return result
            
        except Exception as e:
            logger.error(f"Backtest failed: {str(e)}", ticker=ticker, error=str(e))
            return {"status": "error", "message": str(e)}
    
    def _execute_buy_and_hold(self, data: pd.DataFrame, portfolio: VirtualPortfolio):
        """Buy at start, hold, sell at end"""
        first_date = data.index[0].strftime('%Y-%m-%d')
        first_price = data['Close'].iloc[0]
        
        # Buy at start
        portfolio.buy(first_price, first_date)
        
        # Record portfolio values daily
        for idx in range(1, len(data)):
            current_price = data['Close'].iloc[idx]
            portfolio.record_value(current_price)
        
        # Sell at end
        last_date = data.index[-1].strftime('%Y-%m-%d')
        last_price = data['Close'].iloc[-1]
        portfolio.sell(last_price, last_date)
    
    def _execute_rsi_strategy(self, data: pd.DataFrame, portfolio: VirtualPortfolio):
        """Buy when RSI < 30, Sell when RSI > 70"""
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        holding = False
        
        for idx in range(14, len(data)):  # Start after RSI calculation period
            current_price = data['Close'].iloc[idx]
            current_rsi = rsi.iloc[idx]
            current_date = data.index[idx].strftime('%Y-%m-%d')
            
            # Buy signal: RSI < 30
            if current_rsi < 30 and not holding:
                portfolio.buy(current_price, current_date)
                holding = True
            
            # Sell signal: RSI > 70
            elif current_rsi > 70 and holding:
                portfolio.sell(current_price, current_date)
                holding = False
            
            portfolio.record_value(current_price)
        
        # Close position at end if still holding
        if holding:
            last_price = data['Close'].iloc[-1]
            last_date = data.index[-1].strftime('%Y-%m-%d')
            portfolio.sell(last_price, last_date)
    
    def _execute_ma_crossover(self, data: pd.DataFrame, portfolio: VirtualPortfolio):
        """Golden cross (50d MA > 200d MA) = Buy, Death cross = Sell"""
        # Calculate moving averages
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()
        
        holding = False
        
        for idx in range(200, len(data)):  # Start after MA calculation period
            current_price = data['Close'].iloc[idx]
            ma50 = data['MA50'].iloc[idx]
            ma200 = data['MA200'].iloc[idx]
            prev_ma50 = data['MA50'].iloc[idx-1]
            prev_ma200 = data['MA200'].iloc[idx-1]
            current_date = data.index[idx].strftime('%Y-%m-%d')
            
            # Golden Cross: MA50 crosses above MA200
            if prev_ma50 < prev_ma200 and ma50 > ma200 and not holding:
                portfolio.buy(current_price, current_date)
                holding = True
            
            # Death Cross: MA50 crosses below MA200
            elif prev_ma50 > prev_ma200 and ma50 < ma200 and holding:
                portfolio.sell(current_price, current_date)
                holding = False
            
            portfolio.record_value(current_price)
        
        # Close position at end if still holding
        if holding:
            last_price = data['Close'].iloc[-1]
            last_date = data.index[-1].strftime('%Y-%m-%d')
            portfolio.sell(last_price, last_date)


# Singleton
_backtest_engine = None

def get_backtest_engine() -> BacktestEngine:
    """Get backtest engine singleton"""
    global _backtest_engine
    if _backtest_engine is None:
        _backtest_engine = BacktestEngine()
    return _backtest_engine

"""
Performance Metrics Calculator for Backtest Engine
Calculates Sharpe ratio, drawdown, win rate, etc.
Month 3 Week 2
"""
from shared.utils.logger import get_logger
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = get_logger("backtest-metrics")


class PerformanceMetrics:
    """
    Calculate backtest performance metrics
    """

    @staticmethod
    def calculate_total_return(portfolio_values: List[float]) -> float:
        """
        Calculate total return percentage

        Args:
            portfolio_values: List of portfolio values over time

        Returns:
            Total return as percentage
        """
        if not portfolio_values or len(portfolio_values) < 2:
            return 0.0

        initial_value = portfolio_values[0]
        final_value = portfolio_values[-1]

        return ((final_value - initial_value) / initial_value) * 100

    @staticmethod
    def calculate_sharpe_ratio(
            returns: pd.Series,
            risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio

        Args:
            returns: Series of daily returns
            risk_free_rate: Annual risk-free rate (default 2%)

        Returns:
            Sharpe ratio
        """
        if returns.empty or returns.std() == 0:
            return 0.0

        # Annualize returns and volatility
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * np.sqrt(252)

        sharpe = (annual_return - risk_free_rate) / annual_volatility
        return round(float(sharpe), 2)

    @staticmethod
    def calculate_max_drawdown(portfolio_values: List[float]) -> float:
        """
        Calculate maximum drawdown percentage

        Args:
            portfolio_values: List of portfolio values

        Returns:
            Maximum drawdown as percentage (negative)
        """
        if not portfolio_values:
            return 0.0

        values = pd.Series(portfolio_values)
        cumulative_max = values.cummax()
        drawdown = (values - cumulative_max) / cumulative_max * 100

        return round(float(drawdown.min()), 2)

    @staticmethod
    def calculate_win_rate(trades: List[Dict[str, Any]]) -> float:
        """
        Calculate win rate

        Args:
            trades: List of trade dictionaries with 'profit' key

        Returns:
            Win rate percentage
        """
        if not trades:
            return 0.0

        winning_trades = sum(
            1 for trade in trades if trade.get(
                'profit', 0) > 0)
        win_rate = (winning_trades / len(trades)) * 100

        return round(win_rate, 1)

    @staticmethod
    def calculate_average_gain_loss(
            trades: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate average gain and loss per trade

        Args:
            trades: List of trade dictionaries

        Returns:
            Dictionary with avg_gain and avg_loss
        """
        if not trades:
            return {'avg_gain': 0.0, 'avg_loss': 0.0}

        gains = [t.get('profit', 0) for t in trades if t.get('profit', 0) > 0]
        losses = [abs(t.get('profit', 0))
                  for t in trades if t.get('profit', 0) < 0]

        avg_gain = round(sum(gains) / len(gains), 2) if gains else 0.0
        avg_loss = round(sum(losses) / len(losses), 2) if losses else 0.0

        return {
            'avg_gain': avg_gain,
            'avg_loss': avg_loss,
            'profit_factor': round(
                avg_gain / avg_loss,
                2) if avg_loss > 0 else 0.0}

    @staticmethod
    def compare_vs_buy_hold(strategy_return: float,
                            buy_hold_return: float) -> Dict[str, Any]:
        """
        Compare strategy vs buy-and-hold

        Args:
            strategy_return: Strategy total return %
            buy_hold_return: Buy-and-hold return %

        Returns:
            Comparison dictionary
        """
        outperformance = strategy_return - buy_hold_return

        if buy_hold_return > 0:
            outperformance_pct = (outperformance / buy_hold_return) * 100
        else:
            outperformance_pct = 0.0

        return {
            'strategy_return': round(strategy_return, 2),
            'buy_hold_return': round(buy_hold_return, 2),
            'outperformance': round(outperformance, 2),
            'outperformance_pct': round(outperformance_pct, 1),
            'beats_buy_hold': outperformance > 0
        }

    @staticmethod
    def generate_report(portfolio_values: List[float],
                        trades: List[Dict[str,
                                          Any]],
                        returns: pd.Series,
                        buy_hold_return: float = None) -> Dict[str,
                                                               Any]:
        """
        Generate comprehensive performance report

        Args:
            portfolio_values: Portfolio values over time
            trades: List of trades
            returns: Daily returns series
            buy_hold_return: Buy-and-hold return for comparison

        Returns:
            Complete performance metrics
        """
        total_return = PerformanceMetrics.calculate_total_return(
            portfolio_values)
        sharpe = PerformanceMetrics.calculate_sharpe_ratio(returns)
        max_dd = PerformanceMetrics.calculate_max_drawdown(portfolio_values)
        win_rate = PerformanceMetrics.calculate_win_rate(trades)
        gain_loss = PerformanceMetrics.calculate_average_gain_loss(trades)

        report = {
            'total_return': round(total_return, 2),
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'win_rate': win_rate,
            'total_trades': len(trades),
            'avg_gain': gain_loss['avg_gain'],
            'avg_loss': gain_loss['avg_loss'],
            'profit_factor': gain_loss['profit_factor']
        }

        if buy_hold_return is not None:
            comparison = PerformanceMetrics.compare_vs_buy_hold(
                total_return, buy_hold_return)
            report['vs_buy_hold'] = comparison

        logger.info(
            "Generated performance report",
            total_return=total_return,
            sharpe=sharpe,
            trades=len(trades))

        return report

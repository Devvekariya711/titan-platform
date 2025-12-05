# Historical Data Directory

## Purpose
This directory stores historical OHLCV (Open, High, Low, Close, Volume) data for stocks used in backtesting and technical analysis.

## Data Format

### File Naming
- Pattern: `{TICKER}.csv`
- Examples: `AAPL.csv`, `TSLA.csv`, `MSFT.csv`

### CSV Structure
```csv
Date,Open,High,Low,Close,Volume
2019-01-02,154.89,158.85,154.23,157.92,37039700
2019-01-03,143.98,145.72,142.00,142.19,91312200
```

### Required Columns
| Column | Type | Description |
|--------|------|-------------|
| Date | YYYY-MM-DD | Trading date |
| Open | float | Opening price |
| High | float | Day's high |
| Low | float | Day's low |
| Close | float | Closing price |
| Volume | int | Shares traded |

## How Data is Populated

### Automatic (Recommended)
The system auto-downloads data via yfinance when you query a stock:
```python
from services.backtest_engine.data_loader import DataLoader
dl = DataLoader()
dl.download_historical_data("AAPL", "2019-01-01", "2024-12-01")
```

### Manual Download
1. Go to https://finance.yahoo.com/quote/AAPL/history
2. Set date range (5 years recommended)
3. Click "Download"
4. Save as `AAPL.csv` in this directory

## Recommended Stocks
Download at least these for testing:
- AAPL (Apple)
- TSLA (Tesla)
- MSFT (Microsoft)
- GOOGL (Google)
- NVDA (NVIDIA)
- AMZN (Amazon)

## Storage Size
- ~1,260 rows per ticker (5 years daily)
- ~50-100 KB per file
- Total: ~500 KB for 6 stocks

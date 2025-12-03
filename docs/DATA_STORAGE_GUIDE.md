# Titan Platform - Data Storage Guide

## 📁 Where Your Data is Stored

### 1. Historical Market Data (5-10 Years)
**Location**: `data/historical/`
**What**: Stock price history (OHLCV - Open, High, Low, Close, Volume)
**Format**: CSV files per ticker (e.g., AAPL.csv, MSFT.csv)
**Size**: ~5-10 MB per ticker for 5 years
**Example**:
```
data/historical/
├── AAPL.csv (2019-2024, ~8 MB)
├── MSFT.csv (2019-2024, ~7 MB)
├── GOOGL.csv (2019-2024, ~9 MB)
└── TSLA.csv (2019-2024, ~12 MB)
```

**Used For**:
- Backtesting strategies
- Trend analysis
- Technical indicators (RSI, MACD, Bollinger Bands)
- Performance validation

---

### 2. User Memory & Learning (Memory Bank)
**Location**: `services/memory-bank/chroma_data/`
**What**: User preferences, past analyses, agent decisions
**Format**: ChromaDB vector database
**Size**: Grows over time (starts ~1 MB, can grow to 100+ MB)

**Stores**:
- **User Risk Profiles**: Your tolerance (LOW/MEDIUM/HIGH), max drawdown
- **Trading Styles**: Long-term vs short-term, position sizing
- **Past Analyses**: What agents recommended for specific stocks
- **Decision Outcomes**: Track if recommendations were successful
- **Learning Patterns**: Improve recommendations based on your feedback

**Example**:
```
services/memory-bank/chroma_data/
├── user_risk_profiles (your settings)
├── trading_styles (your preferences)
├── agent_decisions (past recommendations)
└── analysis_history (what worked, what didn't)
```

**Retention**: 90 days by default (configurable in .env)

---

### 3. Logs (Last 24 Hours - 7 Days)
**Location**: `logs/`
**What**: System activity, agent decisions, tool execution
**Format**: Daily log files with rotation
**Size**: 10 MB per file, keeps 5 backup files

**Example**:
```
logs/
├── titan-20241203.log (today, 8 MB)
├── titan-20241203.log.1 (rotated, 10 MB)
├── titan-20241202.log (yesterday, 10 MB)
├── titan-20241201.log (2 days ago, 10 MB)
└── ... (up to 7 days or 5 files)
```

**Contains**:
- Agent decisions with confidence scores
- Tool execution times
- Errors and warnings
- Performance metrics

**Used For**:
- Debugging issues
- Dashboard statistics
- Performance monitoring
- Audit trail

---

### 4. Temporary Cache (Last 24 Hours)
**Location**: `data/cache/`
**What**: Short-term data caching
**Format**: Temporary files
**Size**: Small (~1-5 MB)

**Stores**:
- Recent API responses (to avoid re-fetching)
- Temporary calculations
- Session data

**Auto-cleaned**: Every 24 hours

---

### 5. Dashboard Snapshots
**Location**: `dashboard.html` (root)
**What**: Latest system metrics snapshot
**Format**: HTML file
**Size**: ~50 KB
**Regenerated**: Every time you view dashboard

---

## 📊 Complete Directory Structure

```
titan-platform/
│
├── data/                         # 💾 DATA STORAGE
│   ├── historical/               # 5-10 year stock data (CSV)
│   │   ├── AAPL.csv
│   │   ├── MSFT.csv
│   │   └── ... (grows as you use)
│   └── cache/                    # 24-hour temp cache
│
├── services/memory-bank/         # 🧠 USER MEMORY & LEARNING
│   └── chroma_data/              # Vector database
│       ├── user_risk_profiles
│       ├── trading_styles
│       ├── agent_decisions
│       └── analysis_history
│
├── logs/                         # 📝 LOGS (7 days retention)
│   ├── titan-20241203.log
│   ├── titan-20241202.log
│   └── ... (up to 5 files)
│
└── dashboard.html                # 📊 Latest metrics snapshot
```

---

## 🎯 Retention Policies

| Data Type | Location | Retention | Configurable |
|-----------|----------|-----------|--------------|
| Historical Stock Data | `data/historical/` | Forever (until deleted) | Manual cleanup |
| User Profiles | `memory-bank/chroma_data/` | 90 days | Yes (.env: MEMORY_RETENTION_DAYS) |
| Logs | `logs/` | 7 days or 5 files | Yes (.env: LOG_ROTATION_DAYS) |
| Cache | `data/cache/` | 24 hours | Yes (.env: CACHE_EXPIRY_DAYS) |
| Dashboard | `dashboard.html` | Until regenerated | N/A |

---

## ⚙️ Configuration (.env)

Control storage behavior:

```bash
# Memory Bank
MEMORY_RETENTION_DAYS=90          # Keep user data for 90 days
MEMORY_COMPACTION_ENABLED=true    # Auto-cleanup old data

# Logs
LOG_ROTATION_DAYS=7                # Keep logs for 7 days
LOG_MAX_SIZE_MB=10                 # Max 10 MB per log file

# Cache
CACHE_ENABLED=true                 # Enable caching
CACHE_EXPIRY_DAYS=30               # Historical data cache: 30 days

# Backtest
BACKTEST_DEFAULT_PERIOD=1y         # Default: 1 year of data
```

---

## 📈 Expected Storage Usage

| Component | Initial | After 1 Month | After 6 Months |
|-----------|---------|---------------|----------------|
| Historical Data | 0 MB | 50 MB (10 tickers) | 200 MB (40 tickers) |
| Memory Bank | 1 MB | 10 MB | 50 MB |
| Logs | 0 MB | 50 MB | 50 MB (rotation) |
| Cache | 0 MB | 5 MB | 5 MB |
| **Total** | **1 MB** | **115 MB** | **305 MB** |

---

## 🧹 Cleanup Commands

```bash
# Clear old historical data (keep only recent)
Remove-Item data\historical\*.csv  # Delete all
# (Data will be re-downloaded when needed)

# Clear Memory Bank (reset user profiles)
Remove-Item -Recurse services\memory-bank\chroma_data\
# (Will recreate on next run)

# Clear logs
Remove-Item logs\*.log

# Clear cache
Remove-Item data\cache\*
```

---

## 💡 Best Practices

1. **Backup Memory Bank regularly** (your preferences):
   ```bash
   # Backup
   Compress-Archive services\memory-bank\chroma_data\ backup_$(Get-Date -Format yyyyMMdd).zip
   ```

2. **Pre-download common stocks** to speed up analysis:
   ```python
   # Run once to cache data
   from services.backtest_engine.data_loader import DataLoader
   dl = DataLoader()
   for ticker in ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]:
       dl.download_historical_data(ticker, "2019-01-01", "2024-12-01")
   ```

3. **Monitor storage**:
   - Check `data/historical/` size monthly
   - Review `memory-bank/` if over 100 MB
   - Logs auto-rotate (no action needed)

---

**Last Updated**: December 2024  
**Version**: 1.0.0

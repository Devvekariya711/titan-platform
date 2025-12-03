# Deployment Guide - Titan Platform

Complete guide for deploying and configuring the Titan Platform.

---

## Table of Contents

- [Environment Setup](#environment-setup)
- [API Key Configuration](#api-key-configuration)
- [Data Directory Structure](#data-directory-structure)
- [Running the System](#running-the-system)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)
- [Production Deployment](#production-deployment)

---

## Environment Setup

### System Requirements

**Minimum:**
- Python 3.10 or higher
- 4GB RAM
- 2GB disk space (for cached data)
- Internet connection (for market data)

**Recommended:**
- Python 3.11+
- 8GB RAM
- 10GB disk space
- Stable internet (5 Mbps+)

---

### Step 1: Python Environment

```bash
# Check Python version
python --version  # Should be 3.10+

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation
which python  # Should point to venv/bin/python
```

---

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify critical packages
pip list | grep -E "google-adk|chromadb|pandas|yfinance|pydantic"

# Expected output:
# google-adk            X.X.X
# chromadb             X.X.X
# pandas               X.X.X
# yfinance             X.X.X
# pydantic             X.X.X
```

**Common Installation Issues:**

**Issue:** `chromadb` fails to install
```bash
# Solution: Install build tools
# On Ubuntu/Debian:
sudo apt-get install python3-dev build-essential

# On Mac:
xcode-select --install

# Then retry:
pip install chromadb
```

**Issue:** `pandas_ta` not found
```bash
pip install pandas-ta
```

---

### Step 3: Verify Installation

```bash
# Test imports
python -c "
from google import genai
import chromadb
import pandas as pd
import yfinance as yf
print('✅ All core dependencies installed')
"
```

---

## API Key Configuration

### Required API Keys

1. **Google Gemini API Key** (Required)
   - Sign up: https://aistudio.google.com/app/apikey
   - Free tier: 60 requests per minute
   - Model: gemini-2.5-flash-lite (recommended for cost)

2. **Optional API Keys**
   - News APIs (future enhancement)
   - Twitter/Reddit APIs (future enhancement)

---

### Environment Variables Setup

**Step 1: Create `.env` file**

```bash
# Copy template
cp .env.template .env

# Edit .env
nano .env  # or use your preferred editor
```

**Step 2: Add your API key**

```bash
# .env file contents
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional settings
ENVIRONMENT=development
LOG_LEVEL=INFO
CACHE_ENABLED=true
```

**Step 3: Verify configuration**

```bash
# Test API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if api_key and len(api_key) > 20:
    print('✅ GOOGLE_API_KEY configured')
else:
    print('❌ GOOGLE_API_KEY missing or invalid')
"
```

---

### Security Best Practices

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Set proper file permissions (Linux/Mac)
chmod 600 .env

# Verify .env is not tracked
git status | grep .env  # Should show nothing

# Keep .env.template updated (without actual keys)
```

---

## Data Directory Structure

### Automatic Directory Creation

The system automatically creates necessary directories on first run:

```
titan-platform/
├── data/
│   ├── historical/         # Cached market data (CSV files)
│   │   ├── AAPL.csv       # Apple historical data
│   │   ├── MSFT.csv       # Microsoft historical data
│   │   └── ...
│   └── reports/           # Generated reports (future)
│
├── logs/
│   ├── titan-20241203.log # Daily logs with rotation
│   ├── titan-20241203.log.1  # Rotated logs
│   └── ...
│
├── services/
│   └── memory-bank/
│       └── chroma_data/   # ChromaDB vector storage
│           └── ...        # Persistent user data
│
└── agent_platform/
    └── dashboard.html     # Generated dashboard
```

---

### Manual Setup (if needed)

```bash
# Create directories
mkdir -p data/historical
mkdir -p data/reports
mkdir -p logs
mkdir -p services/memory-bank/chroma_data

# Set permissions (Linux/Mac)
chmod 755 data logs
chmod 700 services/memory-bank/chroma_data  # Private data

# Verify structure
tree -L 2 -d .  # Shows directory tree
```

---

### Data Preloading

**Pre-download commonly used tickers:**

```python
# preload_data.py
from services.backtest_engine.data_loader import DataLoader

dl = DataLoader()
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN", "META", "NFLX"]

for ticker in tickers:
    print(f"Downloading {ticker}...")
    dl.download_historical_data(ticker, "2019-01-01", "2024-12-01")
    
print("✅ Data preload complete")
```

```bash
# Run preload
python preload_data.py
```

---

## Running the System

### Option 1: Google ADK Web Interface (Recommended)

```bash
# Navigate to agent platform
cd agent_platform

# Start ADK web server
adk web

# Output:
# Starting server on http://localhost:8000
# Open in your browser
```

**Using the Web Interface:**

1. Open browser to `http://localhost:8000`
2. Select "MarketTrendPrincipal" agent
3. Enter query in chat interface
4. View agent responses and tool calls

**Example Queries:**
```
"What's the technical analysis for Apple?"
"Should I buy Tesla? (user_id: user123)"
"Backtest RSI strategy on MSFT for 3 years"
```

---

### Option 2: Dashboard

```bash
# Run metrics dashboard
python agent_platform/dashboard.py

# Output: Text report + HTML file
# HTML dashboard saved to: /path/to/dashboard.html
```

**View Dashboard:**
```bash
# Open in browser
open dashboard.html  # Mac
xdg-open dashboard.html  # Linux
start dashboard.html  # Windows
```

---

### Option 3: Python API (Advanced)

```python
# custom_query.py
from agent_platform.agents.root_agent import MarketTrendPrincipal
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

# Initialize
memory = ChromaDBWrapper()
agent = MarketTrendPrincipal()

# Setup user profile
memory.store_risk_profile("user123", "MEDIUM", 0.20, ["technology"])

# Query
query = "Should I invest in Apple?"
response = agent.query(query, user_id="user123")

print(response)
```

```bash
python custom_query.py
```

---

## Configuration Options

### config.yaml

Create `agent_platform/config.yaml`:

```yaml
# Titan Platform Configuration

settings:
  # User Defaults
  default_user_id: "default_user"
  default_risk_tolerance: "MEDIUM"
  
  # Data & Caching
  cache_enabled: true
  cache_directory: "data/historical"
  backtest_default_period: "1y"
  cache_expiry_days: 30
  
  # Logging
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_to_file: true
  log_to_console: true
  log_rotation_days: 7
  log_max_size_mb: 10
  
  # Performance
  max_agent_response_words: 250
  enable_parallel_execution: false
  tool_timeout_seconds: 30
  
  # Memory Bank
  memory_retention_days: 90
  memory_compaction_enabled: true
  
  # Data Sources
  market_data_provider: "yfinance"
  news_default_sources: 5
  social_sentiment_sources: ["reddit", "twitter"]
  
  # Model Configuration
  gemini_model: "gemini-2.5-flash-lite"
  temperature: 0.7
  max_tokens: 1000
  
  # Risk Management
  enable_risk_veto: true
  default_max_drawdown: 0.20  # 20%
  volatility_threshold_multiplier: 1.5
```

---

### Loading Configuration

```python
# In your code
import yaml

def load_config():
    with open('agent_platform/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config['settings']

# Use config
config = load_config()
log_level = config['log_level']
cache_enabled = config['cache_enabled']
```

---

### Environment-Specific Configs

```bash
# Development
cp config.yaml config.dev.yaml
# Edit: log_level: DEBUG, cache_enabled: true

# Production
cp config.yaml config.prod.yaml
# Edit: log_level: WARNING, cache_enabled: true

# Load based on environment
export TITAN_ENV=production
python -c "
import os
env = os.getenv('TITAN_ENV', 'development')
config_file = f'config.{env}.yaml'
print(f'Using config: {config_file}')
"
```

---

## Troubleshooting

### Issue 1: "GOOGLE_API_KEY not found"

**Diagnosis:**
```bash
# Check .env file exists
ls -la .env

# Check contents (without revealing key)
cat .env | grep GOOGLE_API_KEY | sed 's/=.*/=***/'
```

**Solutions:**
1. Ensure `.env` file exists in project root
2. Verify key is set correctly (no spaces around `=`)
3. Restart application to reload environment variables
4. If using IDE, ensure it loads `.env` (some IDEs require plugins)

---

### Issue 2: ChromaDB "Collection not found"

**Diagnosis:**
```bash
# Check ChromaDB directory
ls -la services/memory-bank/chroma_data/

# Check permissions
ls -ld services/memory-bank/chroma_data/
```

**Solutions:**
```python
# Reinitialize ChromaDB
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

memory = ChromaDBWrapper()
memory.client.reset()  # WARNING: Deletes all data
memory.__init__()  # Recreate collections
```

---

### Issue 3: "No historical data found"

**Diagnosis:**
```bash
# Check cache directory
ls -la data/historical/

# Check file sizes
du -h data/historical/*.csv | head
```

**Solutions:**
```python
# Re-download data
from services.backtest_engine.data_loader import DataLoader

dl = DataLoader()
dl.download_historical_data("AAPL", "2019-01-01", "2024-12-01", force=True)
```

---

### Issue 4: Slow Response Times (>10s)

**Diagnosis:**
```python
# Check performance metrics
from agent_platform.dashboard import TitanDashboard

dashboard = TitanDashboard()
metrics = dashboard.get_tool_metrics()

for tool, stats in metrics.items():
    if stats['avg_ms'] > 2000:
        print(f"⚠️ Slow: {tool} - {stats['avg_ms']:.0f}ms")
```

**Solutions:**
1. **Enable caching:**
   ```yaml
   # config.yaml
   cache_enabled: true
   ```

2. **Reduce data lookback:**
   ```python
   # Instead of 5 years:
   backtest_strategy("AAPL", "rsi_strategy", "1y")  # 1 year
   ```

3. **Check internet speed:**
   ```bash
   # Test yfinance connection
   curl -o /dev/null -s -w "%{time_total}\n" https://query1.finance.yahoo.com/v8/finance/chart/AAPL
   ```

4. **Limit parallel agent calls:**
   ```yaml
   enable_parallel_execution: false
   ```

---

### Issue 5: Memory Bank Not Persisting

**Diagnosis:**
```python
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

memory = ChromaDBWrapper()

# Test write
memory.store_risk_profile("test", "LOW", 0.15, [])

# Test read
context = memory.get_user_context("test")
print(context)
```

**Solutions:**
1. Ensure `chroma_data/` directory is writable
2. Check disk space: `df -h`
3. Verify no permissions issues: `ls -la services/memory-bank/chroma_data/`

---

### Issue 6: ADK Web Interface Won't Start

**Diagnosis:**
```bash
# Check if port 8000 is in use
netstat -an | grep 8000
# or
lsof -i :8000
```

**Solutions:**
1. **Kill existing process:**
   ```bash
   # Find PID
   lsof -ti:8000
   
   # Kill it
   kill -9 $(lsof -ti:8000)
   ```

2. **Use different port:**
   ```bash
   adk web --port 8080
   ```

3. **Check ADK installation:**
   ```bash
   pip show google-adk
   adk --version
   ```

---

## Performance Optimization

### 1. Enable Caching

```yaml
# config.yaml
cache_enabled: true
cache_expiry_days: 30  # Refresh after 30 days
```

**Impact:** 10x faster for repeated queries

---

### 2. Pre-download Data

```bash
# Download data for commonly queried stocks
python scripts/preload_data.py
```

**Impact:** Eliminates download time (saves 2-5s per backtest)

---

### 3. Optimize Agent Word Limits

```yaml
# config.yaml
max_agent_response_words: 200  # Default: 250

# Tighter limits = faster responses
```

**Impact:** 20-30% faster response times

---

### 4. Use Local Models (Future)

```yaml
# For on-premise deployment
model_provider: "local"  # Instead of "google"
local_model_path: "/path/to/model"
```

**Impact:** No API latency, unlimited requests

---

### 5. Database Compaction

```python
# Run weekly
from services.memory_bank.chromadb_wrapper import ChromaDBWrapper

memory = ChromaDBWrapper()
memory.compact_old_data(days_to_keep=90)
```

**Impact:** Faster memory retrieval

---

### 6. Parallel Tool Execution (Experimental)

```yaml
# config.yaml
enable_parallel_execution: true
```

⚠️ **Warning:** May increase API costs

---

## Production Deployment

### Containerization (Docker)

**Dockerfile** (create this):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data/historical logs services/memory-bank/chroma_data

# Expose port
EXPOSE 8000

# Run ADK
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & Run:**
```bash
# Build image
docker build -t titan-platform .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  titan-platform
```

---

### Environment Variables for Production

```bash
# .env.production
GOOGLE_API_KEY=your_production_key
ENVIRONMENT=production
LOG_LEVEL=WARNING
CACHE_ENABLED=true
ENABLE_DEBUG=false
```

---

### Monitoring in Production

**1. Health Check Endpoint**
```python
# Add to agent_platform/health.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})

if __name__ == '__main__':
    app.run(port=8001)
```

**2. Log Monitoring**
```bash
# Monitor errors in real-time
tail -f logs/titan-*.log | grep ERROR
```

**3. Performance Monitoring**
```bash
# Run dashboard periodically
crontab -e
# Add: 0 * * * * cd /path/to/titan-platform && python agent_platform/dashboard.py > /path/to/dashboard_report.txt
```

---

### Scaling Considerations

**Vertical Scaling:**
- 8GB RAM: ~100 concurrent queries
- 16GB RAM: ~500 concurrent queries

**Horizontal Scaling:**
- Deploy multiple ADK instances
- Use load balancer (nginx, HAProxy)
- Shared ChromaDB instance

---

## Backup & Recovery

### Backup ChromaDB

```bash
# Backup script
tar -czf memory_bank_backup_$(date +%Y%m%d).tar.gz \
  services/memory-bank/chroma_data/

# Store backups
mv memory_bank_backup_*.tar.gz /path/to/backups/
```

### Restore

```bash
# Stop ADK server
# Extract backup
tar -xzf memory_bank_backup_20241203.tar.gz -C services/memory-bank/

# Restart ADK
adk web
```

---

## Support & Resources

**Documentation:**
- [API Reference](API_REFERENCE.md)
- [Testing Guide](TESTING_GUIDE.md)
- [GitHub Repository](https://github.com/Devvekariya711/titan-platform)

**Community:**
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share experiences

**Version:** 1.0.0  
**Last Updated:** December 2024

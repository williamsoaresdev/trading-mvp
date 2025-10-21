# Complete Execution Guide - Trading MVP

## 🔧 Prerequisites

### Python
- **Recommended version**: Python 3.11
- **Minimum version**: Python 3.10
- **Avoid**: Python 3.12 (known instabilities)

### .NET
- **.NET 8 SDK** or higher

### Version Verification
```bash
python --version  # Should be 3.10+
dotnet --version  # Should be 8.0+
```

## 📦 1. Python Environment Configuration

### Step 1: Navigate to Python directory
```bash
cd trading-intelligence
```

### Step 2: Create virtual environment
```bash
# Linux/Mac
python -m venv .venv && source .venv/bin/activate

# Windows
python -m venv .venv && .venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Train the model (⏱️ ~10-15 minutes)
```bash
python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 2
```

**Expected output:**
- File `artifacts/model.pkl`
- File `artifacts/feature_config.json`
- Model accuracy reported

### Step 5: Start FastAPI service
```bash
uvicorn app.service:app --host 0.0.0.0 --port 8000
```

**Verification:**
- Access: http://localhost:8000/health
- Should return: `{"status":"ok", "model_loaded": true, ...}`

## 🎯 2. Execute the Robot (.NET)

### In a new terminal:

```bash
cd trading-executor
dotnet build
```

**Check for no compilation errors**

```bash
dotnet run
```

**Expected output:**
```
TradingExecutor started. Press Ctrl+C to stop.
2025-10-20T... | BTC/USDT 1h | BUY | pBuy=0.612 pSell=0.388 | price=67234.50 | pos=2.5%
[MOCK BUY] BTC/USDT qty=0.000371
```

## 🔍 3. Tests and Verification

### Test API manually:
```bash
curl "http://localhost:8000/predict?symbol=BTC/USDT&timeframe=1h"
```

### Check executor logs:
- Decisions being made every minute
- Mock orders being executed
- Prices and probabilities being reported

## ⚠️ 4. Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Check if virtual environment is active
which python  # Should point to .venv

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Error: "Connection refused" in .NET
```bash
# Check if FastAPI is running
curl http://localhost:8000/health

# Check port in use
netstat -an | grep 8000
```

### Error: "Model not found"
```bash
# Check if training was completed
ls -la artifacts/
# Should have: model.pkl and feature_config.json
```

## 🚀 5. Next Steps

### For extended Paper Trading:
1. Run for 2-4 weeks
2. Monitor performance via logs
3. Analyze simulated P&L metrics

### For Production (when ready):
1. Implement `BinanceSpotOrderExecutor`
2. Configure Binance API keys
3. Start with small capital (< $100)
4. Monitor 24/7 for the first few days

## 📊 6. Monitoring

### Important metrics:
- **Directional accuracy**: >55% considered good
- **Win rate**: ratio of profitable trades
- **Max drawdown**: maximum consecutive loss
- **Sharpe ratio**: risk-adjusted return

### Logs to observe:
- Trade frequency
- BUY/SELL/FLAT distribution
- Probability values
- Position sizes

---

**⚠️ IMPORTANT**: This MVP is in PAPER TRADING mode. No real orders will be executed until you implement and activate the `BinanceSpotOrderExecutor`.
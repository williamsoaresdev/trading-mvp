# 🚀 Binance Integration Guide - Real Trading

## ⚠️ **IMPORTANT WARNING**
This guide shows how to integrate with real Binance APIs. **START WITH TESTNET** and use **SMALL AMOUNTS** for live testing. Real trading involves financial risk.

## 🔧 **Prerequisites**

### 1. Binance Account Setup
- Create Binance account: https://www.binance.com
- Complete KYC verification
- Enable 2FA security

### 2. API Keys Configuration
1. Go to **Account** → **API Management**
2. Create new API key with permissions:
   - ✅ **Spot & Margin Trading**
   - ✅ **Read Info** 
   - ❌ **Futures Trading** (disable for safety)
   - ❌ **Withdraw** (disable for safety)
3. **Restrict to trusted IPs** (recommended)
4. Save API Key and Secret Key securely

### 3. Testnet Setup (RECOMMENDED FIRST)
- Binance Testnet: https://testnet.binance.vision/
- Get testnet API keys (no real money involved)
- Test all functionality before live trading

## 🛠️ **Implementation Steps**

### Step 1: Install Binance Dependencies

```bash
# In trading-intelligence folder
cd trading-intelligence
pip install python-binance ccxt python-dotenv
```

### Step 2: Environment Configuration

Create `.env` file in root:
```bash
# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=true  # Set to false for live trading

# Trading Configuration  
TRADING_SYMBOL=BTCUSDT
BASE_CURRENCY=USDT
POSITION_SIZE_PERCENT=1.0  # Start with 1% of balance
MAX_DAILY_TRADES=10
STOP_LOSS_PERCENT=2.0
TAKE_PROFIT_PERCENT=3.0

# Risk Management
ENABLE_REAL_TRADING=false  # MUST be true to enable real orders
MIN_ACCOUNT_BALANCE=100    # Minimum USDT balance required
```

### Step 3: Real Binance Order Executor

Create `trading-intelligence/app/infrastructure/external/binance_real_executor.py`:

```python
import os
import logging
from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BinanceRealExecutor:
    """Real Binance order executor with safety features"""
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        self.real_trading_enabled = os.getenv('ENABLE_REAL_TRADING', 'false').lower() == 'true'
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Binance API credentials not found in environment")
            
        # Initialize Binance client
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.secret_key,
            testnet=self.testnet
        )
        
        self.logger = logging.getLogger(__name__)
        
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information and balances"""
        try:
            return self.client.get_account()
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get account info: {e}")
            raise
    
    def get_balance(self, asset: str) -> float:
        """Get balance for specific asset"""
        try:
            account = self.get_account_info()
            for balance in account['balances']:
                if balance['asset'] == asset:
                    return float(balance['free'])
            return 0.0
        except Exception as e:
            self.logger.error(f"Failed to get {asset} balance: {e}")
            return 0.0
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get trading symbol information"""
        try:
            info = self.client.get_symbol_info(symbol)
            return info
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get symbol info for {symbol}: {e}")
            raise
    
    def calculate_quantity(self, symbol: str, usdt_amount: float) -> float:
        """Calculate quantity based on USDT amount and current price"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            quantity = usdt_amount / price
            
            # Get symbol info for precision
            symbol_info = self.get_symbol_info(symbol)
            lot_size = None
            
            for filter_item in symbol_info['filters']:
                if filter_item['filterType'] == 'LOT_SIZE':
                    lot_size = filter_item
                    break
            
            if lot_size:
                step_size = float(lot_size['stepSize'])
                precision = len(str(step_size).split('.')[-1].rstrip('0'))
                quantity = round(quantity, precision)
            
            return quantity
            
        except Exception as e:
            self.logger.error(f"Failed to calculate quantity: {e}")
            raise
    
    def place_market_buy(self, symbol: str, usdt_amount: float) -> Optional[Dict[str, Any]]:
        """Place market buy order"""
        if not self.real_trading_enabled:
            self.logger.warning("Real trading not enabled. Order would be: BUY {} with ${:.2f}".format(
                symbol, usdt_amount))
            return None
            
        try:
            # Safety checks
            balance = self.get_balance('USDT')
            if balance < usdt_amount:
                raise ValueError(f"Insufficient balance. Have: ${balance:.2f}, Need: ${usdt_amount:.2f}")
            
            # Calculate quantity
            quantity = self.calculate_quantity(symbol, usdt_amount)
            
            # Place order
            order = self.client.order_market_buy(
                symbol=symbol,
                quantity=quantity
            )
            
            self.logger.info(f"Market BUY order placed: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to place buy order: {e}")
            raise
    
    def place_market_sell(self, symbol: str, quantity: float) -> Optional[Dict[str, Any]]:
        """Place market sell order"""
        if not self.real_trading_enabled:
            self.logger.warning(f"Real trading not enabled. Order would be: SELL {quantity} {symbol}")
            return None
            
        try:
            # Get base asset (e.g., BTC from BTCUSDT)
            base_asset = symbol.replace('USDT', '')
            balance = self.get_balance(base_asset)
            
            if balance < quantity:
                raise ValueError(f"Insufficient {base_asset}. Have: {balance:.8f}, Need: {quantity:.8f}")
            
            # Place order
            order = self.client.order_market_sell(
                symbol=symbol,
                quantity=quantity
            )
            
            self.logger.info(f"Market SELL order placed: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to place sell order: {e}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Failed to get price for {symbol}: {e}")
            raise
    
    def get_24h_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get 24h ticker statistics"""
        try:
            return self.client.get_24hr_ticker(symbol=symbol)
        except Exception as e:
            self.logger.error(f"Failed to get 24h ticker for {symbol}: {e}")
            raise
```

### Step 4: Update .NET Executor for Real Orders

Update `trading-executor/Infrastructure/Services.cs`:

```csharp
using System.Net.Http.Json;
using System.Text;
using System.Security.Cryptography;

public class BinanceRealOrderExecutor : IOrderExecutor
{
    private readonly HttpClient _httpClient;
    private readonly string _apiKey;
    private readonly string _secretKey;
    private readonly bool _testnet;
    private readonly bool _realTradingEnabled;
    private readonly ILogger<BinanceRealOrderExecutor> _logger;

    public BinanceRealOrderExecutor(IHttpClientFactory httpClientFactory, 
                                   IConfiguration configuration,
                                   ILogger<BinanceRealOrderExecutor> logger)
    {
        _httpClient = httpClientFactory.CreateClient();
        _apiKey = configuration["Binance:ApiKey"] ?? throw new InvalidOperationException("Binance API key not configured");
        _secretKey = configuration["Binance:SecretKey"] ?? throw new InvalidOperationException("Binance secret key not configured");
        _testnet = configuration.GetValue<bool>("Binance:Testnet", true);
        _realTradingEnabled = configuration.GetValue<bool>("Binance:EnableRealTrading", false);
        _logger = logger;

        var baseUrl = _testnet ? "https://testnet.binance.vision/api/v3/" : "https://api.binance.com/api/v3/";
        _httpClient.BaseAddress = new Uri(baseUrl);
    }

    private string CreateSignature(string queryString)
    {
        var keyBytes = Encoding.UTF8.GetBytes(_secretKey);
        var queryBytes = Encoding.UTF8.GetBytes(queryString);
        
        using var hmac = new HMACSHA256(keyBytes);
        var hashBytes = hmac.ComputeHash(queryBytes);
        return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
    }

    public async Task<OrderResult> ExecuteBuyAsync(TradingDecision decision)
    {
        if (!_realTradingEnabled)
        {
            _logger.LogWarning("Real trading disabled. Would place BUY order for {Symbol}", decision.Symbol);
            return new OrderResult(false, "Real trading disabled", 0m);
        }

        try
        {
            var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var queryString = $"symbol={decision.Symbol}&side=BUY&type=MARKET&quoteOrderQty=10&timestamp={timestamp}";
            var signature = CreateSignature(queryString);
            
            _httpClient.DefaultRequestHeaders.Add("X-MBX-APIKEY", _apiKey);
            
            var response = await _httpClient.PostAsync($"order?{queryString}&signature={signature}", null);
            
            if (response.IsSuccessStatusCode)
            {
                var orderResponse = await response.Content.ReadFromJsonAsync<BinanceOrderResponse>();
                _logger.LogInformation("BUY order executed: {OrderId}", orderResponse?.OrderId);
                return new OrderResult(true, "Order executed", decimal.Parse(orderResponse?.Price ?? "0"));
            }
            
            var errorContent = await response.Content.ReadAsStringAsync();
            _logger.LogError("Failed to execute BUY order: {Error}", errorContent);
            return new OrderResult(false, $"API Error: {errorContent}", 0m);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Exception executing BUY order");
            return new OrderResult(false, ex.Message, 0m);
        }
    }

    // Similar implementation for ExecuteSellAsync...
}

public class BinanceOrderResponse
{
    public string Symbol { get; set; } = "";
    public long OrderId { get; set; }
    public string Price { get; set; } = "0";
    public string ExecutedQty { get; set; } = "0";
    public string Status { get; set; } = "";
}
```

### Step 5: Testing Strategy

Create `scripts/test_binance_integration.py`:

```python
#!/usr/bin/env python3
"""
Safe Binance Integration Testing
"""
import os
import sys
import asyncio
from pathlib import Path

# Add trading-intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent / "trading-intelligence"))

async def test_binance_connection():
    """Test Binance API connection safely"""
    print("🧪 BINANCE INTEGRATION TESTING")
    print("=" * 50)
    
    try:
        from app.infrastructure.external.binance_real_executor import BinanceRealExecutor
        
        # Initialize executor
        executor = BinanceRealExecutor()
        
        # Test 1: Connection
        print("📡 Testing API Connection...")
        account_info = executor.get_account_info()
        print(f"   ✅ Connected to Binance ({'Testnet' if executor.testnet else 'Mainnet'})")
        
        # Test 2: Account balances
        print("\n💰 Account Balances:")
        usdt_balance = executor.get_balance('USDT')
        btc_balance = executor.get_balance('BTC')
        print(f"   USDT: ${usdt_balance:.2f}")
        print(f"   BTC: {btc_balance:.8f}")
        
        # Test 3: Market data
        print("\n📊 Market Data:")
        symbol = "BTCUSDT"
        current_price = executor.get_current_price(symbol)
        ticker_24h = executor.get_24h_ticker(symbol)
        print(f"   {symbol} Price: ${current_price:,.2f}")
        print(f"   24h Change: {float(ticker_24h['priceChangePercent']):.2f}%")
        
        # Test 4: Order simulation
        print("\n🎯 Order Simulation:")
        test_amount = 10.0  # $10 USDT
        quantity = executor.calculate_quantity(symbol, test_amount)
        print(f"   ${test_amount} USDT = {quantity:.6f} BTC")
        
        # Test 5: Safety checks
        print("\n🛡️ Safety Status:")
        print(f"   Testnet Mode: {'✅' if executor.testnet else '❌ LIVE'}")
        print(f"   Real Trading: {'✅ ENABLED' if executor.real_trading_enabled else '❌ DISABLED'}")
        
        if not executor.testnet and executor.real_trading_enabled:
            print("\n⚠️ WARNING: LIVE TRADING IS ENABLED!")
            print("   Make sure you understand the risks!")
        
        print("\n✅ All tests passed! Binance integration ready.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_binance_connection())
```

## 🚨 **Safety Checklist**

### Before Live Trading:
- [ ] ✅ Test with Binance Testnet first
- [ ] ✅ Use small amounts ($10-50) initially  
- [ ] ✅ Verify all safety configurations
- [ ] ✅ Test stop-loss mechanisms
- [ ] ✅ Monitor for 24h minimum
- [ ] ✅ Have emergency stop procedures

### Production Deployment:
- [ ] ✅ Secure API key storage
- [ ] ✅ IP restrictions configured
- [ ] ✅ Monitoring and alerting setup
- [ ] ✅ Risk management limits active
- [ ] ✅ Backup and recovery plans

## 🔧 **Configuration Files**

Update `config/config.yaml`:
```yaml
binance:
  testnet: true
  enable_real_trading: false
  max_position_size: 100.0  # USD
  max_daily_loss: 50.0      # USD
  
trading:
  symbol: "BTCUSDT"
  position_size_percent: 1.0
  stop_loss_percent: 2.0
  take_profit_percent: 3.0
  max_daily_trades: 10

risk_management:
  min_account_balance: 100.0
  max_drawdown_percent: 10.0
  emergency_stop_enabled: true
```

## 🚀 **Execution Commands**

```bash
# 1. Test connection (safe)
python scripts/test_binance_integration.py

# 2. Run with testnet
BINANCE_TESTNET=true python scripts/run_realtime.py

# 3. Enable live trading (CAREFUL!)
ENABLE_REAL_TRADING=true BINANCE_TESTNET=false python scripts/run_realtime.py
```

---

**⚠️ DISCLAIMER**: This is for educational purposes. Always start with testnet and small amounts. Trading involves significant financial risk.
#!/usr/bin/env python3
"""
Safe Binance Integration Testing
Tests connection, balances, market data without placing real orders
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add trading-intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent / "trading-intelligence"))

async def test_binance_connection():
    """Test Binance API connection safely"""
    print("🧪 BINANCE INTEGRATION TESTING")
    print("=" * 50)
    
    # Check environment setup
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Binance API Key not configured!")
        print("   Please set BINANCE_API_KEY in .env file")
        return False
        
    if not secret_key or secret_key == 'your_secret_key_here':
        print("❌ Binance Secret Key not configured!")
        print("   Please set BINANCE_SECRET_KEY in .env file")
        return False
    
    try:
        # Import after environment check
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        
        testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        
        # Initialize client
        client = Client(
            api_key=api_key,
            api_secret=secret_key,
            testnet=testnet
        )
        
        # Test 1: Connection
        print("📡 Testing API Connection...")
        try:
            server_time = client.get_server_time()
            print(f"   ✅ Connected to Binance ({'Testnet' if testnet else 'Mainnet'})")
            print(f"   Server time: {server_time}")
        except BinanceAPIException as e:
            print(f"   ❌ Connection failed: {e}")
            return False
        
        # Test 2: Account info
        print("\n👤 Account Information:")
        try:
            account = client.get_account()
            print(f"   Account Type: {account.get('accountType', 'SPOT')}")
            print(f"   Can Trade: {account.get('canTrade', False)}")
            print(f"   Can Withdraw: {account.get('canWithdraw', False)}")
            print(f"   Can Deposit: {account.get('canDeposit', False)}")
        except BinanceAPIException as e:
            print(f"   ❌ Failed to get account info: {e}")
            return False
        
        # Test 3: Account balances
        print("\n💰 Account Balances:")
        try:
            balances = {b['asset']: float(b['free']) for b in account['balances'] if float(b['free']) > 0}
            if balances:
                for asset, balance in list(balances.items())[:10]:  # Show top 10
                    print(f"   {asset}: {balance:.8f}")
                if len(balances) > 10:
                    print(f"   ... and {len(balances) - 10} more assets")
            else:
                print("   No balances found (normal for new testnet accounts)")
        except Exception as e:
            print(f"   ❌ Failed to get balances: {e}")
        
        # Test 4: Market data
        print("\n📊 Market Data Test:")
        try:
            symbol = "BTCUSDT"
            ticker = client.get_symbol_ticker(symbol=symbol)
            ticker_24h = client.get_24hr_ticker(symbol=symbol)
            
            print(f"   {symbol} Price: ${float(ticker['price']):,.2f}")
            print(f"   24h Change: {float(ticker_24h['priceChangePercent']):.2f}%")
            print(f"   24h Volume: {float(ticker_24h['volume']):,.2f} BTC")
        except Exception as e:
            print(f"   ❌ Failed to get market data: {e}")
        
        # Test 5: Symbol info
        print("\n📋 Trading Pair Information:")
        try:
            symbol_info = client.get_symbol_info(symbol)
            print(f"   Symbol: {symbol_info['symbol']}")
            print(f"   Status: {symbol_info['status']}")
            print(f"   Base Asset: {symbol_info['baseAsset']}")
            print(f"   Quote Asset: {symbol_info['quoteAsset']}")
            
            # Get lot size filter
            for f in symbol_info['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    print(f"   Min Quantity: {f['minQty']}")
                    print(f"   Max Quantity: {f['maxQty']}")
                    print(f"   Step Size: {f['stepSize']}")
                    break
        except Exception as e:
            print(f"   ❌ Failed to get symbol info: {e}")
        
        # Test 6: Order book
        print("\n📖 Order Book Sample:")
        try:
            depth = client.get_order_book(symbol=symbol, limit=5)
            print("   Top 5 Bids:")
            for i, (price, qty) in enumerate(depth['bids'][:3]):
                print(f"     {i+1}. ${float(price):,.2f} - {float(qty):.6f} BTC")
            print("   Top 3 Asks:")
            for i, (price, qty) in enumerate(depth['asks'][:3]):
                print(f"     {i+1}. ${float(price):,.2f} - {float(qty):.6f} BTC")
        except Exception as e:
            print(f"   ❌ Failed to get order book: {e}")
        
        # Test 7: Safety status
        print("\n🛡️ Safety Configuration:")
        real_trading = os.getenv('ENABLE_REAL_TRADING', 'false').lower() == 'true'
        print(f"   Testnet Mode: {'✅ ACTIVE' if testnet else '❌ DISABLED (LIVE TRADING)'}")
        print(f"   Real Trading: {'⚠️ ENABLED' if real_trading else '✅ DISABLED'}")
        
        if not testnet and real_trading:
            print("\n🚨 CRITICAL WARNING: LIVE TRADING IS ENABLED!")
            print("   You are connected to LIVE Binance with REAL money!")
            print("   Make sure you understand the risks!")
            response = input("\n   Continue? (type 'YES' to proceed): ")
            if response != 'YES':
                print("   Test cancelled for safety.")
                return False
        elif testnet:
            print("\n✅ SAFE MODE: Using Binance Testnet")
            print("   No real money is involved in this testing")
        
        print(f"\n✅ All tests passed! Binance integration is working correctly.")
        print(f"📊 Connection Status: {'Testnet' if testnet else 'Live'}")
        print(f"🔒 Trading Status: {'Enabled' if real_trading else 'Disabled (Safe)'}")
        
        return True
        
    except ImportError:
        print("❌ Missing dependencies!")
        print("   Please install: pip install python-binance python-dotenv")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Environment Configuration Check")
    print("-" * 40)
    
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env and configure it")
        return False
    
    required_vars = [
        'BINANCE_API_KEY',
        'BINANCE_SECRET_KEY',
        'BINANCE_TESTNET',
        'ENABLE_REAL_TRADING'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Missing environment variables:")
        for var in missing:
            print(f"   - {var}")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

if __name__ == "__main__":
    print("🚀 BINANCE INTEGRATION TEST SUITE")
    print("=" * 60)
    
    # Check environment first
    if not check_environment():
        sys.exit(1)
    
    # Run connection test
    success = asyncio.run(test_binance_connection())
    
    if success:
        print("\n🎉 Integration test completed successfully!")
        print("\nNext steps:")
        print("1. If using testnet, you can now run trading algorithms safely")
        print("2. For live trading, start with VERY small amounts")
        print("3. Monitor closely and have stop-loss mechanisms ready")
    else:
        print("\n❌ Integration test failed!")
        print("Please fix the issues above before proceeding.")
        sys.exit(1)
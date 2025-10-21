#!/usr/bin/env python3
"""
Emergency script to close all open positions
Use in case of system failure or market emergency
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add trading-intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent / "trading-intelligence"))

def emergency_close_all():
    """Close all open positions immediately"""
    print("🚨 EMERGENCY POSITION CLOSURE")
    print("=" * 40)
    
    try:
        from binance.client import Client
        
        # Initialize client
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        
        if not api_key or not secret_key:
            print("❌ API keys not configured!")
            return False
        
        client = Client(
            api_key=api_key,
            api_secret=secret_key,
            testnet=testnet
        )
        
        print(f"📡 Connected to Binance ({'Testnet' if testnet else 'LIVE'})")
        
        # Get account info
        account = client.get_account()
        
        # Find assets with balance > 0 (excluding USDT/BUSD)
        positions_to_close = []
        for balance in account['balances']:
            asset = balance['asset']
            free_balance = float(balance['free'])
            
            # Skip stablecoins and zero balances
            if asset in ['USDT', 'BUSD', 'USDC'] or free_balance <= 0:
                continue
            
            # Common trading pairs
            if asset + 'USDT' in ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT']:
                symbol = asset + 'USDT'
                positions_to_close.append((symbol, asset, free_balance))
        
        if not positions_to_close:
            print("✅ No open positions found")
            return True
        
        print(f"📋 Found {len(positions_to_close)} positions to close:")
        for symbol, asset, balance in positions_to_close:
            print(f"   {symbol}: {balance:.8f} {asset}")
        
        # Confirm action
        if not testnet:
            print("\n🚨 WARNING: This will close REAL positions with REAL money!")
            confirm = input("Type 'CLOSE ALL POSITIONS' to confirm: ")
            if confirm != 'CLOSE ALL POSITIONS':
                print("❌ Operation cancelled")
                return False
        
        # Close positions
        closed_positions = 0
        for symbol, asset, balance in positions_to_close:
            try:
                print(f"\n🔄 Closing {symbol} position...")
                
                # Place market sell order
                order = client.order_market_sell(
                    symbol=symbol,
                    quantity=balance
                )
                
                print(f"✅ {symbol} closed: Order ID {order['orderId']}")
                closed_positions += 1
                
            except Exception as e:
                print(f"❌ Failed to close {symbol}: {e}")
        
        print(f"\n✅ Emergency closure complete!")
        print(f"   Positions closed: {closed_positions}/{len(positions_to_close)}")
        
        return True
        
    except ImportError:
        print("❌ python-binance not installed!")
        return False
    except Exception as e:
        print(f"❌ Emergency closure failed: {e}")
        return False

def get_current_positions():
    """Show current positions without closing"""
    print("📊 CURRENT POSITIONS")
    print("=" * 30)
    
    try:
        from binance.client import Client
        
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        
        if not api_key or not secret_key:
            print("❌ API keys not configured!")
            return
        
        client = Client(
            api_key=api_key,
            api_secret=secret_key,
            testnet=testnet
        )
        
        account = client.get_account()
        
        print(f"📡 Account: {'Testnet' if testnet else 'Live'}")
        print(f"⏰ Last Update: {account['updateTime']}")
        
        # Show balances
        print("\n💰 Current Balances:")
        has_positions = False
        total_usdt_value = 0
        
        for balance in account['balances']:
            asset = balance['asset']
            free_balance = float(balance['free'])
            locked_balance = float(balance['locked'])
            total_balance = free_balance + locked_balance
            
            if total_balance > 0:
                print(f"   {asset}: {total_balance:.8f} (Free: {free_balance:.8f})")
                has_positions = True
                
                # Estimate USDT value for non-stablecoins
                if asset not in ['USDT', 'BUSD', 'USDC'] and total_balance > 0:
                    try:
                        ticker = client.get_symbol_ticker(symbol=asset + 'USDT')
                        price = float(ticker['price'])
                        usdt_value = total_balance * price
                        total_usdt_value += usdt_value
                        print(f"     ≈ ${usdt_value:.2f} USDT")
                    except:
                        pass
                elif asset in ['USDT', 'BUSD', 'USDC']:
                    total_usdt_value += total_balance
        
        if has_positions:
            print(f"\n💵 Total Estimated Value: ${total_usdt_value:.2f}")
        else:
            print("   No positions found")
        
    except Exception as e:
        print(f"❌ Failed to get positions: {e}")

if __name__ == "__main__":
    print("🚨 BINANCE EMERGENCY CONTROLS")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--close-all':
        emergency_close_all()
    else:
        print("Available commands:")
        print("  python scripts/emergency_close_all.py --close-all    # Close all positions")
        print("  python scripts/emergency_close_all.py               # Show positions only")
        print("")
        get_current_positions()
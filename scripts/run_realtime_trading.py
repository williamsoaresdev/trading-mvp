#!/usr/bin/env python3
"""
Real-time trading execution with Binance integration
Supports both testnet and live trading modes
"""
import os
import sys
import asyncio
import json
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add trading-intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent / "trading-intelligence"))

class SafeBinanceExecutor:
    """Safe Binance executor with comprehensive risk management"""
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        self.real_trading = os.getenv('ENABLE_REAL_TRADING', 'false').lower() == 'true'
        
        # Risk management settings
        self.position_size_percent = float(os.getenv('POSITION_SIZE_PERCENT', '1.0'))
        self.max_daily_trades = int(os.getenv('MAX_DAILY_TRADES', '10'))
        self.stop_loss_percent = float(os.getenv('STOP_LOSS_PERCENT', '2.0'))
        self.take_profit_percent = float(os.getenv('TAKE_PROFIT_PERCENT', '3.0'))
        self.min_balance = float(os.getenv('MIN_ACCOUNT_BALANCE', '100'))
        
        # Trading state
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.positions = {}
        self.running = False
        
        print(f"🔧 Initialized SafeBinanceExecutor")
        print(f"   Mode: {'Testnet' if self.testnet else 'LIVE'}")
        print(f"   Real Trading: {'✅' if self.real_trading else '❌'}")
        
    def initialize_binance(self):
        """Initialize Binance client with error handling"""
        try:
            from binance.client import Client
            from binance.exceptions import BinanceAPIException
            
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.secret_key,
                testnet=self.testnet
            )
            
            # Test connection
            server_time = self.client.get_server_time()
            print(f"✅ Connected to Binance at {datetime.fromtimestamp(server_time['serverTime']/1000)}")
            return True
            
        except ImportError:
            print("❌ python-binance not installed!")
            print("   Run: pip install python-binance")
            return False
        except Exception as e:
            print(f"❌ Failed to connect to Binance: {e}")
            return False
    
    def get_account_balance(self, asset: str) -> float:
        """Get account balance for asset"""
        try:
            account = self.client.get_account()
            for balance in account['balances']:
                if balance['asset'] == asset:
                    return float(balance['free'])
            return 0.0
        except Exception as e:
            print(f"❌ Failed to get {asset} balance: {e}")
            return 0.0
    
    def check_safety_conditions(self) -> bool:
        """Check all safety conditions before trading"""
        # Check daily trade limit
        if self.daily_trades >= self.max_daily_trades:
            print(f"🛑 Daily trade limit reached ({self.daily_trades}/{self.max_daily_trades})")
            return False
        
        # Check minimum balance
        usdt_balance = self.get_account_balance('USDT')
        if usdt_balance < self.min_balance:
            print(f"🛑 Balance too low: ${usdt_balance:.2f} < ${self.min_balance}")
            return False
        
        # Check if in testnet or real trading is explicitly enabled
        if not self.testnet and not self.real_trading:
            print("🛑 Live trading not explicitly enabled!")
            return False
        
        return True
    
    def calculate_position_size(self, symbol: str) -> float:
        """Calculate safe position size"""
        usdt_balance = self.get_account_balance('USDT')
        position_usdt = usdt_balance * (self.position_size_percent / 100.0)
        
        # Cap at reasonable maximum
        max_position = 100.0 if self.testnet else 50.0
        position_usdt = min(position_usdt, max_position)
        
        print(f"💰 Position size: ${position_usdt:.2f} ({self.position_size_percent}% of ${usdt_balance:.2f})")
        return position_usdt
    
    def execute_buy_order(self, symbol: str, reason: str) -> bool:
        """Execute buy order with safety checks"""
        if not self.check_safety_conditions():
            return False
        
        try:
            position_usdt = self.calculate_position_size(symbol)
            
            if self.real_trading:
                # Get current price and calculate quantity
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                quantity = position_usdt / price
                
                # Round quantity to valid precision
                symbol_info = self.client.get_symbol_info(symbol)
                for filter_item in symbol_info['filters']:
                    if filter_item['filterType'] == 'LOT_SIZE':
                        step_size = float(filter_item['stepSize'])
                        precision = len(str(step_size).split('.')[-1].rstrip('0'))
                        quantity = round(quantity, precision)
                        break
                
                # Place market buy order
                order = self.client.order_market_buy(
                    symbol=symbol,
                    quantity=quantity
                )
                
                print(f"✅ BUY order executed:")
                print(f"   Symbol: {symbol}")
                print(f"   Quantity: {quantity:.8f}")
                print(f"   Order ID: {order['orderId']}")
                print(f"   Reason: {reason}")
                
                # Track position
                self.positions[symbol] = {
                    'quantity': quantity,
                    'entry_price': price,
                    'entry_time': datetime.now(),
                    'order_id': order['orderId']
                }
                
            else:
                print(f"📝 SIMULATED BUY order:")
                print(f"   Symbol: {symbol}")
                print(f"   Amount: ${position_usdt:.2f}")
                print(f"   Reason: {reason}")
            
            self.daily_trades += 1
            return True
            
        except Exception as e:
            print(f"❌ Failed to execute BUY order: {e}")
            return False
    
    def execute_sell_order(self, symbol: str, reason: str) -> bool:
        """Execute sell order"""
        if symbol not in self.positions:
            print(f"❌ No position found for {symbol}")
            return False
        
        try:
            position = self.positions[symbol]
            quantity = position['quantity']
            
            if self.real_trading:
                order = self.client.order_market_sell(
                    symbol=symbol,
                    quantity=quantity
                )
                
                # Calculate P&L
                current_price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                pnl = (current_price - position['entry_price']) * quantity
                self.daily_pnl += pnl
                
                print(f"✅ SELL order executed:")
                print(f"   Symbol: {symbol}")
                print(f"   Quantity: {quantity:.8f}")
                print(f"   P&L: ${pnl:.2f}")
                print(f"   Order ID: {order['orderId']}")
                print(f"   Reason: {reason}")
                
            else:
                print(f"📝 SIMULATED SELL order:")
                print(f"   Symbol: {symbol}")
                print(f"   Quantity: {quantity:.8f}")
                print(f"   Reason: {reason}")
            
            # Remove position
            del self.positions[symbol]
            self.daily_trades += 1
            return True
            
        except Exception as e:
            print(f"❌ Failed to execute SELL order: {e}")
            return False
    
    def check_stop_loss_take_profit(self):
        """Check stop loss and take profit for all positions"""
        for symbol, position in list(self.positions.items()):
            try:
                current_price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                entry_price = position['entry_price']
                
                # Calculate percentage change
                pct_change = ((current_price - entry_price) / entry_price) * 100
                
                # Check stop loss
                if pct_change <= -self.stop_loss_percent:
                    print(f"🛑 Stop loss triggered for {symbol}: {pct_change:.2f}%")
                    self.execute_sell_order(symbol, f"Stop loss at {pct_change:.2f}%")
                    continue
                
                # Check take profit
                if pct_change >= self.take_profit_percent:
                    print(f"🎯 Take profit triggered for {symbol}: {pct_change:.2f}%")
                    self.execute_sell_order(symbol, f"Take profit at {pct_change:.2f}%")
                    continue
                
                # Show current P&L
                if abs(pct_change) > 0.5:  # Only show if significant change
                    print(f"📊 {symbol}: {pct_change:+.2f}% (${current_price:,.2f})")
                
            except Exception as e:
                print(f"❌ Error checking {symbol}: {e}")
    
    async def run_trading_loop(self):
        """Main trading loop"""
        print(f"\n🚀 Starting trading loop...")
        print(f"   Symbol: {os.getenv('TRADING_SYMBOL', 'BTCUSDT')}")
        print(f"   Max daily trades: {self.max_daily_trades}")
        print(f"   Position size: {self.position_size_percent}%")
        print(f"   Stop loss: {self.stop_loss_percent}%")
        print(f"   Take profit: {self.take_profit_percent}%")
        
        self.running = True
        symbol = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
        
        try:
            while self.running:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Check existing positions
                if self.positions:
                    self.check_stop_loss_take_profit()
                
                # Simple trading logic (replace with your ML model)
                current_price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                
                # Get 24h ticker for simple trend analysis
                ticker_24h = self.client.get_24hr_ticker(symbol=symbol)
                price_change_pct = float(ticker_24h['priceChangePercent'])
                
                print(f"📊 {symbol}: ${current_price:,.2f} ({price_change_pct:+.2f}%)")
                print(f"💼 Positions: {len(self.positions)} | Daily trades: {self.daily_trades}/{self.max_daily_trades}")
                print(f"💰 Daily P&L: ${self.daily_pnl:.2f}")
                
                # Example trading logic - replace with your algorithm
                if symbol not in self.positions and self.daily_trades < self.max_daily_trades:
                    if price_change_pct > 2.0:  # Simple momentum strategy
                        self.execute_buy_order(symbol, f"Momentum buy at +{price_change_pct:.2f}%")
                
                # Wait before next iteration
                await asyncio.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n⏹️ Trading loop interrupted by user")
        except Exception as e:
            print(f"\n❌ Trading loop error: {e}")
        finally:
            self.running = False
    
    def shutdown(self):
        """Graceful shutdown"""
        print("\n🔄 Shutting down trading system...")
        self.running = False
        
        # Close all positions if any
        if self.positions:
            print(f"🔒 Closing {len(self.positions)} open positions...")
            for symbol in list(self.positions.keys()):
                self.execute_sell_order(symbol, "System shutdown")
        
        print("✅ Shutdown complete")

async def main():
    """Main execution function"""
    print("🏦 BINANCE REAL-TIME TRADING SYSTEM")
    print("=" * 50)
    
    # Initialize executor
    executor = SafeBinanceExecutor()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Received signal {signum}")
        executor.shutdown()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize Binance connection
    if not executor.initialize_binance():
        print("❌ Failed to initialize Binance connection")
        return
    
    # Safety confirmation for live trading
    if not executor.testnet and executor.real_trading:
        print("\n🚨 LIVE TRADING MODE DETECTED!")
        print("   This will use REAL money on Binance mainnet!")
        print("   Make sure you understand the risks involved!")
        
        response = input("\n   Type 'START LIVE TRADING' to continue: ")
        if response != 'START LIVE TRADING':
            print("❌ Live trading cancelled for safety")
            return
    
    # Run trading loop
    await executor.run_trading_loop()

if __name__ == "__main__":
    asyncio.run(main())
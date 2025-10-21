"""
Binance Real Order Executor
Production-ready implementation for real trading
"""
import os
import logging
from decimal import Decimal
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BinanceRealExecutor:
    """Real Binance order executor with comprehensive safety features"""
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.testnet = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        self.real_trading_enabled = os.getenv('ENABLE_REAL_TRADING', 'false').lower() == 'true'
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Binance API credentials not found in environment")
        
        # Initialize client only when needed
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        # Trading limits
        self.max_position_size = float(os.getenv('MAX_POSITION_SIZE', '100.0'))
        self.min_balance_required = float(os.getenv('MIN_ACCOUNT_BALANCE', '100.0'))
        
    def _initialize_client(self):
        """Lazy initialization of Binance client"""
        if self.client is None:
            try:
                from binance.client import Client
                self.client = Client(
                    api_key=self.api_key,
                    api_secret=self.secret_key,
                    testnet=self.testnet
                )
            except ImportError:
                raise ImportError("python-binance not installed. Run: pip install python-binance")
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information and balances"""
        self._initialize_client()
        try:
            return self.client.get_account()
        except Exception as e:
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
        self._initialize_client()
        try:
            info = self.client.get_symbol_info(symbol)
            return info
        except Exception as e:
            self.logger.error(f"Failed to get symbol info for {symbol}: {e}")
            raise
    
    def calculate_quantity(self, symbol: str, usdt_amount: float) -> float:
        """Calculate quantity based on USDT amount and current price"""
        self._initialize_client()
        try:
            # Get current price
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
                # Calculate precision from step size
                precision = 0
                temp_step = step_size
                while temp_step < 1:
                    temp_step *= 10
                    precision += 1
                quantity = round(quantity, precision)
            
            return quantity
            
        except Exception as e:
            self.logger.error(f"Failed to calculate quantity: {e}")
            raise
    
    def _safety_checks(self, usdt_amount: float) -> bool:
        """Perform safety checks before placing order"""
        # Check if real trading is enabled
        if not self.real_trading_enabled:
            self.logger.warning("Real trading not enabled")
            return False
        
        # Check position size limit
        if usdt_amount > self.max_position_size:
            self.logger.error(f"Position size ${usdt_amount:.2f} exceeds limit ${self.max_position_size:.2f}")
            return False
        
        # Check minimum balance
        balance = self.get_balance('USDT')
        if balance < self.min_balance_required:
            self.logger.error(f"Account balance ${balance:.2f} below required ${self.min_balance_required:.2f}")
            return False
        
        # Check sufficient balance for order
        if balance < usdt_amount:
            self.logger.error(f"Insufficient balance. Have: ${balance:.2f}, Need: ${usdt_amount:.2f}")
            return False
        
        return True
    
    def place_market_buy(self, symbol: str, usdt_amount: float) -> Optional[Dict[str, Any]]:
        """Place market buy order with safety checks"""
        if not self._safety_checks(usdt_amount):
            return None
        
        self._initialize_client()
        try:
            # Calculate quantity
            quantity = self.calculate_quantity(symbol, usdt_amount)
            
            self.logger.info(f"Placing BUY order: {quantity:.8f} {symbol} (~${usdt_amount:.2f})")
            
            # Place order
            order = self.client.order_market_buy(
                symbol=symbol,
                quantity=quantity
            )
            
            self.logger.info(f"Market BUY order placed successfully: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to place buy order: {e}")
            raise
    
    def place_market_sell(self, symbol: str, quantity: float) -> Optional[Dict[str, Any]]:
        """Place market sell order with safety checks"""
        if not self.real_trading_enabled:
            self.logger.warning(f"Real trading not enabled. Would SELL {quantity:.8f} {symbol}")
            return None
        
        self._initialize_client()
        try:
            # Get base asset (e.g., BTC from BTCUSDT)
            base_asset = symbol.replace('USDT', '').replace('BUSD', '').replace('USDC', '')
            balance = self.get_balance(base_asset)
            
            if balance < quantity:
                raise ValueError(f"Insufficient {base_asset}. Have: {balance:.8f}, Need: {quantity:.8f}")
            
            self.logger.info(f"Placing SELL order: {quantity:.8f} {symbol}")
            
            # Place order
            order = self.client.order_market_sell(
                symbol=symbol,
                quantity=quantity
            )
            
            self.logger.info(f"Market SELL order placed successfully: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to place sell order: {e}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        self._initialize_client()
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Failed to get price for {symbol}: {e}")
            raise
    
    def get_24h_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get 24h ticker statistics"""
        self._initialize_client()
        try:
            return self.client.get_24hr_ticker(symbol=symbol)
        except Exception as e:
            self.logger.error(f"Failed to get 24h ticker for {symbol}: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get order status by ID"""
        self._initialize_client()
        try:
            return self.client.get_order(symbol=symbol, orderId=order_id)
        except Exception as e:
            self.logger.error(f"Failed to get order status: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an open order"""
        if not self.real_trading_enabled:
            self.logger.warning(f"Real trading not enabled. Would cancel order {order_id}")
            return {}
        
        self._initialize_client()
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order {order_id} cancelled successfully")
            return result
        except Exception as e:
            self.logger.error(f"Failed to cancel order {order_id}: {e}")
            raise
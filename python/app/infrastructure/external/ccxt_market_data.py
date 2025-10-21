"""
CCXT Market Data Repository Implementation.
"""
import ccxt
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

from ...domain.repositories.market_data_repository import MarketDataRepository
from ...domain.value_objects.symbol import TradingSymbol
from ...domain.value_objects.money import Money


class CCXTMarketDataRepository(MarketDataRepository):
    """
    Market data repository using CCXT library for cryptocurrency exchanges.
    
    This implementation fetches real market data from Binance.
    """
    
    def __init__(self, exchange_id: str = 'binance'):
        """
        Initialize with specified exchange.
        
        Args:
            exchange_id: CCXT exchange identifier (default: binance)
        """
        self._exchange_class = getattr(ccxt, exchange_id)
        self._exchange = self._exchange_class({
            'sandbox': False,  # Use live data
            'rateLimit': 1200,  # Be respectful with API calls
            'enableRateLimit': True,
        })
    
    async def get_current_price(self, symbol: TradingSymbol) -> Money:
        """Get the current market price for a symbol."""
        try:
            ticker = self._exchange.fetch_ticker(symbol.to_ccxt_format())
            current_price = Decimal(str(ticker['last']))
            
            return Money(current_price, symbol.quote_currency)
        except Exception as e:
            raise MarketDataError(f"Failed to fetch current price for {symbol}: {e}")
    
    async def get_historical_data(self, symbol: TradingSymbol, timeframe: str, 
                                 lookback_periods: int = 100) -> pd.DataFrame:
        """Get historical market data."""
        try:
            # Calculate the since timestamp
            timeframe_minutes = self._timeframe_to_minutes(timeframe)
            since_datetime = datetime.now() - timedelta(minutes=timeframe_minutes * lookback_periods)
            since_timestamp = int(since_datetime.timestamp() * 1000)
            
            # Fetch OHLCV data
            ohlcv = self._exchange.fetch_ohlcv(
                symbol.to_ccxt_format(),
                timeframe,
                since=since_timestamp,
                limit=lookback_periods
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
        except Exception as e:
            raise MarketDataError(f"Failed to fetch historical data for {symbol}: {e}")
    
    async def get_recent_candles(self, symbol: TradingSymbol, timeframe: str, 
                               limit: int = 50) -> pd.DataFrame:
        """Get recent candlestick data."""
        try:
            ohlcv = self._exchange.fetch_ohlcv(
                symbol.to_ccxt_format(),
                timeframe,
                limit=limit
            )
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
        except Exception as e:
            raise MarketDataError(f"Failed to fetch recent candles for {symbol}: {e}")
    
    async def is_market_open(self, symbol: TradingSymbol) -> bool:
        """Check if the market is currently open for trading."""
        try:
            # For crypto markets, typically 24/7
            # This could be enhanced to check exchange status
            ticker = self._exchange.fetch_ticker(symbol.to_ccxt_format())
            return ticker is not None
        except Exception:
            return False
    
    async def get_trading_fees(self, symbol: TradingSymbol) -> dict:
        """Get trading fees for a symbol."""
        try:
            markets = self._exchange.load_markets()
            market = markets.get(symbol.to_ccxt_format())
            
            if not market:
                raise MarketDataError(f"Market not found for symbol: {symbol}")
            
            return {
                'maker': market.get('maker', 0.001),  # Default 0.1%
                'taker': market.get('taker', 0.001),  # Default 0.1%
                'percentage': True
            }
        except Exception as e:
            raise MarketDataError(f"Failed to fetch trading fees for {symbol}: {e}")
    
    def _timeframe_to_minutes(self, timeframe: str) -> int:
        """Convert timeframe string to minutes."""
        timeframe_minutes = {
            '1m': 1,
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60,
            '4h': 240,
            '1d': 1440,
            '1w': 10080
        }
        
        return timeframe_minutes.get(timeframe, 60)  # Default to 1 hour


class MarketDataError(Exception):
    """Exception raised for market data related errors."""
    pass
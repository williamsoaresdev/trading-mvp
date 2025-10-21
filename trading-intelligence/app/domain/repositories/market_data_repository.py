"""
Market Data Repository Interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import pandas as pd

from ..value_objects.symbol import TradingSymbol
from ..value_objects.money import Money


class MarketDataRepository(ABC):
    """
    Abstract repository for market data.
    
    Handles fetching and caching of market data for trading decisions.
    """
    
    @abstractmethod
    async def get_current_price(self, symbol: TradingSymbol) -> Money:
        """
        Get the current market price for a symbol.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            Current market price
            
        Raises:
            MarketDataError: If price cannot be retrieved
        """
        pass
    
    @abstractmethod
    async def get_historical_data(self, symbol: TradingSymbol, timeframe: str, 
                                 lookback_periods: int = 100) -> pd.DataFrame:
        """
        Get historical market data.
        
        Args:
            symbol: The trading symbol
            timeframe: Timeframe (e.g., '1h', '4h', '1d')
            lookback_periods: Number of periods to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """
        pass
    
    @abstractmethod
    async def get_recent_candles(self, symbol: TradingSymbol, timeframe: str, 
                               limit: int = 50) -> pd.DataFrame:
        """
        Get recent candlestick data.
        
        Args:
            symbol: The trading symbol
            timeframe: Timeframe (e.g., '1h', '4h', '1d')
            limit: Number of recent candles to retrieve
            
        Returns:
            DataFrame with recent OHLCV data
        """
        pass
    
    @abstractmethod
    async def is_market_open(self, symbol: TradingSymbol) -> bool:
        """
        Check if the market is currently open for trading.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            True if market is open, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_trading_fees(self, symbol: TradingSymbol) -> dict:
        """
        Get trading fees for a symbol.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            Dictionary with fee information (maker, taker fees)
        """
        pass
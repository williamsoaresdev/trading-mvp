"""
Trading Symbol Value Object.
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TradingSymbol:
    """
    Value object representing a trading symbol (e.g., BTC/USDT).
    
    Ensures symbol format is valid and provides utility methods.
    """
    
    symbol: str
    
    def __post_init__(self):
        """Validate trading symbol format."""
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")
        
        # Basic validation for crypto pairs (BASE/QUOTE format)
        if not re.match(r'^[A-Z0-9]+/[A-Z0-9]+$', self.symbol):
            raise ValueError(f"Invalid symbol format: {self.symbol}. Expected format: BASE/QUOTE (e.g., BTC/USDT)")
        
        parts = self.symbol.split('/')
        if len(parts) != 2:
            raise ValueError(f"Symbol must contain exactly one '/' separator: {self.symbol}")
        
        base, quote = parts
        if len(base) < 2 or len(quote) < 2:
            raise ValueError(f"Base and quote currencies must be at least 2 characters: {self.symbol}")
    
    def __str__(self) -> str:
        """String representation."""
        return self.symbol
    
    @property
    def base_currency(self) -> str:
        """Get the base currency (left side of /)."""
        return self.symbol.split('/')[0]
    
    @property
    def quote_currency(self) -> str:
        """Get the quote currency (right side of /)."""
        return self.symbol.split('/')[1]
    
    @property
    def normalized(self) -> str:
        """Get normalized symbol (uppercase, no spaces)."""
        return self.symbol.upper().replace(' ', '')
    
    def is_crypto_pair(self) -> bool:
        """Check if this appears to be a cryptocurrency pair."""
        common_crypto_quotes = {'USDT', 'USDC', 'BTC', 'ETH', 'USD', 'EUR'}
        return self.quote_currency in common_crypto_quotes
    
    def is_fiat_pair(self) -> bool:
        """Check if this appears to be a fiat currency pair."""
        common_fiat = {'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF'}
        return self.base_currency in common_fiat and self.quote_currency in common_fiat
    
    @classmethod
    def from_string(cls, symbol_str: str) -> 'TradingSymbol':
        """Create from string, with normalization."""
        normalized = symbol_str.upper().replace(' ', '').replace('_', '/')
        return cls(normalized)
    
    @classmethod
    def btc_usdt(cls) -> 'TradingSymbol':
        """Create BTC/USDT symbol (commonly used for testing)."""
        return cls("BTC/USDT")
    
    @classmethod
    def eth_usdt(cls) -> 'TradingSymbol':
        """Create ETH/USDT symbol."""
        return cls("ETH/USDT")
    
    def to_ccxt_format(self) -> str:
        """Convert to ccxt library format."""
        return self.symbol  # ccxt uses BASE/QUOTE format
    
    def to_binance_format(self) -> str:
        """Convert to Binance API format (BASEQUOTE)."""
        return self.symbol.replace('/', '')
    
    def to_filename_safe(self) -> str:
        """Convert to filename-safe format."""
        return self.symbol.replace('/', '_')
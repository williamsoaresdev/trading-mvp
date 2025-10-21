"""
Trading Action Value Object.
"""
from enum import Enum


class TradingAction(Enum):
    """
    Value object representing possible trading actions.
    
    This is immutable and represents the three possible states
    of a trading decision.
    """
    
    BUY = "BUY"
    SELL = "SELL" 
    FLAT = "FLAT"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def from_probabilities(cls, buy_prob: float, sell_prob: float, 
                          buy_threshold: float = 0.6, sell_threshold: float = 0.6) -> 'TradingAction':
        """
        Determine trading action from buy/sell probabilities.
        
        Args:
            buy_prob: Probability of buying (0.0 to 1.0)
            sell_prob: Probability of selling (0.0 to 1.0)
            buy_threshold: Minimum confidence required for buy signal
            sell_threshold: Minimum confidence required for sell signal
            
        Returns:
            TradingAction based on probabilities and thresholds
        """
        if buy_prob >= buy_threshold and buy_prob > sell_prob:
            return cls.BUY
        elif sell_prob >= sell_threshold and sell_prob > buy_prob:
            return cls.SELL
        else:
            return cls.FLAT
    
    @property
    def is_directional(self) -> bool:
        """Check if action is directional (BUY or SELL)."""
        return self in [TradingAction.BUY, TradingAction.SELL]
    
    @property
    def is_long(self) -> bool:
        """Check if action is a long position (BUY)."""
        return self == TradingAction.BUY
    
    @property
    def is_short(self) -> bool:
        """Check if action is a short position (SELL)."""
        return self == TradingAction.SELL
    
    @property
    def is_neutral(self) -> bool:
        """Check if action is neutral (FLAT)."""
        return self == TradingAction.FLAT
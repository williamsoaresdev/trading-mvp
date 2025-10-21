"""
Trading Decision Entity - Core domain entity representing a trading decision.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

from ..value_objects.trading_action import TradingAction
from ..value_objects.money import Money
from ..value_objects.percentage import Percentage
from ..value_objects.symbol import TradingSymbol


@dataclass(frozen=True)
class TradingDecision:
    """
    Core entity representing a trading decision.
    
    This is the heart of our trading domain - immutable and containing
    all necessary information for making trading decisions.
    """
    
    # Unique identifier
    decision_id: str
    
    # Trading parameters
    symbol: TradingSymbol
    action: TradingAction
    timestamp: datetime
    
    # Confidence levels
    buy_probability: Percentage
    sell_probability: Percentage
    
    # Price and position information
    current_price: Money
    position_fraction: Percentage
    atr_percentage: Percentage
    
    # Optional metadata
    timeframe: str = "1h"
    confidence_score: Optional[float] = None
    risk_score: Optional[float] = None
    
    def __post_init__(self):
        """Validate the decision after creation."""
        self._validate_probabilities()
        self._validate_position_fraction()
        
    def _validate_probabilities(self):
        """Ensure probabilities are valid."""
        total_prob = self.buy_probability.value + self.sell_probability.value
        if total_prob > 1.0:
            raise ValueError("Buy and sell probabilities cannot exceed 100%")
            
    def _validate_position_fraction(self):
        """Ensure position fraction is reasonable."""
        if self.position_fraction.value <= 0:
            raise ValueError("Position fraction must be positive")
        if self.position_fraction.value > 1:
            raise ValueError("Position fraction cannot exceed 100%")
    
    @property
    def is_buy_signal(self) -> bool:
        """Check if this is a buy signal."""
        return self.action == TradingAction.BUY
    
    @property
    def is_sell_signal(self) -> bool:
        """Check if this is a sell signal."""
        return self.action == TradingAction.SELL
    
    @property
    def is_flat_signal(self) -> bool:
        """Check if this is a flat (no action) signal."""
        return self.action == TradingAction.FLAT
    
    @property
    def max_probability(self) -> Percentage:
        """Get the maximum probability between buy and sell."""
        return max(self.buy_probability, self.sell_probability)
    
    def meets_confidence_threshold(self, threshold: Percentage) -> bool:
        """Check if decision meets minimum confidence threshold."""
        return self.max_probability >= threshold
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "decision_id": self.decision_id,
            "symbol": str(self.symbol),
            "action": self.action.value,
            "timestamp": self.timestamp.isoformat(),
            "buy_probability": self.buy_probability.value,
            "sell_probability": self.sell_probability.value,
            "current_price": self.current_price.amount,
            "position_fraction": self.position_fraction.value,
            "atr_percentage": self.atr_percentage.value,
            "timeframe": self.timeframe,
            "confidence_score": self.confidence_score,
            "risk_score": self.risk_score
        }
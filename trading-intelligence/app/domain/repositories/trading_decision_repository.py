"""
Trading Decision Repository Interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities.trading_decision import TradingDecision
from ..value_objects.symbol import TradingSymbol


class TradingDecisionRepository(ABC):
    """
    Abstract repository for trading decisions.
    
    This defines the contract for persisting and retrieving trading decisions,
    following the Repository pattern from DDD.
    """
    
    @abstractmethod
    async def save(self, decision: TradingDecision) -> None:
        """
        Save a trading decision.
        
        Args:
            decision: The trading decision to save
            
        Raises:
            RepositoryError: If save operation fails
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, decision_id: str) -> Optional[TradingDecision]:
        """
        Find a trading decision by its ID.
        
        Args:
            decision_id: Unique identifier for the decision
            
        Returns:
            The trading decision if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_symbol(self, symbol: TradingSymbol, limit: int = 100) -> List[TradingDecision]:
        """
        Find trading decisions for a specific symbol.
        
        Args:
            symbol: The trading symbol to search for
            limit: Maximum number of decisions to return
            
        Returns:
            List of trading decisions, ordered by timestamp (newest first)
        """
        pass
    
    @abstractmethod
    async def find_recent(self, limit: int = 50) -> List[TradingDecision]:
        """
        Find the most recent trading decisions.
        
        Args:
            limit: Maximum number of decisions to return
            
        Returns:
            List of recent trading decisions, ordered by timestamp (newest first)
        """
        pass
    
    @abstractmethod
    async def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[TradingDecision]:
        """
        Find trading decisions within a date range.
        
        Args:
            start_date: Start of the date range (inclusive)
            end_date: End of the date range (inclusive)
            
        Returns:
            List of trading decisions within the date range
        """
        pass
    
    @abstractmethod
    async def count_total(self) -> int:
        """
        Get total count of all trading decisions.
        
        Returns:
            Total number of decisions in the repository
        """
        pass
    
    @abstractmethod
    async def count_by_symbol(self, symbol: TradingSymbol) -> int:
        """
        Get count of decisions for a specific symbol.
        
        Args:
            symbol: The trading symbol to count
            
        Returns:
            Number of decisions for the symbol
        """
        pass
    
    @abstractmethod
    async def delete_older_than(self, cutoff_date: datetime) -> int:
        """
        Delete decisions older than the specified date.
        
        Args:
            cutoff_date: Delete decisions older than this date
            
        Returns:
            Number of decisions deleted
        """
        pass
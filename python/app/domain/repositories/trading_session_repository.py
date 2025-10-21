"""
Trading Session Repository Interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.trading_session import TradingSession, SessionStatus
from ..value_objects.symbol import TradingSymbol


class TradingSessionRepository(ABC):
    """
    Abstract repository for trading sessions.
    
    Manages persistence and retrieval of trading sessions.
    """
    
    @abstractmethod
    async def save(self, session: TradingSession) -> None:
        """
        Save a trading session.
        
        Args:
            session: The trading session to save
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, session_id: str) -> Optional[TradingSession]:
        """
        Find a trading session by its ID.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            The trading session if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_active_session(self, symbol: TradingSymbol) -> Optional[TradingSession]:
        """
        Find the active trading session for a symbol.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            The active session if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: SessionStatus) -> List[TradingSession]:
        """
        Find sessions by status.
        
        Args:
            status: The session status to filter by
            
        Returns:
            List of sessions with the specified status
        """
        pass
    
    @abstractmethod
    async def find_recent(self, limit: int = 10) -> List[TradingSession]:
        """
        Find the most recent trading sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of recent sessions, ordered by created_at (newest first)
        """
        pass
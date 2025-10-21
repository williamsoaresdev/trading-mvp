"""
In-Memory Trading Session Repository Implementation.
"""
from typing import List, Optional, Dict

from ...domain.entities.trading_session import TradingSession, SessionStatus
from ...domain.repositories.trading_session_repository import TradingSessionRepository
from ...domain.value_objects.symbol import TradingSymbol


class InMemoryTradingSessionRepository(TradingSessionRepository):
    """
    In-memory implementation of trading session repository.
    """
    
    def __init__(self):
        self._sessions: Dict[str, TradingSession] = {}
        self._active_sessions_by_symbol: Dict[str, str] = {}  # symbol -> session_id
    
    async def save(self, session: TradingSession) -> None:
        """Save a trading session."""
        self._sessions[session.session_id] = session
        
        # Update active session tracking
        symbol_key = str(session.symbol)
        if session.is_active:
            self._active_sessions_by_symbol[symbol_key] = session.session_id
        elif symbol_key in self._active_sessions_by_symbol and self._active_sessions_by_symbol[symbol_key] == session.session_id:
            # Remove from active if session is no longer active
            del self._active_sessions_by_symbol[symbol_key]
    
    async def find_by_id(self, session_id: str) -> Optional[TradingSession]:
        """Find a trading session by its ID."""
        return self._sessions.get(session_id)
    
    async def find_active_session(self, symbol: TradingSymbol) -> Optional[TradingSession]:
        """Find the active trading session for a symbol."""
        symbol_key = str(symbol)
        session_id = self._active_sessions_by_symbol.get(symbol_key)
        
        if session_id:
            session = self._sessions.get(session_id)
            if session and session.is_active:
                return session
            else:
                # Clean up stale reference
                del self._active_sessions_by_symbol[symbol_key]
        
        return None
    
    async def find_by_status(self, status: SessionStatus) -> List[TradingSession]:
        """Find sessions by status."""
        return [
            session for session in self._sessions.values()
            if session.status == status
        ]
    
    async def find_recent(self, limit: int = 10) -> List[TradingSession]:
        """Find the most recent trading sessions."""
        all_sessions = list(self._sessions.values())
        
        # Sort by created_at (newest first)
        all_sessions.sort(key=lambda s: s.created_at, reverse=True)
        
        return all_sessions[:limit]
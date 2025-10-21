"""
Start Trading Session Use Case.
"""
from dataclasses import dataclass
from typing import Optional
import uuid

from ...domain.entities.trading_session import TradingSession, SessionStatus
from ...domain.value_objects.symbol import TradingSymbol
from ...domain.repositories.trading_session_repository import TradingSessionRepository


@dataclass
class StartTradingSessionRequest:
    """Request for starting a trading session."""
    symbol: TradingSymbol
    decision_interval_seconds: int = 60
    max_decisions: int = 1000


@dataclass
class StartTradingSessionResponse:
    """Response for starting a trading session."""
    session: Optional[TradingSession]
    success: bool
    error_message: str = ""


class StartTradingSessionUseCase:
    """
    Use case for starting a new trading session.
    
    Ensures only one active session per symbol and handles session lifecycle.
    """
    
    def __init__(self, session_repository: TradingSessionRepository):
        self._session_repository = session_repository
    
    async def execute(self, request: StartTradingSessionRequest) -> StartTradingSessionResponse:
        """
        Execute the use case to start a trading session.
        
        Args:
            request: The request containing session parameters
            
        Returns:
            Response containing the started session or error
        """
        try:
            # 1. Check if there's already an active session for this symbol
            existing_session = await self._session_repository.find_active_session(request.symbol)
            
            if existing_session:
                return StartTradingSessionResponse(
                    session=None,
                    success=False,
                    error_message=f"Active session already exists for {request.symbol}"
                )
            
            # 2. Create new trading session
            session = TradingSession(
                session_id=str(uuid.uuid4()),
                symbol=request.symbol,
                decision_interval_seconds=request.decision_interval_seconds,
                max_decisions=request.max_decisions
            )
            
            # 3. Start the session
            session.start()
            
            # 4. Save the session
            await self._session_repository.save(session)
            
            return StartTradingSessionResponse(
                session=session,
                success=True
            )
            
        except Exception as e:
            return StartTradingSessionResponse(
                session=None,
                success=False,
                error_message=str(e)
            )
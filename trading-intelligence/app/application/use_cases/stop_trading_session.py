"""
Stop Trading Session Use Case.
"""
from dataclasses import dataclass
from typing import Optional

from ...domain.entities.trading_session import TradingSession
from ...domain.value_objects.symbol import TradingSymbol
from ...domain.repositories.trading_session_repository import TradingSessionRepository


@dataclass
class StopTradingSessionRequest:
    """Request for stopping a trading session."""
    symbol: TradingSymbol


@dataclass
class StopTradingSessionResponse:
    """Response for stopping a trading session."""
    session: Optional[TradingSession]
    success: bool
    error_message: str = ""


class StopTradingSessionUseCase:
    """
    Use case for stopping an active trading session.
    """
    
    def __init__(self, session_repository: TradingSessionRepository):
        self._session_repository = session_repository
    
    async def execute(self, request: StopTradingSessionRequest) -> StopTradingSessionResponse:
        """
        Execute the use case to stop a trading session.
        
        Args:
            request: The request containing symbol to stop
            
        Returns:
            Response containing the stopped session or error
        """
        try:
            # 1. Find active session for the symbol
            session = await self._session_repository.find_active_session(request.symbol)
            
            if not session:
                return StopTradingSessionResponse(
                    session=None,
                    success=False,
                    error_message=f"No active session found for {request.symbol}"
                )
            
            # 2. Stop the session
            session.stop()
            
            # 3. Save the updated session
            await self._session_repository.save(session)
            
            return StopTradingSessionResponse(
                session=session,
                success=True
            )
            
        except Exception as e:
            return StopTradingSessionResponse(
                session=None,
                success=False,
                error_message=str(e)
            )
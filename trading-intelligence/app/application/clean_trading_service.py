"""
Clean Real-Time Trading Service using Clean Architecture.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ..domain.entities.trading_session import TradingSession, SessionStatus
from ..domain.value_objects.symbol import TradingSymbol
from ..domain.repositories.trading_session_repository import TradingSessionRepository
from ..application.use_cases.start_trading_session import StartTradingSessionUseCase, StartTradingSessionRequest
from ..application.use_cases.stop_trading_session import StopTradingSessionUseCase, StopTradingSessionRequest
from ..application.use_cases.generate_trading_decision import GenerateTradingDecisionUseCase, GenerateTradingDecisionRequest


logger = logging.getLogger(__name__)


@dataclass
class TradingServiceConfig:
    """Configuration for the trading service."""
    default_symbol: str = "BTC/USDT"
    default_timeframe: str = "1h"
    decision_interval_seconds: int = 60
    buy_threshold: float = 0.6
    sell_threshold: float = 0.6
    max_decisions_per_session: int = 1000


class CleanTradingService:
    """
    Clean trading service implementing proper Clean Architecture.
    
    This service orchestrates trading operations using well-defined use cases
    and domain entities, following SOLID principles.
    """
    
    def __init__(
        self,
        session_repository: TradingSessionRepository,
        start_session_use_case: StartTradingSessionUseCase,
        stop_session_use_case: StopTradingSessionUseCase,
        generate_decision_use_case: GenerateTradingDecisionUseCase,
        config: TradingServiceConfig
    ):
        self._session_repository = session_repository
        self._start_session_use_case = start_session_use_case
        self._stop_session_use_case = stop_session_use_case
        self._generate_decision_use_case = generate_decision_use_case
        self._config = config
        
        self._current_session: Optional[TradingSession] = None
        self._decision_task: Optional[asyncio.Task] = None
        self._is_running = False
    
    async def start_trading(self, symbol: Optional[str] = None, 
                          interval_seconds: Optional[int] = None) -> dict:
        """
        Start real-time trading for a symbol.
        
        Args:
            symbol: Trading symbol (defaults to config)
            interval_seconds: Decision interval (defaults to config)
            
        Returns:
            Response dictionary with status
        """
        try:
            trading_symbol = TradingSymbol.from_string(symbol or self._config.default_symbol)
            decision_interval = interval_seconds or self._config.decision_interval_seconds
            
            # Check if already running
            if self._is_running and self._current_session:
                return {
                    "success": False,
                    "message": f"Trading already running for {self._current_session.symbol}",
                    "session_id": self._current_session.session_id
                }
            
            # Start new session
            request = StartTradingSessionRequest(
                symbol=trading_symbol,
                decision_interval_seconds=decision_interval,
                max_decisions=self._config.max_decisions_per_session
            )
            
            response = await self._start_session_use_case.execute(request)
            
            if not response.success:
                return {
                    "success": False,
                    "message": response.error_message
                }
            
            self._current_session = response.session
            self._is_running = True
            
            # Start decision generation loop
            self._decision_task = asyncio.create_task(
                self._decision_generation_loop(trading_symbol, decision_interval)
            )
            
            logger.info(f"✅ Trading started for {trading_symbol}")
            
            return {
                "success": True,
                "message": f"Real-time trading started for {trading_symbol}",
                "session_id": self._current_session.session_id,
                "symbol": str(trading_symbol),
                "interval_seconds": decision_interval
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to start trading: {e}")
            return {
                "success": False,
                "message": f"Failed to start trading: {str(e)}"
            }
    
    async def stop_trading(self, symbol: Optional[str] = None) -> dict:
        """
        Stop real-time trading.
        
        Args:
            symbol: Trading symbol (optional)
            
        Returns:
            Response dictionary with status
        """
        try:
            if not self._is_running or not self._current_session:
                return {
                    "success": False,
                    "message": "No active trading session"
                }
            
            # Stop decision generation
            if self._decision_task:
                self._decision_task.cancel()
                try:
                    await self._decision_task
                except asyncio.CancelledError:
                    pass
                self._decision_task = None
            
            # Stop session
            request = StopTradingSessionRequest(symbol=self._current_session.symbol)
            response = await self._stop_session_use_case.execute(request)
            
            session_id = self._current_session.session_id
            symbol_str = str(self._current_session.symbol)
            
            self._current_session = None
            self._is_running = False
            
            logger.info(f"🛑 Trading stopped for {symbol_str}")
            
            return {
                "success": True,
                "message": f"Real-time trading stopped for {symbol_str}",
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to stop trading: {e}")
            return {
                "success": False,
                "message": f"Failed to stop trading: {str(e)}"
            }
    
    async def get_status(self) -> dict:
        """Get current trading status."""
        if not self._current_session:
            return {
                "is_running": False,
                "session": None,
                "decisions_count": 0
            }
        
        # Refresh session data from repository
        current_session = await self._session_repository.find_by_id(self._current_session.session_id)
        
        return {
            "is_running": self._is_running,
            "session": current_session.to_dict() if current_session else None,
            "decisions_count": current_session.decision_count if current_session else 0,
            "latest_decision": current_session.latest_decision.to_dict() if current_session and current_session.latest_decision else None
        }
    
    async def _decision_generation_loop(self, symbol: TradingSymbol, interval_seconds: int):
        """
        Main loop for generating trading decisions.
        
        This runs continuously until cancelled, generating decisions
        at regular intervals.
        """
        logger.info(f"🔄 Starting decision generation loop for {symbol}")
        
        try:
            while self._is_running and self._current_session:
                try:
                    # Generate new trading decision
                    request = GenerateTradingDecisionRequest(
                        symbol=symbol,
                        timeframe=self._config.default_timeframe,
                        buy_threshold=self._config.buy_threshold,
                        sell_threshold=self._config.sell_threshold
                    )
                    
                    response = await self._generate_decision_use_case.execute(request)
                    
                    if response.success and response.decision:
                        # Add decision to current session
                        if self._current_session and self._current_session.is_active:
                            self._current_session.add_decision(response.decision)
                            await self._session_repository.save(self._current_session)
                            
                            logger.info(f"📈 Generated decision: {response.decision.action} for {symbol}")
                        else:
                            logger.warning("⚠️ Session not active, stopping decision generation")
                            break
                    else:
                        logger.error(f"❌ Failed to generate decision: {response.error_message}")
                    
                    # Wait for next interval
                    await asyncio.sleep(interval_seconds)
                    
                except asyncio.CancelledError:
                    logger.info("🛑 Decision generation cancelled")
                    break
                except Exception as e:
                    logger.error(f"❌ Error in decision generation loop: {e}")
                    await asyncio.sleep(5)  # Brief pause before retry
                    
        except Exception as e:
            logger.error(f"❌ Fatal error in decision generation loop: {e}")
        finally:
            logger.info("🏁 Decision generation loop ended")
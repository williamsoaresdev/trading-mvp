"""
Trading Session Entity - Represents a trading session with multiple decisions.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

from .trading_decision import TradingDecision
from ..value_objects.symbol import TradingSymbol


class SessionStatus(Enum):
    """Trading session status."""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class TradingSession:
    """
    Entity representing a trading session.
    
    A session contains multiple trading decisions and tracks
    the overall state of the trading system.
    """
    
    # Identity
    session_id: str
    symbol: TradingSymbol
    
    # Status and timing
    status: SessionStatus = SessionStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    
    # Decisions made during this session
    decisions: List[TradingDecision] = field(default_factory=list)
    
    # Configuration
    decision_interval_seconds: int = 60
    max_decisions: int = 1000
    
    def start(self) -> None:
        """Start the trading session."""
        if self.status != SessionStatus.CREATED:
            raise ValueError(f"Cannot start session in {self.status} state")
        
        self.status = SessionStatus.ACTIVE
        self.started_at = datetime.now()
    
    def pause(self) -> None:
        """Pause the trading session."""
        if self.status != SessionStatus.ACTIVE:
            raise ValueError(f"Cannot pause session in {self.status} state")
        
        self.status = SessionStatus.PAUSED
    
    def resume(self) -> None:
        """Resume the trading session."""
        if self.status != SessionStatus.PAUSED:
            raise ValueError(f"Cannot resume session in {self.status} state")
        
        self.status = SessionStatus.ACTIVE
    
    def stop(self) -> None:
        """Stop the trading session."""
        if self.status in [SessionStatus.STOPPED, SessionStatus.ERROR]:
            return  # Already stopped
        
        self.status = SessionStatus.STOPPED
        self.stopped_at = datetime.now()
    
    def add_decision(self, decision: TradingDecision) -> None:
        """Add a new trading decision to the session."""
        if self.status != SessionStatus.ACTIVE:
            raise ValueError(f"Cannot add decision to {self.status} session")
        
        if len(self.decisions) >= self.max_decisions:
            raise ValueError(f"Session has reached maximum decisions limit: {self.max_decisions}")
        
        if decision.symbol != self.symbol:
            raise ValueError(f"Decision symbol {decision.symbol} doesn't match session symbol {self.symbol}")
        
        self.decisions.append(decision)
    
    def mark_error(self, error_message: str) -> None:
        """Mark session as error state."""
        self.status = SessionStatus.ERROR
        # In a real implementation, we would store the error message
    
    @property
    def is_active(self) -> bool:
        """Check if session is currently active."""
        return self.status == SessionStatus.ACTIVE
    
    @property
    def decision_count(self) -> int:
        """Get total number of decisions made."""
        return len(self.decisions)
    
    @property
    def buy_decisions(self) -> List[TradingDecision]:
        """Get all buy decisions."""
        return [d for d in self.decisions if d.is_buy_signal]
    
    @property
    def sell_decisions(self) -> List[TradingDecision]:
        """Get all sell decisions."""
        return [d for d in self.decisions if d.is_sell_signal]
    
    @property
    def flat_decisions(self) -> List[TradingDecision]:
        """Get all flat decisions."""
        return [d for d in self.decisions if d.is_flat_signal]
    
    @property
    def latest_decision(self) -> Optional[TradingDecision]:
        """Get the most recent decision."""
        return self.decisions[-1] if self.decisions else None
    
    @property
    def duration_seconds(self) -> Optional[int]:
        """Get session duration in seconds."""
        if not self.started_at:
            return None
        
        end_time = self.stopped_at or datetime.now()
        return int((end_time - self.started_at).total_seconds())
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "symbol": str(self.symbol),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "stopped_at": self.stopped_at.isoformat() if self.stopped_at else None,
            "decision_count": self.decision_count,
            "decision_interval_seconds": self.decision_interval_seconds,
            "duration_seconds": self.duration_seconds
        }
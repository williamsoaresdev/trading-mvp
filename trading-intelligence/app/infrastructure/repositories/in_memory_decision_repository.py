"""
In-Memory Trading Decision Repository Implementation.
"""
from typing import List, Optional, Dict
from datetime import datetime

from ...domain.entities.trading_decision import TradingDecision
from ...domain.repositories.trading_decision_repository import TradingDecisionRepository
from ...domain.value_objects.symbol import TradingSymbol


class InMemoryTradingDecisionRepository(TradingDecisionRepository):
    """
    In-memory implementation of trading decision repository.
    
    This is suitable for MVP and testing. In production, this would
    be replaced with a database implementation.
    """
    
    def __init__(self):
        self._decisions: Dict[str, TradingDecision] = {}
        self._decisions_by_symbol: Dict[str, List[str]] = {}
    
    async def save(self, decision: TradingDecision) -> None:
        """Save a trading decision."""
        self._decisions[decision.decision_id] = decision
        
        # Index by symbol for faster lookups
        symbol_key = str(decision.symbol)
        if symbol_key not in self._decisions_by_symbol:
            self._decisions_by_symbol[symbol_key] = []
        
        if decision.decision_id not in self._decisions_by_symbol[symbol_key]:
            self._decisions_by_symbol[symbol_key].append(decision.decision_id)
    
    async def find_by_id(self, decision_id: str) -> Optional[TradingDecision]:
        """Find a trading decision by its ID."""
        return self._decisions.get(decision_id)
    
    async def find_by_symbol(self, symbol: TradingSymbol, limit: int = 100) -> List[TradingDecision]:
        """Find trading decisions for a specific symbol."""
        symbol_key = str(symbol)
        decision_ids = self._decisions_by_symbol.get(symbol_key, [])
        
        decisions = [
            self._decisions[decision_id] 
            for decision_id in decision_ids 
            if decision_id in self._decisions
        ]
        
        # Sort by timestamp (newest first)
        decisions.sort(key=lambda d: d.timestamp, reverse=True)
        
        return decisions[:limit]
    
    async def find_recent(self, limit: int = 50) -> List[TradingDecision]:
        """Find the most recent trading decisions."""
        all_decisions = list(self._decisions.values())
        
        # Sort by timestamp (newest first)
        all_decisions.sort(key=lambda d: d.timestamp, reverse=True)
        
        return all_decisions[:limit]
    
    async def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[TradingDecision]:
        """Find trading decisions within a date range."""
        filtered_decisions = [
            decision for decision in self._decisions.values()
            if start_date <= decision.timestamp <= end_date
        ]
        
        # Sort by timestamp
        filtered_decisions.sort(key=lambda d: d.timestamp)
        
        return filtered_decisions
    
    async def count_total(self) -> int:
        """Get total count of all trading decisions."""
        return len(self._decisions)
    
    async def count_by_symbol(self, symbol: TradingSymbol) -> int:
        """Get count of decisions for a specific symbol."""
        symbol_key = str(symbol)
        return len(self._decisions_by_symbol.get(symbol_key, []))
    
    async def delete_older_than(self, cutoff_date: datetime) -> int:
        """Delete decisions older than the specified date."""
        decisions_to_delete = [
            decision_id for decision_id, decision in self._decisions.items()
            if decision.timestamp < cutoff_date
        ]
        
        deleted_count = 0
        for decision_id in decisions_to_delete:
            decision = self._decisions.pop(decision_id, None)
            if decision:
                # Remove from symbol index
                symbol_key = str(decision.symbol)
                if symbol_key in self._decisions_by_symbol:
                    try:
                        self._decisions_by_symbol[symbol_key].remove(decision_id)
                    except ValueError:
                        pass  # Already removed
                
                deleted_count += 1
        
        return deleted_count
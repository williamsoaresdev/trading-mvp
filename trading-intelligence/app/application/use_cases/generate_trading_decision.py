"""
Generate Trading Decision Use Case.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable
import uuid

from ...domain.entities.trading_decision import TradingDecision
from ...domain.value_objects.trading_action import TradingAction
from ...domain.value_objects.symbol import TradingSymbol
from ...domain.value_objects.money import Money
from ...domain.value_objects.percentage import Percentage
from ...domain.repositories.trading_decision_repository import TradingDecisionRepository
from ...domain.repositories.market_data_repository import MarketDataRepository


@runtime_checkable
class MLPredictionService(Protocol):
    """Protocol for ML prediction service."""
    
    async def predict(self, symbol: TradingSymbol, timeframe: str) -> dict:
        """Generate ML prediction for a symbol."""
        ...


@dataclass
class GenerateTradingDecisionRequest:
    """Request for generating a trading decision."""
    symbol: TradingSymbol
    timeframe: str = "1h"
    buy_threshold: float = 0.6
    sell_threshold: float = 0.6


@dataclass
class GenerateTradingDecisionResponse:
    """Response containing the trading decision."""
    decision: TradingDecision
    success: bool
    error_message: str = ""


class GenerateTradingDecisionUseCase:
    """
    Use case for generating trading decisions.
    
    This encapsulates the business logic for creating trading decisions
    based on ML predictions and market data.
    """
    
    def __init__(
        self,
        decision_repository: TradingDecisionRepository,
        market_data_repository: MarketDataRepository,
        ml_service: MLPredictionService
    ):
        self._decision_repository = decision_repository
        self._market_data_repository = market_data_repository
        self._ml_service = ml_service
    
    async def execute(self, request: GenerateTradingDecisionRequest) -> GenerateTradingDecisionResponse:
        """
        Execute the use case to generate a trading decision.
        
        Args:
            request: The request containing symbol and parameters
            
        Returns:
            Response containing the generated decision
        """
        try:
            # 1. Get ML prediction
            prediction = await self._ml_service.predict(request.symbol, request.timeframe)
            
            # 2. Get current market price
            current_price = await self._market_data_repository.get_current_price(request.symbol)
            
            # 3. Determine trading action
            action = TradingAction.from_probabilities(
                buy_prob=prediction["proba_buy"],
                sell_prob=prediction["proba_sell"],
                buy_threshold=request.buy_threshold,
                sell_threshold=request.sell_threshold
            )
            
            # 4. Create trading decision
            decision = TradingDecision(
                decision_id=str(uuid.uuid4()),
                symbol=request.symbol,
                action=action,
                timestamp=datetime.now(),
                buy_probability=Percentage.from_decimal(prediction["proba_buy"]),
                sell_probability=Percentage.from_decimal(prediction["proba_sell"]),
                current_price=current_price,
                position_fraction=Percentage.from_decimal(prediction["position_fraction"]),
                atr_percentage=Percentage.from_decimal(prediction["atr_pct"]),
                timeframe=request.timeframe,
                confidence_score=max(prediction["proba_buy"], prediction["proba_sell"]),
                risk_score=prediction.get("risk_score")
            )
            
            # 5. Save decision
            await self._decision_repository.save(decision)
            
            return GenerateTradingDecisionResponse(
                decision=decision,
                success=True
            )
            
        except Exception as e:
            return GenerateTradingDecisionResponse(
                decision=None,  # type: ignore
                success=False,
                error_message=str(e)
            )
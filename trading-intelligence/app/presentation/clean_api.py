"""
Clean FastAPI presentation layer using Clean Architecture.
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import logging
from datetime import datetime
from typing import Set

from ..application.clean_trading_service import CleanTradingService, TradingServiceConfig
from ..application.use_cases.generate_trading_decision import GenerateTradingDecisionUseCase
from ..application.use_cases.start_trading_session import StartTradingSessionUseCase
from ..application.use_cases.stop_trading_session import StopTradingSessionUseCase
from ..infrastructure.repositories.in_memory_decision_repository import InMemoryTradingDecisionRepository
from ..infrastructure.repositories.in_memory_session_repository import InMemoryTradingSessionRepository
from ..infrastructure.external.ccxt_market_data import CCXTMarketDataRepository
from ..infrastructure.ml.ml_prediction_service import MLPredictionService


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketConnectionManager:
    """
    Manages WebSocket connections following Single Responsibility Principle.
    """
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


# Dependency injection setup
def create_dependencies():
    """
    Create all dependencies following Dependency Inversion Principle.
    
    This function wires up all the dependencies needed for the application,
    following Clean Architecture principles.
    """
    # Repositories (Infrastructure layer)
    decision_repository = InMemoryTradingDecisionRepository()
    session_repository = InMemoryTradingSessionRepository()
    market_data_repository = CCXTMarketDataRepository()
    
    # ML Service (Infrastructure layer)
    ml_service = MLPredictionService()
    
    # Use Cases (Application layer)
    generate_decision_use_case = GenerateTradingDecisionUseCase(
        decision_repository=decision_repository,
        market_data_repository=market_data_repository,
        ml_service=ml_service
    )
    
    start_session_use_case = StartTradingSessionUseCase(
        session_repository=session_repository
    )
    
    stop_session_use_case = StopTradingSessionUseCase(
        session_repository=session_repository
    )
    
    # Configuration
    config = TradingServiceConfig(
        default_symbol="BTC/USDT",
        decision_interval_seconds=60,
        buy_threshold=0.6,
        sell_threshold=0.6
    )
    
    # Application Service
    trading_service = CleanTradingService(
        session_repository=session_repository,
        start_session_use_case=start_session_use_case,
        stop_session_use_case=stop_session_use_case,
        generate_decision_use_case=generate_decision_use_case,
        config=config
    )
    
    return {
        'trading_service': trading_service,
        'decision_repository': decision_repository,
        'session_repository': session_repository
    }


# Global dependencies (in a real app, this would use proper DI container)
dependencies = create_dependencies()
trading_service = dependencies['trading_service']
decision_repository = dependencies['decision_repository']
session_repository = dependencies['session_repository']

# WebSocket manager
connection_manager = WebSocketConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("🚀 Starting Clean Trading API")
    yield
    logger.info("🛑 Shutting down Clean Trading API")
    await trading_service.stop_trading()


# Create FastAPI app
app = FastAPI(
    title="Clean Real-Time Trading API",
    description="Trading API built with Clean Architecture principles",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await connection_manager.connect(websocket)
    try:
        # Send initial status
        status = await trading_service.get_status()
        await websocket.send_text(json.dumps({
            "type": "status",
            "data": {
                "connected": True,
                "timestamp": datetime.now().isoformat(),
                **status
            }
        }))
        
        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            # Echo back for now (could handle commands in the future)
            await websocket.send_text(f"Echo: {data}")
            
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket)


# REST API Endpoints
@app.get("/health")
async def health():
    """Health check endpoint."""
    status = await trading_service.get_status()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "websocket_connections": len(connection_manager.active_connections),
        "trading_status": status
    }


@app.post("/trading/start")
async def start_trading(symbol: str = "BTC/USDT", interval_seconds: int = 60):
    """Start real-time trading."""
    try:
        result = await trading_service.start_trading(symbol, interval_seconds)
        
        if result["success"]:
            # Notify WebSocket clients
            await connection_manager.broadcast({
                "type": "trading_started",
                "data": result
            })
        
        return result
    except Exception as e:
        logger.error(f"Error starting trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trading/stop")
async def stop_trading():
    """Stop real-time trading."""
    try:
        result = await trading_service.stop_trading()
        
        if result["success"]:
            # Notify WebSocket clients
            await connection_manager.broadcast({
                "type": "trading_stopped",
                "data": result
            })
        
        return result
    except Exception as e:
        logger.error(f"Error stopping trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/trading/status")
async def get_trading_status():
    """Get current trading status."""
    try:
        return await trading_service.get_status()
    except Exception as e:
        logger.error(f"Error getting trading status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/trading/history")
async def get_trading_history(limit: int = 50):
    """Get recent trading decisions."""
    try:
        decisions = await decision_repository.find_recent(limit)
        return {
            "decisions": [decision.to_dict() for decision in decisions],
            "total": await decision_repository.count_total()
        }
    except Exception as e:
        logger.error(f"Error getting trading history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/recent")
async def get_recent_sessions(limit: int = 10):
    """Get recent trading sessions."""
    try:
        sessions = await session_repository.find_recent(limit)
        return {
            "sessions": [session.to_dict() for session in sessions],
            "total": len(sessions)
        }
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "clean_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
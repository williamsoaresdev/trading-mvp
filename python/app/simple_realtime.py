#!/usr/bin/env python3
"""
Simple Real-time Trading Service - Uses existing service.py
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

class SimpleTradingService:
    """Simple trading service with real-time capabilities"""
    
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.is_running = False
        self.trading_history: List[Dict] = []
        self.last_prediction: Optional[Dict] = None
    
    async def start_real_time_trading(self, symbol: str = "BTC/USDT", interval_seconds: int = 60):
        """Start real-time trading loop"""
        self.is_running = True
        logger.info(f"Starting real-time trading for {symbol}")
        
        while self.is_running:
            try:
                # Make dummy prediction for testing
                prediction = {
                    "symbol": symbol,
                    "timeframe": "1h", 
                    "action": "BUY",
                    "proba_buy": 0.65,
                    "proba_sell": 0.35,
                    "current_price": 50000.0,
                    "position_fraction": 0.1,
                    "atr_pct": 0.02,
                    "ts_utc": datetime.now().isoformat()
                }
                
                # Create trading decision
                decision = {
                    "timestamp": datetime.now().isoformat(),
                    "symbol": symbol,
                    "prediction": prediction,
                    "decision_id": int(time.time() * 1000)
                }
                
                # Store in history
                self.trading_history.append(decision)
                self.last_prediction = decision
                
                # Keep only last 100 decisions
                if len(self.trading_history) > 100:
                    self.trading_history = self.trading_history[-100:]
                
                # Broadcast to all connected clients
                await self.connection_manager.broadcast(json.dumps({
                    "type": "trading_decision",
                    "data": decision
                }))
                
                logger.info(f"Broadcasting decision: {prediction['action']} for {symbol}")
                
                # Wait for next iteration
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in real-time trading loop: {e}")
                await asyncio.sleep(5)
    
    def stop_real_time_trading(self):
        """Stop real-time trading loop"""
        self.is_running = False
        logger.info("Stopping real-time trading")

# Initialize services
app = FastAPI(
    title="Simple Real-Time Trading API",
    description="Testing version of real-time trading API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize simple service
simple_service = SimpleTradingService()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await simple_service.connection_manager.connect(websocket)
    try:
        # Send current status
        status_message = {
            "type": "status",
            "data": {
                "connected": True,
                "timestamp": datetime.now().isoformat(),
                "is_trading": simple_service.is_running,
                "total_decisions": len(simple_service.trading_history)
            }
        }
        await websocket.send_text(json.dumps(status_message))
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
            
    except WebSocketDisconnect:
        simple_service.connection_manager.disconnect(websocket)

# REST API Endpoints
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "websocket_connections": len(simple_service.connection_manager.active_connections),
        "is_trading": simple_service.is_running
    }

@app.post("/predict")
async def predict():
    """Simple predict endpoint for testing"""
    return {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "action": "BUY", 
        "proba_buy": 0.65,
        "proba_sell": 0.35,
        "current_price": 50000.0,
        "position_fraction": 0.1,
        "atr_pct": 0.02,
        "ts_utc": datetime.now().isoformat()
    }

@app.get("/trading/history")
async def get_trading_history(limit: int = 50):
    """Get recent trading decisions"""
    return {
        "decisions": simple_service.trading_history[-limit:],
        "total": len(simple_service.trading_history)
    }

@app.post("/trading/start")
async def start_trading(symbol: str = "BTC/USDT", interval_seconds: int = 30):
    """Start real-time trading"""
    if simple_service.is_running:
        return {"message": "Trading already running", "status": "running"}
    
    # Start in background
    asyncio.create_task(simple_service.start_real_time_trading(symbol, interval_seconds))
    return {"message": "Real-time trading started", "symbol": symbol, "interval": interval_seconds}

@app.post("/trading/stop")
async def stop_trading():
    """Stop real-time trading"""
    simple_service.stop_real_time_trading()
    return {"message": "Real-time trading stopped"}

@app.get("/trading/status")
async def get_trading_status():
    """Get current trading status"""
    return {
        "is_running": simple_service.is_running,
        "connections": len(simple_service.connection_manager.active_connections),
        "total_decisions": len(simple_service.trading_history),
        "last_prediction": simple_service.last_prediction
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_realtime:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
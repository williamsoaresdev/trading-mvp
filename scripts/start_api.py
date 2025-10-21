#!/usr/bin/env python3
"""
Direct API Starter
"""
import sys
import os
import uvicorn

# Add python directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
python_dir = os.path.join(current_dir, 'python')
sys.path.insert(0, python_dir)

from app.simple_realtime import app

if __name__ == "__main__":
    print("🚀 Starting Real-Time Trading API...")
    print("📡 WebSocket endpoint: ws://localhost:8000/ws")
    print("🌐 API docs: http://localhost:8000/docs")
    print("🏥 Health check: http://localhost:8000/health")
    print()
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
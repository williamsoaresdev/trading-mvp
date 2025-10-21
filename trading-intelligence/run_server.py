#!/usr/bin/env python3
"""
Servidor de teste simples para verificar se a API funciona
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.service import app
    import uvicorn
    print("Starting FastAPI server on http://localhost:8000")
    print("Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
#!/usr/bin/env python3
"""
Script para iniciar o servidor FastAPI
"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.service:app", host="0.0.0.0", port=8000, reload=False)
#!/usr/bin/env python3
"""
Start the Clean Trading API with proper architecture.
"""
import sys
import os
from pathlib import Path
import uvicorn

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "python"))

if __name__ == "__main__":
    print("🚀 Starting Clean Real-Time Trading API")
    print("=" * 50)
    print("📐 Architecture: Clean Architecture + DDD")
    print("🔧 Features: SOLID Principles + Dependency Injection")
    print("🎯 Domain-Driven Design with Use Cases")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "python.app.presentation.clean_api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Clean Trading API")
    except Exception as e:
        print(f"❌ Error starting API: {e}")
        sys.exit(1)
#!/usr/bin/env python3
"""
Trading MVP - Development Server Runner
Starts the FastAPI server with proper environment setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_virtual_env():
    """Check if virtual environment is activated"""
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run setup first: python setup.py")
        return False
    
    # Check if we're in the virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("⚠️  Virtual environment not activated")
        return False

def activate_and_run():
    """Activate virtual environment and run the server"""
    # Change to python directory
    os.chdir("python")
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
        run_cmd = f"{activate_cmd} && python -m uvicorn app.service:app --host 0.0.0.0 --port 8000 --reload"
    else:
        activate_cmd = "source .venv/bin/activate"
        run_cmd = f"{activate_cmd} && python -m uvicorn app.service:app --host 0.0.0.0 --port 8000 --reload"
    
    print("🚀 Starting FastAPI server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📊 Health check: http://localhost:8000/health")
    print("📚 API docs: http://localhost:8000/docs")
    print("\n🔄 Server will auto-reload on file changes")
    print("⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(run_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError:
        print("\n❌ Server failed to start")
        print("Make sure all dependencies are installed: python setup.py")

def main():
    """Main function"""
    print("🐍 Trading MVP - FastAPI Development Server")
    print("=" * 45)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Check if model exists
        model_path = Path("python/model.pkl")
        if not model_path.exists():
            print("⚠️  ML model not found!")
            print("Train the model first:")
            if platform.system() == "Windows":
                print("   cd python && .venv\\Scripts\\activate")
            else:
                print("   cd python && source .venv/bin/activate")
            print("   python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1")
            print("\nContinuing anyway (predictions will use dummy data)...\n")
        
        activate_and_run()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
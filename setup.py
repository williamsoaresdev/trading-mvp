#!/usr/bin/env python3
"""
Trading MVP - Setup Script (Cross-platform)
This script sets up the entire project for first-time use
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_prerequisites():
    """Check if all required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    success, output = run_command("python --version", check=False)
    if not success:
        print("❌ Python not found. Please install Python 3.10+!")
        return False
    print(f"✅ Python found: {output.strip()}")
    
    # Check .NET
    success, output = run_command("dotnet --version", check=False)
    if not success:
        print("❌ .NET SDK not found. Please install .NET 8+!")
        return False
    print(f"✅ .NET found: {output.strip()}")
    
    # Check Node.js
    success, output = run_command("node --version", check=False)
    if not success:
        print("❌ Node.js not found. Please install Node.js 18+!")
        return False
    print(f"✅ Node.js found: {output.strip()}")
    
    print("✅ All prerequisites met!\n")
    return True

def setup_python_env():
    """Setup Python virtual environment and dependencies"""
    print("🐍 Setting up Python environment...")
    
    os.chdir("python")
    
    # Create virtual environment
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("📦 Creating Python virtual environment...")
        success, _ = run_command("python -m venv .venv")
        if not success:
            print("❌ Failed to create virtual environment!")
            return False
        print("✅ Virtual environment created!")
    else:
        print("⚠️  Virtual environment already exists!")
    
    # Install dependencies
    print("📦 Installing Python dependencies...")
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate && "
    else:
        activate_cmd = "source .venv/bin/activate && "
    
    # Upgrade pip and install requirements
    pip_cmd = f"{activate_cmd}python -m pip install --upgrade pip"
    success, _ = run_command(pip_cmd)
    if not success:
        print("❌ Failed to upgrade pip!")
        return False
    
    install_cmd = f"{activate_cmd}pip install -r requirements.txt"
    success, _ = run_command(install_cmd)
    if not success:
        print("❌ Failed to install Python dependencies!")
        return False
    
    print("✅ Python dependencies installed!")
    os.chdir("..")
    return True

def setup_angular_env():
    """Setup Angular environment and dependencies"""
    print("🅰️  Setting up Angular environment...")
    
    os.chdir("trading-dashboard")
    
    print("📦 Installing Angular dependencies...")
    success, _ = run_command("npm install")
    if not success:
        print("❌ Failed to install Angular dependencies!")
        return False
    
    print("✅ Angular dependencies installed!")
    os.chdir("..")
    return True

def build_dotnet_project():
    """Build the .NET project"""
    print("🔨 Building .NET project...")
    
    os.chdir("dotnet/TradingExecutor")
    
    success, output = run_command("dotnet build")
    if not success:
        print("❌ Failed to build .NET project!")
        print(output)
        return False
    
    print("✅ .NET project built successfully!")
    os.chdir("../..")
    return True

def print_next_steps():
    """Print instructions for running the system"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    
    if platform.system() == "Windows":
        print("1. Train the ML model:")
        print("   cd python && .venv\\Scripts\\activate")
        print("   python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1")
        print("\n2. Start the FastAPI server:")
        print("   python run_server.py")
        print("\n3. Start the Angular dashboard (new terminal):")
        print("   cd trading-dashboard && npm start")
        print("\n4. Start the .NET executor (new terminal):")
        print("   cd dotnet\\TradingExecutor && dotnet run")
    else:
        print("1. Train the ML model:")
        print("   cd python && source .venv/bin/activate")
        print("   python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1")
        print("\n2. Start the FastAPI server:")
        print("   python run_server.py")
        print("\n3. Start the Angular dashboard (new terminal):")
        print("   cd trading-dashboard && npm start")
        print("\n4. Start the .NET executor (new terminal):")
        print("   cd dotnet/TradingExecutor && dotnet run")
    
    print("\n🌐 Access URLs:")
    print("• Dashboard: http://localhost:4200")
    print("• API: http://localhost:8000")
    print("• API Health: http://localhost:8000/health")
    print("\n⚠️  Note: This runs in PAPER TRADING mode (safe)")

def main():
    """Main setup function"""
    print("🚀 Trading MVP - Setup Script (Cross-platform)")
    print("=" * 50)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Check prerequisites
        if not check_prerequisites():
            sys.exit(1)
        
        # Setup Python environment
        if not setup_python_env():
            sys.exit(1)
        
        # Setup Angular environment
        if not setup_angular_env():
            sys.exit(1)
        
        # Build .NET project
        if not build_dotnet_project():
            sys.exit(1)
        
        # Print next steps
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
@echo off
REM Trading MVP - Setup Script for Windows
REM This script sets up the entire project for first-time use

echo 🚀 Trading MVP - Setup Script (Windows)
echo ========================================

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+!
    pause
    exit /b 1
) else (
    echo [SUCCESS] Python found
)

REM Check .NET
dotnet --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] .NET SDK not found. Please install .NET 8+!
    pause
    exit /b 1
) else (
    echo [SUCCESS] .NET found
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+!
    pause
    exit /b 1
) else (
    echo [SUCCESS] Node.js found
)

echo [SUCCESS] All prerequisites met!
echo.

REM Setup Python environment
echo [INFO] Setting up Python environment...
cd python

REM Create virtual environment
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
    echo [SUCCESS] Virtual environment created!
) else (
    echo [WARNING] Virtual environment already exists!
)

REM Activate virtual environment and install dependencies
echo [INFO] Installing Python dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Python dependencies installed!

cd ..

REM Setup Angular environment
echo [INFO] Setting up Angular environment...
cd trading-dashboard

echo [INFO] Installing Angular dependencies...
npm install
echo [SUCCESS] Angular dependencies installed!

cd ..

REM Build .NET project
echo [INFO] Building .NET project...
cd dotnet\TradingExecutor

dotnet build
if %errorlevel% eq 0 (
    echo [SUCCESS] .NET project built successfully!
) else (
    echo [ERROR] Failed to build .NET project!
    pause
    exit /b 1
)

cd ..\..

REM Final setup message
echo.
echo [SUCCESS] 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Train the ML model:
echo    cd python ^&^& .venv\Scripts\activate
echo    python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1
echo.
echo 2. Start the FastAPI server:
echo    python run_server.py
echo.
echo 3. Start the Angular dashboard (new terminal):
echo    cd trading-dashboard ^&^& npm start
echo.
echo 4. Start the .NET executor (new terminal):
echo    cd dotnet\TradingExecutor ^&^& dotnet run
echo.
echo 🌐 Access URLs:
echo • Dashboard: http://localhost:4200
echo • API: http://localhost:8000
echo • API Health: http://localhost:8000/health
echo.
echo ⚠️  Note: This runs in PAPER TRADING mode (safe)
echo.
pause
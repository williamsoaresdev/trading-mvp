@echo off
REM Binance Integration Setup Script for Windows
REM Installs required dependencies and sets up environment

echo 🚀 Setting up Binance Integration...
echo ==================================

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed!
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ pip is not installed!
    pause
    exit /b 1
)

echo ✅ pip found
pip --version

REM Install required packages
echo.
echo 📦 Installing Python packages...
pip install python-binance python-dotenv ccxt pandas numpy

REM Check if packages were installed successfully
echo.
echo 🔍 Verifying installations...

python -c "import binance; print('✅ python-binance installed')" 2>nul || echo ❌ python-binance failed
python -c "import dotenv; print('✅ python-dotenv installed')" 2>nul || echo ❌ python-dotenv failed
python -c "import ccxt; print('✅ ccxt installed')" 2>nul || echo ❌ ccxt failed
python -c "import pandas; print('✅ pandas installed')" 2>nul || echo ❌ pandas failed
python -c "import numpy; print('✅ numpy installed')" 2>nul || echo ❌ numpy failed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created!
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your Binance API credentials!
    echo    1. Open .env file in your editor
    echo    2. Replace 'your_api_key_here' with your actual Binance API key
    echo    3. Replace 'your_secret_key_here' with your actual Binance secret key
    echo    4. Set BINANCE_TESTNET=true for safe testing
) else (
    echo.
    echo ✅ .env file already exists
)

echo.
echo ✅ Binance integration setup complete!
echo.
echo Next steps:
echo 1. Configure your .env file with Binance API credentials
echo 2. Test connection: python scripts/test_binance_integration.py
echo 3. Run trading: python scripts/run_realtime_trading.py
echo.
echo ⚠️  Remember: Start with TESTNET and small amounts!
echo.
pause
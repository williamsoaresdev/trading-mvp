#!/bin/bash

# Binance Integration Setup Script
# Installs required dependencies and sets up environment

echo "🚀 Setting up Binance Integration..."
echo "=================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed!"
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed!"
    exit 1
fi

echo "✅ pip found: $(pip --version)"

# Install required packages
echo ""
echo "📦 Installing Python packages..."
pip install python-binance python-dotenv ccxt pandas numpy

# Check if packages were installed successfully
echo ""
echo "🔍 Verifying installations..."

python -c "import binance; print('✅ python-binance installed')" 2>/dev/null || echo "❌ python-binance failed"
python -c "import dotenv; print('✅ python-dotenv installed')" 2>/dev/null || echo "❌ python-dotenv failed"
python -c "import ccxt; print('✅ ccxt installed')" 2>/dev/null || echo "❌ ccxt failed"
python -c "import pandas; print('✅ pandas installed')" 2>/dev/null || echo "❌ pandas failed"
python -c "import numpy; print('✅ numpy installed')" 2>/dev/null || echo "❌ numpy failed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your Binance API credentials!"
    echo "   1. Open .env file in your editor"
    echo "   2. Replace 'your_api_key_here' with your actual Binance API key"
    echo "   3. Replace 'your_secret_key_here' with your actual Binance secret key"
    echo "   4. Set BINANCE_TESTNET=true for safe testing"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Make Python scripts executable
echo ""
echo "🔧 Setting up script permissions..."
chmod +x scripts/*.py
chmod +x scripts/*.sh

echo ""
echo "✅ Binance integration setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with Binance API credentials"
echo "2. Test connection: python scripts/test_binance_integration.py"
echo "3. Run trading: python scripts/run_realtime_trading.py"
echo ""
echo "⚠️  Remember: Start with TESTNET and small amounts!"
#!/bin/bash

# Trading MVP - Setup Script
# This script sets up the entire project for first-time use

echo "🚀 Trading MVP - Setup Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.10+!"
    exit 1
fi

# Check .NET
if command -v dotnet &> /dev/null; then
    DOTNET_VERSION=$(dotnet --version)
    print_success ".NET found: $DOTNET_VERSION"
else
    print_error ".NET SDK not found. Please install .NET 8+!"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found. Please install Node.js 18+!"
    exit 1
fi

print_success "All prerequisites met!"
echo ""

# Setup Python environment
print_status "Setting up Python environment..."
cd python

# Create virtual environment
if [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created!"
else
    print_warning "Virtual environment already exists!"
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
source .venv/bin/activate  # Linux/Mac
# For Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed!"

cd ..

# Setup Angular environment  
print_status "Setting up Angular environment..."
cd trading-dashboard

print_status "Installing Angular dependencies..."
npm install
print_success "Angular dependencies installed!"

cd ..

# Build .NET project
print_status "Building .NET project..."
cd dotnet/TradingExecutor

dotnet build
if [ $? -eq 0 ]; then
    print_success ".NET project built successfully!"
else
    print_error "Failed to build .NET project!"
    exit 1
fi

cd ../..

# Final setup message
echo ""
print_success "🎉 Setup completed successfully!"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Train the ML model:"
echo "   cd python && source .venv/bin/activate"  
echo "   python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1"
echo ""
echo "2. Start the FastAPI server:"
echo "   python run_server.py"
echo ""
echo "3. Start the Angular dashboard (new terminal):"
echo "   cd trading-dashboard && npm start"
echo ""
echo "4. Start the .NET executor (new terminal):"
echo "   cd dotnet/TradingExecutor && dotnet run"
echo ""
echo -e "${GREEN}🌐 Access URLs:${NC}"
echo "• Dashboard: http://localhost:4200"
echo "• API: http://localhost:8000"
echo "• API Health: http://localhost:8000/health"
echo ""
echo -e "${YELLOW}⚠️  Note: This runs in PAPER TRADING mode (safe)${NC}"
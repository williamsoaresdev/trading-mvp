# Trading MVP - System Requirements

## Software Requirements

### Python
- Version: 3.10 or higher (recommended: 3.11)
- Avoid: Python 3.12 (known stability issues with some libraries)

### .NET
- Version: .NET 8 SDK or higher

### Node.js  
- Version: 18+ 
- Package Manager: npm (included with Node.js)

## Hardware Requirements

### Minimum
- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Storage: 2 GB free space
- Network: Stable internet connection

### Recommended  
- CPU: 4+ cores, 2.5+ GHz
- RAM: 8+ GB  
- Storage: 10+ GB free space (for historical data)
- Network: Low-latency internet for real-time trading

## Operating System Support

- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu 20.04+
- ✅ Other Linux distributions (with manual setup)

## Network Requirements

### API Access
- Binance API (public endpoints): No authentication required for market data
- Binance API (trading): API key/secret required for real trading

### Ports Used
- `8000`: FastAPI server
- `4200`: Angular development server
- `3000-3999`: Additional development ports (if needed)

## Browser Support (for Dashboard)

- ✅ Chrome 90+
- ✅ Firefox 90+  
- ✅ Safari 14+
- ✅ Edge 90+

## Development Tools (Optional)

- **IDE**: VS Code, PyCharm, Visual Studio, WebStorm
- **Git**: For version control
- **Docker**: For containerized deployment (future)
- **Postman**: For API testing
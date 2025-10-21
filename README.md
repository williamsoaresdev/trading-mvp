# 🚀 Algorithmic Trading MVP - Clean Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)
[![Angular](https://img.shields.io/badge/Angular-20+-red.svg)](https://angular.io/)
[![Clean Architecture](https://img.shields.io/badge/Clean-Architecture-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![SOLID](https://img.shields.io/badge/SOLID-Principles-orange.svg)](https://en.wikipedia.org/wiki/SOLID)

A complete **real-time algorithmic trading system** featuring **Clean Architecture**, **SOLID principles**, **machine learning predictions**, **WebSocket streaming**, **automated trading execution**, and **live monitoring dashboard**.

This MVP implements a complete automated trading system following **Clean Architecture** and **Clean Code** patterns, with **machine learning**, **real-time automated execution**, **WebSocket for data streaming**, and **live monitoring dashboard**.

## 🏛️ Clean Architecture Implementation

The system has been completely refactored following **Clean Architecture** and **SOLID** principles, ensuring high quality, testability, and code maintainability.

### ✅ **SOLID Principles Implemented:**
- **🔹 Single Responsibility**: Each class has a single, well-defined responsibility
- **🔹 Open/Closed**: Open for extension, closed for modification
- **🔹 Liskov Substitution**: Interfaces implemented correctly
- **🔹 Interface Segregation**: Small and focused interfaces
- **🔹 Dependency Inversion**: Dependencies abstracted by interfaces

### 🏗️ **Layered Structure:**

#### **📦 Domain Layer** (Business Core)
- **Entities**: `TradingDecision`, `TradingSession`
- **Value Objects**: `TradingSymbol`, `Money`, `Percentage`, `TradingAction`
- **Repository Interfaces**: Abstractions for persistence
- **Zero external dependencies**

#### **⚙️ Application Layer** (Use Cases)
- **Use Cases**: `GenerateTradingDecisionUseCase`, `StartTradingSessionUseCase`
- **Application Services**: Business logic orchestration
- **Dependency Injection**: Control inversion
- **Depends only on Domain Layer**

#### **🏗️ Infrastructure Layer** (Technical Implementations)
- **Repositories**: `InMemoryTradingDecisionRepository`
- **External Services**: `CCXTMarketDataRepository`, `MLPredictionService`
- **Data Persistence**: Concrete implementations
- **External APIs**: Binance, WebSocket, HTTP clients

#### **🖥️ Presentation Layer** (Interface/API)
- **FastAPI**: Clean RESTful endpoints
- **WebSocket**: Real-time communication
- **Controllers**: Thin controllers delegating to use cases
- **DTOs**: Data transfer objects

### 🎯 **Benefits Achieved:**

**✅ Testability:**
- Dependencies can be easily mocked
- Isolated unit tests per layer
- Comprehensive test coverage

**✅ Maintainability:**
- Clear separation of concerns
- Changes isolated to specific layers
- Self-documenting code

**✅ Flexibility:**
- Easy switching of implementations (database, APIs)
- Adding new features without breaking existing code
- Support for multiple trading strategies

**✅ Scalability:**
- Structure ready for microservices
- Patterns that support growth
- Low coupling between components

## 🏗️ Architecture - Clean Architecture

### **Python** (Clean Architecture Implementation)

#### **📦 Domain Layer** (`trading-intelligence/app/domain/`)
```
domain/
├── entities/
│   ├── trading_decision.py    # Main decision entity
│   └── trading_session.py     # Trading session
├── value_objects/
│   ├── symbol.py              # Trading symbol (BTC/USDT)
│   ├── money.py               # Monetary value with validation
│   ├── percentage.py          # Percentage with business rules
│   └── trading_action.py      # Trading action (BUY/SELL/FLAT)
└── repositories/
    ├── trading_decision_repository.py    # Repository interface
    └── market_data_repository.py         # Market data interface
```

#### **⚙️ Application Layer** (`trading-intelligence/app/application/`)
```
application/
├── use_cases/
│   ├── generate_trading_decision.py    # UC: Generate trading decision
│   ├── start_trading_session.py       # UC: Start session
│   └── stop_trading_session.py        # UC: Stop session
└── services/
    └── clean_trading_service.py        # Main application service
```

#### **🏗️ Infrastructure Layer** (`trading-intelligence/app/infrastructure/`)
```
infrastructure/
├── repositories/
│   └── in_memory_decision_repository.py    # In-memory implementation
├── external/
│   └── ccxt_market_data.py                 # Data via CCXT/Binance
├── ml/
│   └── ml_prediction_service.py            # ML service
└── persistence/
    └── file_system.py                      # File persistence
```

#### **🖥️ Presentation Layer** (`trading-intelligence/app/presentation/`)
```
presentation/
├── api/
│   ├── trading_controller.py              # REST controller
│   └── websocket_handler.py               # WebSocket handler
├── dto/
│   ├── trading_request.py                 # Request DTOs
│   └── trading_response.py                # Response DTOs
└── main.py                                # Main FastAPI app
```

### **.NET** (Clean Architecture Implementation)

#### **📦 Domain Layer** (`trading-executor/Domain/`)
```csharp
// Domain Models (Immutable records)
public record TradingDecision(Symbol Symbol, TradingAction Action, decimal Confidence);
public record OrderResult(bool Success, string Message, decimal ExecutedPrice);

// Value Objects
public record Symbol(string Value);
public record Money(decimal Amount, string Currency);
```

#### **⚙️ Application Layer** (`trading-executor/Application/`)
```csharp
// Application Services
public interface ITradingApplicationService
{
    Task<OrderResult> ExecuteDecisionAsync(TradingDecision decision);
}

// Use Cases
public class ExecuteTradingDecisionUseCase
{
    private readonly ITradingExecutor _executor;
    private readonly IRiskManager _riskManager;
}
```

#### **🏗️ Infrastructure Layer** (`trading-executor/Infrastructure/`)
```csharp
// WebSocket Client
public class WebSocketTradingClient : ITradingDataSource
{
    public async Task<TradingDecision> ReceiveDecisionAsync();
}

// Order Execution
public class MockOrderExecutor : ITradingExecutor
{
    public async Task<OrderResult> ExecuteOrderAsync(TradingOrder order);
}
```

### **Angular** (Clean Frontend Architecture)
- `trading-dashboard/`: projeto Angular 20+ com **dashboard em tempo real**
- **Componentes**: estatísticas ao vivo, tabela de decisões streaming, gráficos dinâmicos
- **Serviços**: **WebSocket connection** para updates instantâneos + polling de backup
- **UI moderna**: gradientes, animações, códigos de cores, indicadores de status de conexão

### **Config**
- `config/config.yaml`: parameters (symbol, timeframe, thresholds, sizing, stops).

## 🚀 Prerequisites

- **Python 3.10+** (tested with Python 3.13)
- **.NET 8 SDK** or higher (tested with .NET 9.0)  
- **Node.js 18+** and npm for Angular dashboard
- Account/exchange for *live* data (Binance — public endpoints sufficient for data; for real orders, insert keys)

## ⚡ Quick Start - Real-Time System

### **🔥 Recommended Mode: Complete Real-Time System**

**1. Start Python API (Terminal 1):**
```bash
cd trading-intelligence
python app/simple_realtime.py
```

**2. Start .NET Executor (Terminal 2):**
```bash
cd trading-executor
dotnet run
```

**3. Start Angular Dashboard (Terminal 3):**
```bash
cd trading-dashboard
npm start
```

### **🎯 What happens:**
- ✅ **Python API**: Runs on port 8000 with WebSocket
- ✅ **Automatic decisions**: Every 30-60 seconds  
- ✅ **.NET Executor**: Connects via WebSocket and executes orders
- ✅ **Angular Dashboard**: Real-time updates on port 4200
- ✅ **WebSocket streaming**: Bidirectional communication between services
- ✅ **Detailed logs**: Follow each decision and execution

### **🌐 Access URLs:**
- **Dashboard**: http://localhost:4200 (live updates)
- **API Health**: http://localhost:8000/health  
- **Trading Status**: http://localhost:8000/trading/status
- **WebSocket**: ws://localhost:8000/ws

### **🛠️ Alternative Setup (First Time)**

**Windows:**
```cmd
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Cross-platform (Python):**
```bash
python setup.py
```

### **📚 Setup Manual (Opcional)**

**Prepare Environment** (first time):
```bash
cd trading-intelligence

2. **Train ML Model** (first time):
```bash
cd python
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1
```

3. **Traditional Mode** (without WebSocket):

Terminal 1 - FastAPI Server:
```bash
python run_server.py
```

Terminal 2 - Angular Dashboard:
```bash
cd trading-dashboard
npm start
```

Terminal 3 - .NET Trading Executor:
```bash
cd trading-executor
dotnet run
```

## 📊 **Dashboard Features - Real-Time**

- **📈 Live Statistics**
  - Total decisions (BUY/SELL/FLAT) in real-time
  - Distribution percentages automatically updated
  - Current BTC price via WebSocket
  - Average confidence level of decisions

- **📋 Streaming Decision Table**
  - Real-time decision stream via WebSocket
  - Last 100 decisions with precise timestamps
  - Instant buy/sell probabilities
  - Dynamic visual confidence bar
  - Order execution status

- **🔄 Real-Time Connectivity**
  - **WebSocket connection** for instant updates
  - Connection status indicator (Online/Offline)
  - Automatic fallback to HTTP polling
  - Manual reconnection button
  - Real-time latency display

- **⚡ System Monitoring**
  - Service status (API, Executor, Dashboard)
  - Number of active WebSocket connections
  - System health indicators
  - Real-time execution logs

## 🌐 **Access URLs - Complete System**

- **🖥️ Angular Dashboard**: http://localhost:4200 (live updates via WebSocket)
- **🔗 FastAPI API**: http://localhost:8000  
- **📊 API Health**: http://localhost:8000/health
- **📈 Trading Status**: http://localhost:8000/trading/status
- **📋 Trading History**: http://localhost:8000/trading/history
- **🔌 WebSocket Endpoint**: ws://localhost:8000/ws
- **🤖 Manual Prediction**: http://localhost:8000/predict?symbol=BTC/USDT&timeframe=1h
- **▶️ Start Trading**: POST http://localhost:8000/trading/start
- **⏹️ Stop Trading**: POST http://localhost:8000/trading/stop

## 📁 **Project Structure - Clean Architecture**

```
trading-mvp/
├── 📁 docs/                            # 📚 Project Documentation
│   ├── SETUP_GUIDE.md                    # Step-by-step setup guide
│   ├── REFACTORING_LOG.md                # Refactoring history
│   └── REQUIREMENTS.md                   # Requirements documentation
├── 📁 scripts/                         # 🔧 Build & Setup Scripts
│   ├── setup.py                          # Cross-platform setup
│   ├── setup.sh                          # Linux/macOS setup
│   ├── setup.bat                         # Windows setup
│   ├── run_server.py                     # Start API server
│   ├── run_realtime.py                   # Start real-time service
│   ├── start_api.py                      # Legacy API starter
│   └── start_clean_api.py                # Clean API starter
├── 📁 tests/                           # 🧪 Test Suite
│   ├── test_clean_architecture.py        # Clean Architecture tests
│   ├── test_complete_system.py           # End-to-end tests
│   └── test_results_summary.py           # Test results summary
├── 📁 tools/                           # 🛠️ Development Tools
│   ├── code_analysis.py                  # Code quality analyzer
│   ├── quality_report.py                 # Quality report generator
│   ├── final_structure.py               # Structure documentation
│   └── verify_structure.py               # Structure verification
├── 📁 config/                          # ⚙️ Configuration Files
│   └── config.yaml                       # Main configuration
├── 📁 trading-intelligence/            # 🧠 Clean Architecture Python Backend
│   ├── 📁 app/
│   │   ├── 📁 domain/                  # 📦 DOMAIN LAYER
│   │   │   ├── 📁 entities/
│   │   │   │   ├── trading_decision.py    # Main entity
│   │   │   │   └── trading_session.py     # Trading session
│   │   │   ├── 📁 value_objects/
│   │   │   │   ├── symbol.py              # Symbol (BTC/USDT)
│   │   │   │   ├── money.py               # Monetary value
│   │   │   │   ├── percentage.py          # Percentage
│   │   │   │   └── trading_action.py      # Action (BUY/SELL/FLAT)
│   │   │   └── 📁 repositories/
│   │   │       ├── trading_decision_repository.py
│   │   │       └── market_data_repository.py
│   │   ├── 📁 application/             # ⚙️ APPLICATION LAYER
│   │   │   ├── 📁 use_cases/
│   │   │   │   ├── generate_trading_decision.py
│   │   │   │   ├── start_trading_session.py
│   │   │   │   └── stop_trading_session.py
│   │   │   └── 📁 services/
│   │   │       └── clean_trading_service.py
│   │   ├── 📁 infrastructure/          # 🏗️ INFRASTRUCTURE LAYER
│   │   │   ├── 📁 repositories/
│   │   │   │   └── in_memory_decision_repository.py
│   │   │   ├── 📁 external/
│   │   │   │   └── ccxt_market_data.py
│   │   │   ├── 📁 ml/
│   │   │   │   └── ml_prediction_service.py
│   │   │   └── 📁 persistence/
│   │   │       └── file_system.py
│   │   ├── 📁 presentation/            # 🖥️ PRESENTATION LAYER
│   │   │   ├── 📁 api/
│   │   │   │   ├── trading_controller.py
│   │   │   │   └── websocket_handler.py
│   │   │   ├── 📁 dto/
│   │   │   │   ├── trading_request.py
│   │   │   │   └── trading_response.py
│   │   │   └── main.py                    # FastAPI app
│   │   ├── model_train.py              # 🧠 ML Training (legacy)
│   │   ├── service.py                  # 🔄 Legacy API
│   │   ├── simple_realtime.py          # ⚡ Real-time service
│   │   └── utils.py                    # 🛠️ Utilities
│   ├── 📁 artifacts/                   # Modelo treinado (git ignored)
│   ├── requirements.txt                # Dependências Python
│   └── run_server.py                  # Script para subir API
├── 📁 trading-executor/                 # Clean Architecture .NET Backend
│   ├── 📁 Domain/                      # 📦 DOMAIN LAYER
│   │   ├── Models/                        # Domain models (records)
│   │   ├── ValueObjects/                  # Value objects
│   │   └── Interfaces/                    # Domain interfaces
│   ├── 📁 Application/                 # ⚙️ APPLICATION LAYER
│   │   ├── Services/                      # Application services
│   │   ├── UseCases/                      # Use cases
│   │   └── Interfaces/                    # Application interfaces
│   ├── 📁 Infrastructure/              # 🏗️ INFRASTRUCTURE LAYER
│   │   ├── WebSocket/                     # WebSocket client
│   │   ├── OrderExecution/                # Order execution
│   │   ├── RiskManagement/                # Risk management
│   │   └── Logging/                       # Logging infrastructure
│   ├── Program.cs                      # 🚀 Main entry point
│   ├── OrderExecution.cs              # 📋 Order execution (legacy)
│   └── *.csproj                       # Projeto .NET com DI
├── 📁 trading-dashboard/               # Angular Frontend (Clean Frontend)
│   ├── 📁 src/app/
│   │   ├── 📁 components/              # UI Components
│   │   ├── 📁 services/                # � WebSocket + HTTP services
│   │   ├── 📁 models/                  # TypeScript interfaces
│   │   └── 📁 shared/                  # Shared utilities
│   └── package.json                   # Dependências NPM
├── 📁 config/                         # Configurações
│   └── config.yaml                    # Parâmetros de trading
├── 📁 tests/                          # 🧪 Test Suite
│   ├── test_clean_architecture.py     # Testes da Clean Architecture
│   ├── test_results_summary.py        # Resumo dos testes
│   └── unit_tests/                    # Testes unitários por camada
├── run_realtime.py                    # 🔥 Script para sistema completo
├── start_api.py                       # Script simplificado para API
├── setup.bat / setup.sh               # Scripts de instalação
├── .gitignore                         # Arquivos ignorados
└── README.md                          # 📖 Esta documentação
```

### 🎯 **Camadas e Dependências:**

```
🖥️ Presentation Layer
    ⬇️ (depende de)
⚙️ Application Layer
    ⬇️ (depende de)
📦 Domain Layer (sem dependências)
    ⬆️ (implementado por)
🏗️ Infrastructure Layer
```

**📝 Regras de Dependência:**
- ✅ **Domain Layer**: Zero dependências externas
- ✅ **Application Layer**: Depende apenas do Domain
- ✅ **Infrastructure Layer**: Implementa interfaces do Domain
- ✅ **Presentation Layer**: Coordena Application e Infrastructure
- ✅ **Dependency Injection**: Injeta Infrastructure no Application

## ⚙️ **Configuration (config.yaml)**

```yaml
symbol: "BTC/USDT"
timeframe: "1h" 
years: 1

# Decision thresholds
proba_buy_threshold: 0.58
proba_sell_threshold: 0.58

# Risk & sizing
vol_target_annual: 0.20        # 20% volatilidade anual
max_position_fraction: 0.30    # 30% max do capital
min_position_fraction: 0.02    # 2% min do capital

# Stops (em ATR)
stop_atr_mult: 1.2
take_atr_mult: 2.0

# Circuit breakers  
daily_loss_limit_frac: 0.04    # 4% perda diária máxima
```

### **🧪 Testes da Clean Architecture**

O projeto inclui uma suíte abrangente de testes para validar todos os componentes da Clean Architecture:

```bash
# Executar todos os testes da Clean Architecture
python test_clean_architecture.py

# Ver resumo detalhado dos resultados
python test_results_summary.py
```

**✅ Cobertura de Testes:**
- **Domain Layer**: Value Objects, Entities, Repository interfaces
- **Application Layer**: Use Cases, Application Services
- **Infrastructure Layer**: Repository implementations, External services
- **Integration Tests**: Comunicação entre camadas
- **SOLID Principles**: Validação dos princípios aplicados

## 🛡️ **Segurança & Produção**

### **⚠️ Paper Trading (Atual)**
- Todas as ordens são **MOCK** por segurança
- Nenhuma ordem real é executada
- Perfeito para testes e validação

### **🔄 Para Produção (Opcional)**
```csharp
// 1. Implementar BinanceSpotOrderExecutor em OrderExecution.cs
// 2. Adicionar suas credenciais da Binance
// 3. Uncomment real execution lines
// 4. Iniciar com capital pequeno (< $100)
// 5. Monitorar 24/7 nos primeiros dias
```

### **📈 Métricas de Performance**
- **Accuracy direcional**: 63.7% (resultado do treinamento)
- **Win rate**: calculado em tempo real no dashboard
- **Max drawdown**: monitorado via circuit breakers
- **Sharpe ratio**: implementar em versões futuras

## 🔧 **Troubleshooting**

### **🔌 WebSocket: Connection Issues**
```bash
# Verificar se API está rodando com WebSocket
curl http://localhost:8000/health

# Testar WebSocket diretamente  
wscat -c ws://localhost:8000/ws

# Verificar portas em uso
netstat -an | findstr :8000
```

### **🐍 Python: ModuleNotFoundError**
```bash
# Certificar que venv está ativo
which python  # deve apontar para .venv

# Para Python 3.13+ (dependências flexíveis)
pip install -r requirements.txt --force-reinstall
```

### **⚡ .NET: Connection refused**
```bash
# Verificar se FastAPI está rodando
curl http://localhost:8000/trading/status

# Restart com logs detalhados
cd trading-executor
dotnet run --verbosity detailed
```

### **🅰️ Angular: Build errors**
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install

# Verificar versões
node --version  # deve ser 18+
npm --version
```

### **🔄 Sistema Completo: Services não comunicam**
```bash
# 1. Verificar ordem de inicialização:
# Primeiro: Python API (porta 8000)
# Segundo: .NET Executor (conecta via WebSocket)  
# Terceiro: Angular Dashboard (porta 4200)

# 2. Verificar conectividade
curl http://localhost:8000/trading/status
curl http://localhost:4200

# 3. Logs detalhados em cada terminal
# Python: logs automáticos no console
# .NET: logs automáticos no console  
# Angular: F12 > Console para logs do browser
```

## 🚀 **Roadmap & Melhorias**

### **✅ Recursos Implementados**
- [x] **Sistema de Trading em Tempo Real** com WebSocket
- [x] **Conectividade bidirecional** entre todos os serviços
- [x] **Dashboard responsivo** com updates instantâneos
- [x] **Executor .NET** com cliente WebSocket robusto
- [x] **Risk management** integrado com circuit breakers
- [x] **Detailed logs** for complete monitoring
- [x] **Fallback automático** HTTP quando WebSocket falha
- [x] **Mock orders** para testing seguro
- [x] **Status monitoring** em tempo real

### **✅ Clean Architecture Implementada**
- [x] **Domain Layer** com Entities e Value Objects
- [x] **Application Layer** com Use Cases e Services
- [x] **Infrastructure Layer** com Repositories e External Services
- [x] **Presentation Layer** com Controllers e DTOs
- [x] **Dependency Injection** implementado em Python e .NET
- [x] **SOLID Principles** aplicados em todo o codebase
- [x] **Interface Segregation** com contratos bem definidos
- [x] **Dependency Inversion** com abstrações apropriadas
- [x] **Single Responsibility** em todas as classes
- [x] **Open/Closed Principle** para extensibilidade
- [x] **Clean Code Standards** aplicados
- [x] **Test Suite abrangente** validando todas as camadas
- [x] **Centralized Error Handling** and structured logging
- [x] **Configuration Management** desacoplado
- [x] **Async/Await patterns** implementados corretamente

### **🎯 Próximas Features - Baseadas em Clean Architecture**
- [ ] **Domain Events** para comunicação assíncrona entre agregados
- [ ] **CQRS Pattern** para separação de comandos e consultas
- [ ] **Event Sourcing** para auditoria completa de decisões
- [ ] **Hexagonal Architecture** ports and adapters refinement
- [ ] **DDD Bounded Contexts** para múltiplas estratégias
- [ ] **Microservices Architecture** baseada nos domínios
- [ ] **Repository Pattern** com Entity Framework ou SQLAlchemy
- [ ] **Unit of Work Pattern** para transações atômicas
- [ ] **Specification Pattern** para regras de negócio complexas
- [ ] **Factory Pattern** para criação de estratégias dinâmicas

### **📊 Analytics Planejadas**
- [ ] **Heatmap de performance** por hora/dia/semana
- [ ] **Correlação** entre volatilidade e accuracy  
- [ ] **Métricas de Sharpe** e maximum drawdown
- [ ] **Monte Carlo** para stress testing
- [ ] **A/B testing** de diferentes estratégias
- [ ] **Machine learning** para otimização de parâmetros

### **🔒 Segurança & Produção**
- [ ] **Rate limiting** para API endpoints
- [ ] **Autenticação JWT** para dashboard
- [ ] **SSL/TLS** para conexões seguras
- [ ] **Kubernetes deployment** para escalabilidade
- [ ] **Monitoring avançado** com Prometheus/Grafana
- [ ] **Backup automático** de decisões e logs

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**⚠️ DISCLAIMER**: This is an educational project focused on **Clean Architecture**, **SOLID principles**, **real-time systems** and **WebSocket streaming**. The system demonstrates how to implement clean architecture in an automated trading context. Automated trading involves significant financial risks. Use only capital you can afford to lose. The current system uses **mock orders** for safety. We are not responsible for financial losses.

**🏛️ ARCHITECTURAL HIGHLIGHT**: Complete system implementing **Clean Architecture** with **Domain-Driven Design**, **SOLID principles**, **Dependency Injection**, **Use Cases pattern**, **Repository pattern**, **Value Objects**, and **Entity pattern** - **100% tested and working!**

**🔥 TECHNICAL HIGHLIGHT**: Complete **real-time trading system** with **WebSocket communication** between Python, .NET and Angular following **Clean Architecture** - **production architecture!**

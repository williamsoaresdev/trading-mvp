# 🚀 Algorithmic Trading MVP - Clean Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)
[![Angular](https://img.shields.io/badge/Angular-20+-red.svg)](https://angular.io/)
[![Clean Architecture](https://img.shields.io/badge/Clean-Architecture-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![SOLID](https://img.shields.io/badge/SOLID-Principles-orange.svg)](https://en.wikipedia.org/wiki/SOLID)

A complete **real-time algorithmic trading system** featuring **Clean Architecture**, **SOLID principles**, **machine learning predictions**, **WebSocket streaming**, **automated trading execution**, and **live monitoring dashboard**.

Este MVP implementa um sistema completo de trading automatizado seguindo os padrões de **Clean Architecture** e **Clean Code**, com **machine learning**, **execução automática em tempo real**, **WebSocket para streaming de dados**, e **dashboard de monitoramento ao vivo**.

## 🏛️ Clean Architecture Implementation

O sistema foi completamente refatorado seguindo os princípios da **Clean Architecture** e **SOLID**, garantindo alta qualidade, testabilidade e manutenibilidade do código.

### ✅ **Princípios SOLID Implementados:**
- **🔹 Single Responsibility**: Cada classe tem uma única responsabilidade bem definida
- **🔹 Open/Closed**: Aberto para extensão, fechado para modificação
- **🔹 Liskov Substitution**: Interfaces implementadas corretamente
- **🔹 Interface Segregation**: Interfaces pequenas e focadas
- **🔹 Dependency Inversion**: Dependências abstraídas por interfaces

### 🏗️ **Estrutura em Camadas:**

#### **📦 Domain Layer** (Núcleo do Negócio)
- **Entities**: `TradingDecision`, `TradingSession`
- **Value Objects**: `TradingSymbol`, `Money`, `Percentage`, `TradingAction`
- **Repository Interfaces**: Abstrações para persistência
- **Zero dependências externas**

#### **⚙️ Application Layer** (Casos de Uso)
- **Use Cases**: `GenerateTradingDecisionUseCase`, `StartTradingSessionUseCase`
- **Application Services**: Orquestração da lógica de negócio
- **Dependency Injection**: Inversão de controle
- **Depende apenas do Domain Layer**

#### **🏗️ Infrastructure Layer** (Implementações Técnicas)
- **Repositories**: `InMemoryTradingDecisionRepository`
- **External Services**: `CCXTMarketDataRepository`, `MLPredictionService`
- **Data Persistence**: Implementações concretas
- **APIs Externas**: Binance, WebSocket, HTTP clients

#### **🖥️ Presentation Layer** (Interface/API)
- **FastAPI**: Endpoints RESTful limpos
- **WebSocket**: Comunicação em tempo real
- **Controllers**: Thin controllers delegando para use cases
- **DTOs**: Objetos de transferência de dados

### 🎯 **Benefícios Alcançados:**

**✅ Testabilidade:**
- Dependencies podem ser facilmente mockadas
- Testes unitários isolados por camada
- Cobertura de testes abrangente

**✅ Manutenibilidade:**
- Separação clara de responsabilidades
- Mudanças isoladas em camadas específicas
- Código autodocumentado

**✅ Flexibilidade:**
- Fácil troca de implementações (banco de dados, APIs)
- Adição de novas features sem quebrar código existente
- Suporte a múltiplas estratégias de trading

**✅ Escalabilidade:**
- Estrutura preparada para microserviços
- Padrões que suportam crescimento
- Baixo acoplamento entre componentes

## 🏗️ Arquitetura - Clean Architecture

### **Python** (Clean Architecture Implementation)

#### **📦 Domain Layer** (`python/app/domain/`)
```
domain/
├── entities/
│   ├── trading_decision.py    # Entidade principal de decisão
│   └── trading_session.py     # Sessão de trading
├── value_objects/
│   ├── symbol.py              # Símbolo de trading (BTC/USDT)
│   ├── money.py               # Valor monetário com validação
│   ├── percentage.py          # Porcentagem com regras de negócio
│   └── trading_action.py      # Ação de trading (BUY/SELL/FLAT)
└── repositories/
    ├── trading_decision_repository.py    # Interface de repositório
    └── market_data_repository.py         # Interface de dados de mercado
```

#### **⚙️ Application Layer** (`python/app/application/`)
```
application/
├── use_cases/
│   ├── generate_trading_decision.py    # UC: Gerar decisão de trading
│   ├── start_trading_session.py       # UC: Iniciar sessão
│   └── stop_trading_session.py        # UC: Parar sessão
└── services/
    └── clean_trading_service.py        # Serviço de aplicação principal
```

#### **🏗️ Infrastructure Layer** (`python/app/infrastructure/`)
```
infrastructure/
├── repositories/
│   └── in_memory_decision_repository.py    # Implementação em memória
├── external/
│   └── ccxt_market_data.py                 # Dados via CCXT/Binance
├── ml/
│   └── ml_prediction_service.py            # Serviço de ML
└── persistence/
    └── file_system.py                      # Persistência em arquivo
```

#### **🖥️ Presentation Layer** (`python/app/presentation/`)
```
presentation/
├── api/
│   ├── trading_controller.py              # Controller REST
│   └── websocket_handler.py               # Handler WebSocket
├── dto/
│   ├── trading_request.py                 # DTOs de request
│   └── trading_response.py                # DTOs de response
└── main.py                                # FastAPI app principal
```

### **.NET** (Clean Architecture Implementation)

#### **📦 Domain Layer** (`dotnet/TradingExecutor/Domain/`)
```csharp
// Domain Models (Records imutáveis)
public record TradingDecision(Symbol Symbol, TradingAction Action, decimal Confidence);
public record OrderResult(bool Success, string Message, decimal ExecutedPrice);

// Value Objects
public record Symbol(string Value);
public record Money(decimal Amount, string Currency);
```

#### **⚙️ Application Layer** (`dotnet/TradingExecutor/Application/`)
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

#### **🏗️ Infrastructure Layer** (`dotnet/TradingExecutor/Infrastructure/`)
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
- `config/config.yaml`: parâmetros (símbolo, timeframe, limiares, sizing, stops).

## 🚀 Pré-requisitos

- **Python 3.10+** (testado com Python 3.13)
- **.NET 8 SDK** ou superior (testado com .NET 9.0)  
- **Node.js 18+** e npm para o dashboard Angular
- Conta/exchange para dados *live* (Binance — endpoints públicos bastam para dados; para ordens reais, inserir keys)

## ⚡ Quick Start - Real-Time System

### **🔥 Modo Recomendado: Sistema Completo em Tempo Real**

**1. Inicie a API Python (Terminal 1):**
```bash
cd python
python app/simple_realtime.py
```

**2. Inicie o Executor .NET (Terminal 2):**
```bash
cd dotnet/TradingExecutor
dotnet run
```

**3. Inicie o Dashboard Angular (Terminal 3):**
```bash
cd trading-dashboard
npm start
```

### **🎯 O que acontece:**
- ✅ **API Python**: Roda na porta 8000 com WebSocket
- ✅ **Decisões automáticas**: A cada 30-60 segundos  
- ✅ **Executor .NET**: Conecta via WebSocket e executa ordens
- ✅ **Dashboard Angular**: Updates em tempo real na porta 4200
- ✅ **WebSocket streaming**: Comunicação bidirecional entre serviços
- ✅ **Logs detalhados**: Acompanhe cada decisão e execução

### **🌐 URLs de Acesso:**
- **Dashboard**: http://localhost:4200 (updates ao vivo)
- **API Health**: http://localhost:8000/health  
- **Trading Status**: http://localhost:8000/trading/status
- **WebSocket**: ws://localhost:8000/ws

### **🛠️ Setup Alternativo (Primeira Vez)**

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

1. **Preparar Ambiente** (primeira vez):
```bash
# Linux/macOS
./setup.sh

# Windows
setup.bat

# Cross-platform
python setup.py
```

2. **Treinar Modelo ML** (primeira vez):
```bash
cd python
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1
```

3. **Modo Tradicional** (sem WebSocket):

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
cd dotnet/TradingExecutor
dotnet run
```

## 📊 **Dashboard Features - Real-Time**

- **📈 Estatísticas Ao Vivo**
  - Total de decisões (BUY/SELL/FLAT) em tempo real
  - Percentuais de distribuição atualizados automaticamente
  - Preço atual do BTC via WebSocket
  - Nível de confiança médio das decisões

- **📋 Tabela de Decisões Streaming**
  - Stream de decisões em tempo real via WebSocket
  - Últimas 100 decisões com timestamps precisos
  - Probabilidades de compra/venda instantâneas
  - Barra de confiança visual dinâmica
  - Status de execução das ordens

- **🔄 Conectividade Tempo Real**
  - **WebSocket connection** para updates instantâneos
  - Indicador de status da conexão (Online/Offline)
  - Fallback automático para polling HTTP
  - Botão de reconexão manual
  - Latência exibida em tempo real

- **⚡ Monitoramento de Sistema**
  - Status dos serviços (API, Executor, Dashboard)
  - Número de conexões WebSocket ativas
  - Indicadores de saúde do sistema
  - Logs de execução em tempo real

## 🌐 **URLs de Acesso - Sistema Completo**

- **🖥️ Dashboard Angular**: http://localhost:4200 (live updates via WebSocket)
- **🔗 API FastAPI**: http://localhost:8000  
- **📊 API Health**: http://localhost:8000/health
- **📈 Trading Status**: http://localhost:8000/trading/status
- **📋 Trading History**: http://localhost:8000/trading/history
- **🔌 WebSocket Endpoint**: ws://localhost:8000/ws
- **🤖 Manual Prediction**: http://localhost:8000/predict?symbol=BTC/USDT&timeframe=1h
- **▶️ Start Trading**: POST http://localhost:8000/trading/start
- **⏹️ Stop Trading**: POST http://localhost:8000/trading/stop

## 📁 **Estrutura do Projeto - Clean Architecture**

```
trading-mvp/
├── 📁 python/                          # Clean Architecture Python Backend
│   ├── 📁 app/
│   │   ├── 📁 domain/                  # 📦 DOMAIN LAYER
│   │   │   ├── 📁 entities/
│   │   │   │   ├── trading_decision.py    # Entidade principal
│   │   │   │   └── trading_session.py     # Sessão de trading
│   │   │   ├── 📁 value_objects/
│   │   │   │   ├── symbol.py              # Símbolo (BTC/USDT)
│   │   │   │   ├── money.py               # Valor monetário
│   │   │   │   ├── percentage.py          # Porcentagem
│   │   │   │   └── trading_action.py      # Ação (BUY/SELL/FLAT)
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
├── 📁 dotnet/                          # Clean Architecture .NET Backend
│   └── 📁 TradingExecutor/
│       ├── 📁 Domain/                  # 📦 DOMAIN LAYER
│       │   ├── Models/                    # Domain models (records)
│       │   ├── ValueObjects/              # Value objects
│       │   └── Interfaces/                # Domain interfaces
│       ├── 📁 Application/             # ⚙️ APPLICATION LAYER
│       │   ├── Services/                  # Application services
│       │   ├── UseCases/                  # Use cases
│       │   └── Interfaces/                # Application interfaces
│       ├── 📁 Infrastructure/          # 🏗️ INFRASTRUCTURE LAYER
│       │   ├── WebSocket/                 # WebSocket client
│       │   ├── OrderExecution/            # Order execution
│       │   ├── RiskManagement/            # Risk management
│       │   └── Logging/                   # Logging infrastructure
│       ├── Program.cs                  # 🚀 Main entry point
│       ├── OrderExecution.cs          # 📋 Order execution (legacy)
│       └── *.csproj                   # Projeto .NET com DI
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

## ⚙️ **Configuração (config.yaml)**

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
// 3. Descomentar linhas de execução real
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
cd dotnet/TradingExecutor
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
- [x] **Logs detalhados** para monitoramento completo
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
- [x] **Error Handling centralizado** e logging estruturado
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

**⚠️ DISCLAIMER**: Este é um projeto educacional com foco em **Clean Architecture**, **SOLID principles**, **real-time systems** e **WebSocket streaming**. O sistema demonstra como implementar arquitetura limpa em um contexto de trading automatizado. Trading automatizado envolve riscos financeiros significativos. Use apenas capital que você pode perder. O sistema atual utiliza **mock orders** para segurança. Não somos responsáveis por perdas financeiras.

**🏛️ DESTAQUE ARQUITETURAL**: Sistema completo implementando **Clean Architecture** com **Domain-Driven Design**, **SOLID principles**, **Dependency Injection**, **Use Cases pattern**, **Repository pattern**, **Value Objects**, e **Entity pattern** - **100% testado e funcionando!**

**🔥 DESTAQUE TÉCNICO**: Sistema completo de **trading em tempo real** com **comunicação WebSocket** entre Python, .NET e Angular seguindo **Clean Architecture** - **arquitetura de produção!**

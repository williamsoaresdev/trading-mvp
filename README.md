# 🚀 Algorithmic Trading MVP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)
[![Angular](https://img.shields.io/badge/Angular-20+-red.svg)](https://angular.io/)

A complete **real-time algorithmic trading system** featuring **machine learning predictions**, **WebSocket streaming**, **automated trading execution**, and **live monitoring dashboard**.

Este MVP implementa um pipeline completo para robô de trading automatizado com **machine learning**, **execução automática em tempo real**, **WebSocket para streaming de dados**, e **dashboard de monitoramento ao vivo**.

## 🏗️ Arquitetura

### **Python** (Machine Learning & Real-Time API)
- `python/app/model_train.py`: coleta dados (Binance via ccxt), gera features (EMA, RSI, ATR), rotula com *triple barrier* simplificado, faz *walk-forward*, treina LightGBM e salva `model.pkl` + `feature_config.json`.
- `python/app/service.py`: serviço **FastAPI** que carrega o modelo, puxa candles recentes, calcula features e retorna `BUY/SELL/FLAT` + tamanho de posição por *volatility targeting*.
- `python/app/simple_realtime.py`: **serviço de trading em tempo real** com WebSocket broadcasting e decisões automatizadas a cada 30-60 segundos.
- `python/app/utils.py`: utilitários (indicadores, rótulos, features).
- `python/requirements.txt`: dependências Python.

### **.NET** (Real-Time Trading Executor)
- `dotnet/TradingExecutor/Program.cs`: executor que **conecta via WebSocket** ao serviço Python, recebe decisões em tempo real e executa ordens automaticamente.
- `dotnet/TradingExecutor/RealTimeTradingExecutor.cs`: **cliente WebSocket** com fallback HTTP, aplica *risk management* e executa ordens com logging detalhado.
- `dotnet/TradingExecutor/TradingExecutor.csproj`: projeto .NET 8+ com dependências WebSocket.
- `dotnet/TradingExecutor/OrderExecution.cs`: interface de execução, com *mock orders* para testing seguro.

### **Angular** (Live Dashboard)
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

## 📁 **Estrutura do Projeto**

```
trading-mvp/
├── 📁 python/                  # ML & Real-Time API Backend
│   ├── 📁 app/
│   │   ├── model_train.py      # Treinamento do modelo ML
│   │   ├── service.py          # API FastAPI tradicional
│   │   ├── simple_realtime.py  # 🔥 API Real-Time com WebSocket
│   │   └── utils.py            # Utilitários e indicadores
│   ├── 📁 artifacts/           # Modelo treinado (git ignored)
│   ├── requirements.txt        # Dependências Python
│   └── run_server.py          # Script para subir API tradicional
├── 📁 dotnet/                  # Real-Time Trading Executor
│   └── 📁 TradingExecutor/
│       ├── Program.cs          # Executor principal
│       ├── RealTimeTradingExecutor.cs  # 🔥 Cliente WebSocket
│       ├── OrderExecution.cs   # Interface de ordens
│       └── *.csproj           # Projeto .NET com WebSocket
├── 📁 trading-dashboard/       # Live Dashboard Angular
│   ├── 📁 src/app/
│   │   ├── 📁 components/      # Componentes UI em tempo real
│   │   ├── 📁 services/        # 🔥 WebSocket + HTTP services
│   │   └── 📁 models/          # Interfaces TypeScript
│   └── package.json           # Dependências NPM
├── 📁 config/                 # Configurações
│   └── config.yaml            # Parâmetros de trading
├── run_realtime.py            # 🔥 Script para sistema completo
├── start_api.py               # Script simplificado para API
├── setup.bat / setup.sh       # Scripts de instalação
├── .gitignore                 # Arquivos ignorados
└── README.md                  # Esta documentação
```

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

### **🎯 Próximas Features**
- [ ] **Gráficos avançados** com Chart.js em tempo real
- [ ] **Múltiplos símbolos** simultâneos (BTC, ETH, etc)
- [ ] **Alertas push** para decisões importantes
- [ ] **Histórico persistente** com base de dados
- [ ] **Backtesting avançado** com métricas detalhadas
- [ ] **API de configuração** dinâmica via dashboard
- [ ] **Estratégias ensemble** com múltiplos modelos
- [ ] **Mobile app** para monitoramento remoto

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

**⚠️ DISCLAIMER**: Este é um projeto educacional com foco em **real-time systems** e **WebSocket streaming**. Trading automatizado envolve riscos financeiros significativos. Use apenas capital que você pode perder. O sistema atual utiliza **mock orders** para segurança. Não somos responsáveis por perdas financeiras.

**🔥 DESTAQUE**: Sistema completo de **trading em tempo real** com **comunicação WebSocket** entre Python, .NET e Angular - **testado e funcionando!**

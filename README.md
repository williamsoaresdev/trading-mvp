# 🚀 Algorithmic Trading MVP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)
[![Angular](https://img.shields.io/badge/Angular-20+-red.svg)](https://angular.io/)

A complete algorithmic trading system featuring **machine learning predictions**, **REST API**, **trading execution engine**, and **real-time monitoring dashboard**.

Este MVP implementa um pipeline completo para robô de trading automatizado com **machine learning**, **execução automática** e **dashboard de monitoramento em tempo real**.

## 🏗️ Arquitetura

### **Python** (Machine Learning & API)
- `python/app/model_train.py`: coleta dados (Binance via ccxt), gera features (EMA, RSI, ATR), rotula com *triple barrier* simplificado, faz *walk-forward*, treina LightGBM e salva `model.pkl` + `feature_config.json`.
- `python/app/service.py`: serviço **FastAPI** que carrega o modelo, puxa candles recentes, calcula features e retorna `BUY/SELL/FLAT` + tamanho de posição por *volatility targeting*.
- `python/app/utils.py`: utilitários (indicadores, rótulos, features).
- `python/requirements.txt`: dependências Python.

### **.NET** (Trading Executor)
- `dotnet/TradingExecutor/Program.cs`: executor que consome FastAPI a cada barra, aplica *rulebook* (limiares, circuit breakers) e **mocka** ordens.
- `dotnet/TradingExecutor/TradingExecutor.csproj`: projeto .NET 8.
- `dotnet/TradingExecutor/OrderExecution.cs`: interface de execução, com *stub* de Binance para ordens reais.

### **Angular** (Dashboard Web)
- `trading-dashboard/`: projeto Angular 20+ com dashboard responsivo
- **Componentes**: estatísticas em tempo real, tabela de decisões, gráficos
- **Serviços**: polling automático da API FastAPI a cada 30 segundos
- **UI moderna**: gradientes, animações, códigos de cores para decisões

### **Config**
- `config/config.yaml`: parâmetros (símbolo, timeframe, limiares, sizing, stops).

## 🚀 Pré-requisitos

- **Python 3.10+** (idealmente 3.11)
- **.NET 8 SDK** ou superior  
- **Node.js 18+** e npm para o dashboard Angular
- Conta/exchange para dados *live* (Binance — endpoints públicos bastam para dados; para ordens reais, inserir keys)

## Quick Start

### Option 1: **Real-Time Mode** (Recommended) 🔥

Start all services simultaneously with WebSocket streaming:

```bash
python run_realtime.py
```

This will:
- ✅ Start Python API with WebSocket support
- ✅ Enable real-time trading decisions (every 30 seconds)
- ✅ Launch Angular dashboard with live updates
- ✅ Start .NET executor with WebSocket connection
- ✅ Provide real-time monitoring and logging

**Access URLs:**
- Dashboard: http://localhost:4200 (live updates)
- API: http://localhost:8000
- WebSocket: ws://localhost:8000/ws

### Option 2: Automated Setup (First Time)

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

### Option 3: Manual Setup

1. **Setup Environment** (first time only):
```bash
# Linux/macOS
./setup.sh

# Windows
setup.bat

# Cross-platform
python setup.py
```

2. **Train the ML Model**:
```bash
cd python
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 1
```

3. **Start the Services**:

Terminal 1 - FastAPI Server:
```bash
# Easy way (auto-activates virtual environment)
python run_server.py

# Manual way
cd python
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m uvicorn app.service:app --host 0.0.0.0 --port 8000 --reload
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

## 📊 **Dashboard Features**

- **📈 Estatísticas em Tempo Real**
  - Total de decisões (BUY/SELL/FLAT)  
  - Percentuais de distribuição
  - Preço atual do BTC
  - Nível de confiança médio

- **📋 Tabela de Decisões**
  - Últimas 100 decisões com timestamps
  - Probabilidades de compra/venda  
  - Barra de confiança visual
  - Códigos de cores por tipo de decisão

- **🔄 Atualizações Automáticas**
  - Polling da API a cada 30 segundos
  - Indicador de status da conexão
  - Botão de refresh manual

## 🌐 **URLs de Acesso**

- **🖥️ Dashboard Angular**: http://localhost:4200
- **🔗 API FastAPI**: http://localhost:8000  
- **📊 API Health**: http://localhost:8000/health
- **🤖 API Predict**: http://localhost:8000/predict?symbol=BTC/USDT&timeframe=1h

## 📁 **Estrutura do Projeto**

```
trading-mvp/
├── 📁 python/                  # ML & API Backend
│   ├── 📁 app/
│   │   ├── model_train.py      # Treinamento do modelo
│   │   ├── service.py          # API FastAPI  
│   │   └── utils.py            # Utilitários
│   ├── 📁 artifacts/           # Modelo treinado (git ignored)
│   ├── requirements.txt        # Dependências Python
│   └── run_server.py          # Script para subir API
├── 📁 dotnet/                  # Trading Executor
│   └── 📁 TradingExecutor/
│       ├── Program.cs          # Executor principal
│       ├── OrderExecution.cs   # Interface de ordens
│       └── *.csproj           # Projeto .NET
├── 📁 trading-dashboard/       # Dashboard Angular
│   ├── 📁 src/app/
│   │   ├── 📁 components/      # Componentes UI
│   │   ├── 📁 services/        # Serviços API
│   │   └── 📁 models/          # Interfaces TypeScript
│   └── package.json           # Dependências NPM
├── 📁 config/                 # Configurações
│   └── config.yaml            # Parâmetros de trading
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

### **Python: ModuleNotFoundError**
```bash
# Certificar que venv está ativo
which python  # deve apontar para .venv

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### **.NET: Connection refused**
```bash
# Verificar se FastAPI está rodando
curl http://localhost:8000/health

# Verificar porta em uso
netstat -an | grep 8000
```

### **Angular: Build errors**
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

## 🚀 **Roadmap & Melhorias**

### **🎯 Próximas features**
- [ ] WebSocket para atualizações em tempo real
- [ ] Gráficos avançados com Chart.js  
- [ ] Histórico detalhado com filtros
- [ ] Alertas para decisões importantes
- [ ] Métricas de performance avançadas
- [ ] Suporte a múltiplos símbolos
- [ ] Estratégias ensemble

### **📊 Analytics sugeridas**
- [ ] Heatmap de performance por hora/dia
- [ ] Correlação entre volatilidade e accuracy  
- [ ] Backtest com dados out-of-sample
- [ ] Monte Carlo para stress testing

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**⚠️ DISCLAIMER**: Este é um projeto educacional. Trading automatizado envolve riscos financeiros significativos. Use apenas capital que você pode perder. Não somos responsáveis por perdas financeiras.

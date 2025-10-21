# Guia Completo de Execução - Trading MVP

## 🔧 Pré-requisitos

### Python
- **Versão recomendada**: Python 3.11
- **Versão mínima**: Python 3.10
- **Evitar**: Python 3.12 (instabilidades conhecidas)

### .NET
- **.NET 8 SDK** ou superior

### Verificação de Versões
```bash
python --version  # Deve ser 3.10+
dotnet --version  # Deve ser 8.0+
```

## 📦 1. Configuração do Ambiente Python

### Passo 1: Navegar para o diretório Python
```bash
cd trading-intelligence
```

### Passo 2: Criar ambiente virtual
```bash
# Linux/Mac
python -m venv .venv && source .venv/bin/activate

# Windows
python -m venv .venv && .venv\Scripts\activate
```

### Passo 3: Instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Treinar o modelo (⏱️ ~10-15 minutos)
```bash
python app/model_train.py --symbol BTC/USDT --timeframe 1h --years 2
```

**Saída esperada:**
- Arquivo `artifacts/model.pkl`
- Arquivo `artifacts/feature_config.json`
- Accuracy do modelo reportada

### Passo 5: Iniciar o serviço FastAPI
```bash
uvicorn app.service:app --host 0.0.0.0 --port 8000
```

**Verificação:**
- Acesse: http://localhost:8000/health
- Deve retornar: `{"status":"ok", "model_loaded": true, ...}`

## 🎯 2. Executar o Robô (.NET)

### Em um novo terminal:

```bash
cd trading-executor
dotnet build
```

**Verificar se não há erros de compilação**

```bash
dotnet run
```

**Saída esperada:**
```
TradingExecutor started. Press Ctrl+C to stop.
2025-10-20T... | BTC/USDT 1h | BUY | pBuy=0.612 pSell=0.388 | price=67234.50 | pos=2.5%
[MOCK BUY] BTC/USDT qty=0.000371
```

## 🔍 3. Testes e Verificação

### Testar API manualmente:
```bash
curl "http://localhost:8000/predict?symbol=BTC/USDT&timeframe=1h"
```

### Verificar logs do executor:
- Decisões sendo tomadas a cada minuto
- Ordens mock sendo executadas
- Preços e probabilidades sendo reportados

## ⚠️ 4. Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
# Verificar se ambiente virtual está ativo
which python  # Deve apontar para .venv

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Connection refused" no .NET
```bash
# Verificar se FastAPI está rodando
curl http://localhost:8000/health

# Verificar porta em uso
netstat -an | grep 8000
```

### Erro: "Model not found"
```bash
# Verificar se treinamento foi concluído
ls -la artifacts/
# Deve ter: model.pkl e feature_config.json
```

## 🚀 5. Próximos Passos

### Para Paper Trading prolongado:
1. Execute por 2-4 semanas
2. Monitore performance via logs
3. Analise métricas de P&L simulado

### Para Produção (quando ready):
1. Implemente `BinanceSpotOrderExecutor`
2. Configure API keys da Binance
3. Inicie com capital pequeno (< $100)
4. Monitore 24/7 nos primeiros dias

## 📊 6. Monitoramento

### Métricas importantes:
- **Accuracy direcional**: >55% considerado bom
- **Win rate**: ratio de trades profitable
- **Max drawdown**: perda máxima consecutiva
- **Sharpe ratio**: retorno ajustado ao risco

### Logs a observar:
- Frequência de trades
- Distribuição BUY/SELL/FLAT
- Valores de probabilidade
- Tamanhos de posição

---

**⚠️ IMPORTANTE**: Este MVP está em modo PAPER TRADING. Nenhuma ordem real será executada até que você implemente e ative o `BinanceSpotOrderExecutor`.
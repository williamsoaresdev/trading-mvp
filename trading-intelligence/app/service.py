import os, json, time
from pathlib import Path
from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
import numpy as np
import ccxt
import joblib
import yaml
from datetime import datetime, timedelta, timezone

from .utils import make_features, volatility_target_position, atr

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "artifacts"
CFG = Path(__file__).resolve().parents[2] / "config" / "config.yaml"

with open(CFG, "r") as f:
    CONFIG = yaml.safe_load(f)

MODEL = joblib.load(ART / "model.pkl")
with open(ART / "feature_config.json", "r") as f:
    FEATCFG = json.load(f)

app = FastAPI(title="Trading MVP Service", version="0.1.0")

class PredictResponse(BaseModel):
    symbol: str
    timeframe: str
    decision: str
    proba_buy: float
    proba_sell: float
    position_fraction: float
    price: float
    atr_pct: float
    ts_utc: str

def fetch_recent(symbol: str, timeframe: str, lookback: int = 300):
    ex = ccxt.binance()
    tf_ms = ex.parse_timeframe(timeframe) * 1000
    since = int((datetime.now(timezone.utc) - timedelta(milliseconds=tf_ms * (lookback+5))).timestamp() * 1000)
    data = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=lookback)
    df = pd.DataFrame(data, columns=["ts","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df[["timestamp","open","high","low","close","volume"]]

@app.get("/health")
def health():
    return {"status":"ok", "model_loaded": True, "features": FEATCFG["features"][:5] + ["..."]}

@app.get("/predict", response_model=PredictResponse)
def predict(symbol: str = Query(default=None), timeframe: str = Query(default=None)):
    sym = symbol or CONFIG["symbol"]
    tf = timeframe or CONFIG["timeframe"]

    df = fetch_recent(sym, tf, lookback=400)
    feat = make_features(df)
    X = feat[FEATCFG["features"]].tail(1)

    # inferência: prob. classe 0 (sell), 2 (buy)
    probs = MODEL.predict(X)[0]
    proba_sell = float(probs[0])
    proba_buy = float(probs[2])

    decision = "FLAT"
    if proba_buy >= CONFIG["proba_buy_threshold"] and proba_buy > proba_sell:
        decision = "BUY"
    elif proba_sell >= CONFIG["proba_sell_threshold"] and proba_sell > proba_buy:
        decision = "SELL"

    last = feat.tail(1).iloc[0]
    atr_pct = float(last["atr_pct"])
    pos_frac = float(volatility_target_position(atr_pct,
                        vol_target_annual=CONFIG["vol_target_annual"],
                        min_frac=CONFIG["min_position_fraction"],
                        max_frac=CONFIG["max_position_fraction"]))

    return PredictResponse(
        symbol=sym,
        timeframe=tf,
        decision=decision,
        proba_buy=proba_buy,
        proba_sell=proba_sell,
        position_fraction=pos_frac,
        price=float(last["close"]),
        atr_pct=atr_pct,
        ts_utc=str(last["timestamp"])
    )

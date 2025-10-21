import argparse, json, time, math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import ccxt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import joblib
from pathlib import Path

from .utils import make_features, triple_barrier_labels

def fetch_ohlcv(symbol: str, timeframe: str, years: int = 2) -> pd.DataFrame:
    ex = ccxt.binance()
    since = int((datetime.now(timezone.utc) - timedelta(days=365*years)).timestamp() * 1000)
    all_rows = []
    limit = 1000
    while True:
        batch = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not batch:
            break
        all_rows.extend(batch)
        since = batch[-1][0] + 1
        if len(batch) < limit:
            break
        # safety sleep to avoid rate limits
        time.sleep(0.2)
    df = pd.DataFrame(all_rows, columns=["ts","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["ts"], unit="ms", utc=True).dt.tz_convert("UTC")
    return df[["timestamp","open","high","low","close","volume"]]

def walk_forward_train(df_feat: pd.DataFrame, labels: pd.Series, n_splits: int = 5):
    # alinhamento
    X = df_feat.drop(columns=["timestamp","open","high","low","close","volume"]).copy()
    y = labels.loc[df_feat.index]
    mask_valid = y != 0  # remove neutros para simplificar (MVP)
    X, y = X[mask_valid], y[mask_valid]

    tscv = TimeSeriesSplit(n_splits=n_splits)
    best_model, best_score = None, -1
    fold_scores = []
    for fold, (tr_idx, val_idx) in enumerate(tscv.split(X)):
        Xtr, Xval = X.iloc[tr_idx], X.iloc[val_idx]
        ytr, yval = y.iloc[tr_idx], y.iloc[val_idx]
        dtrain = lgb.Dataset(Xtr, label=ytr)
        dval = lgb.Dataset(Xval, label=yval, reference=dtrain)
        params = {
            "objective": "multiclass",
            "num_class": 3,               # classes: -1,0,1 (mas removemos 0; manteremos mapeamento {-1->0, 1->2})
            "learning_rate": 0.05,
            "num_leaves": 63,
            "max_depth": -1,
            "metric": "multi_logloss",
            "verbose": -1,
            "feature_pre_filter": False
        }
        # Remap -1 -> 0, 1 -> 2 (vamos usar 1 classe vazia no centro para compatibilidade)
        def remap(y_):
            return np.where(y_==-1, 0, 2)
        ytr_m = remap(ytr.values)
        yval_m = remap(yval.values)
        dtrain = lgb.Dataset(Xtr, label=ytr_m)
        dval = lgb.Dataset(Xval, label=yval_m, reference=dtrain)
        model = lgb.train(
            params,
            dtrain,
            num_boost_round=500,
            valid_sets=[dtrain, dval],
            valid_names=["train","valid"],
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)]
        )
        # accuracy simples direcional (mapear de volta)
        pred = model.predict(Xval).argmax(axis=1)
        pred_dir = np.where(pred==0, -1, 1)
        acc = accuracy_score(yval.values, pred_dir)
        fold_scores.append(acc)
        if acc > best_score:
            best_score = acc
            best_model = model
    return best_model, float(np.mean(fold_scores)), X.columns.tolist()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--years", type=int, default=2)
    parser.add_argument("--up", type=float, default=0.015)
    parser.add_argument("--dn", type=float, default=-0.007)
    parser.add_argument("--horizon", type=int, default=90)
    args = parser.parse_args()

    outdir = Path(__file__).resolve().parent.parent / "artifacts"
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching OHLCV for {args.symbol} {args.timeframe} ({args.years}y)...")
    df = fetch_ohlcv(args.symbol, args.timeframe, years=args.years)
    feat = make_features(df)
    labels = triple_barrier_labels(feat, up=args.up, dn=args.dn, horizon=args.horizon)

    print("Training with walk-forward...")
    model, cv_acc, feature_names = walk_forward_train(feat, labels, n_splits=5)
    print(f"CV directional accuracy: {cv_acc:.3f}")

    # salvar artefatos
    model_path = outdir / "model.pkl"
    joblib.dump(model, model_path)

    config = {
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "features": feature_names,
        "labeling": {"up": args.up, "dn": args.dn, "horizon": args.horizon},
        "cv_directional_accuracy": cv_acc
    }
    with open(outdir / "feature_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"Saved: {model_path}")
    print(f"Saved: {outdir / 'feature_config.json'}")

if __name__ == "__main__":
    main()

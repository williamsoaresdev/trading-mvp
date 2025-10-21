import math
import numpy as np
import pandas as pd
from typing import Tuple, Dict

# --------- Indicators (pure pandas, sem TA-Lib) ----------

def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.ewm(com=period-1, adjust=False).mean()
    roll_down = down.ewm(com=period-1, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-12)
    return 100 - (100 / (1 + rs))

def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df['close'].shift(1)
    tr1 = df['high'] - df['low']
    tr2 = (df['high'] - prev_close).abs()
    tr3 = (df['low'] - prev_close).abs()
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    tr = true_range(df)
    return tr.ewm(alpha=1/period, adjust=False).mean()

# --------- Feature engineering ----------

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['ret_1'] = out['close'].pct_change()
    out['ret_3'] = out['close'].pct_change(3)
    out['ret_6'] = out['close'].pct_change(6)
    out['ema_fast'] = ema(out['close'], 12)
    out['ema_slow'] = ema(out['close'], 26)
    out['ema_ratio'] = out['ema_fast'] / (out['ema_slow'] + 1e-12) - 1.0
    out['rsi_14'] = rsi(out['close'], 14)
    out['atr_14'] = atr(out, 14)
    out['atr_pct'] = out['atr_14'] / (out['close'] + 1e-12)
    out['bb_mid'] = out['close'].rolling(20).mean()
    out['bb_std'] = out['close'].rolling(20).std()
    out['bb_pos'] = (out['close'] - out['bb_mid']) / (out['bb_std'] + 1e-12)
    out['hour'] = out['timestamp'].dt.hour
    out['dow'] = out['timestamp'].dt.dayofweek
    out = out.dropna().reset_index(drop=True)
    return out

# --------- Labeling (triple barrier simplificado) ---------

def triple_barrier_labels(df: pd.DataFrame, up: float, dn: float, horizon: int) -> pd.Series:
    """
    up, dn são limiares de retorno (ex.: 0.015 e -0.007). horizon em barras.
    Retorna labels {+1, -1, 0}.
    """
    closes = df['close'].values
    n = len(df)
    labels = np.zeros(n, dtype=int)
    for i in range(n - horizon):
        entry = closes[i]
        up_lvl = entry * (1 + up)
        dn_lvl = entry * (1 + dn)
        win = closes[i+1:i+horizon+1]
        hit_up = np.where(win >= up_lvl)[0]
        hit_dn = np.where(win <= dn_lvl)[0]
        if hit_up.size > 0 and (hit_dn.size == 0 or hit_up[0] < hit_dn[0]):
            labels[i] = 1
        elif hit_dn.size > 0 and (hit_up.size == 0 or hit_dn[0] < hit_up[0]):
            labels[i] = -1
        else:
            # se não atingiu nem up nem dn até o horizonte, usa sinal do retorno líquido
            ret = (win[-1] / entry) - 1
            labels[i] = 1 if ret > 0 else (-1 if ret < 0 else 0)
    return pd.Series(labels, index=df.index)

# --------- Volatility targeting ----------

def volatility_target_position(atr_pct: float, vol_target_annual: float = 0.20, min_frac: float = 0.02, max_frac: float = 0.30) -> float:
    """
    Tamanho de posição aproximado a partir de vol implícita via ATR%.
    """
    # converte alvo anual ~ alvo diário simplificado (assumindo ~252 dias, 24h mercados cripto é contínuo; é uma heurística)
    vol_target_daily = vol_target_annual / (252 ** 0.5)
    current_vol = max(atr_pct, 1e-6)
    frac = vol_target_daily / current_vol
    frac = max(min_frac, min(max_frac, frac))
    return float(frac)

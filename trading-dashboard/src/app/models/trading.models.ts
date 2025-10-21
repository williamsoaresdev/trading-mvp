export interface TradingDecision {
  symbol: string;
  timeframe: string;
  decision: 'BUY' | 'SELL' | 'FLAT';
  proba_buy: number;
  proba_sell: number;
  position_fraction: number;
  price: number;
  atr_pct: number;
  ts_utc: string;
  timestamp?: Date;
}

export interface HealthStatus {
  status: string;
  model_loaded: boolean;
  features: string[];
}

export interface TradingStats {
  totalDecisions: number;
  buyDecisions: number;
  sellDecisions: number;
  flatDecisions: number;
  averageProba: number;
  currentPrice: number;
  totalVolume: number;
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    fill: boolean;
  }[];
}
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, Subject } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { TradingDecision, HealthStatus, TradingStats } from '../models/trading.models';

export interface WebSocketMessage {
  type: 'status' | 'trading_decision' | 'error';
  data: any;
}

@Injectable({
  providedIn: 'root'
})
export class TradingApi {
  private readonly API_BASE_URL = 'http://localhost:8000';
  private readonly WS_URL = 'ws://localhost:8000/ws';
  
  private decisionsSubject = new BehaviorSubject<TradingDecision[]>([]);
  private statsSubject = new BehaviorSubject<TradingStats | null>(null);
  private connectionStatusSubject = new BehaviorSubject<boolean>(false);
  private wsMessagesSubject = new Subject<WebSocketMessage>();
  
  public decisions$ = this.decisionsSubject.asObservable();
  public stats$ = this.statsSubject.asObservable();
  public connectionStatus$ = this.connectionStatusSubject.asObservable();
  public wsMessages$ = this.wsMessagesSubject.asObservable();
  
  private websocket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(private http: HttpClient) {
    this.initializeWebSocket();
  }

  getHealth(): Observable<HealthStatus> {
    return this.http.get<HealthStatus>(`${this.API_BASE_URL}/health`);
  }

  getPredict(symbol: string = 'BTC/USDT'): Observable<TradingDecision> {
    return this.http.post<TradingDecision>(`${this.API_BASE_URL}/predict`, {
      symbol: symbol
    }).pipe(
      map(decision => ({
        ...decision,
        timestamp: new Date()
      }))
    );
  }

  getTradingHistory(limit: number = 50): Observable<{decisions: TradingDecision[], total: number}> {
    return this.http.get<{decisions: TradingDecision[], total: number}>(`${this.API_BASE_URL}/trading/history?limit=${limit}`);
  }

  startRealTimeTrading(symbol: string = 'BTC/USDT', intervalSeconds: number = 30): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/trading/start`, {
      symbol,
      interval_seconds: intervalSeconds
    });
  }

  stopRealTimeTrading(): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/trading/stop`, {});
  }

  getTradingStatus(): Observable<any> {
    return this.http.get(`${this.API_BASE_URL}/trading/status`);
  }

  private initializeWebSocket(): void {
    try {
      this.websocket = new WebSocket(this.WS_URL);
      
      this.websocket.onopen = () => {
        console.log('✅ WebSocket connected');
        this.connectionStatusSubject.next(true);
        this.reconnectAttempts = 0;
      };
      
      this.websocket.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleWebSocketMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      this.websocket.onclose = () => {
        console.log('❌ WebSocket disconnected');
        this.connectionStatusSubject.next(false);
        this.handleReconnection();
      };
      
      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.connectionStatusSubject.next(false);
      };
      
    } catch (error) {
      console.error('Error initializing WebSocket:', error);
      this.handleReconnection();
    }
  }

  private handleWebSocketMessage(message: WebSocketMessage): void {
    this.wsMessagesSubject.next(message);
    
    switch (message.type) {
      case 'trading_decision':
        this.handleTradingDecision(message.data);
        break;
      case 'status':
        console.log('Status update:', message.data);
        break;
      case 'error':
        console.error('WebSocket error:', message.data);
        break;
    }
  }

  private handleTradingDecision(decisionData: any): void {
    // Transform the decision data to match our model
    const decision: TradingDecision = {
      decision: decisionData.prediction.action,
      proba_buy: decisionData.prediction.proba_buy,
      proba_sell: decisionData.prediction.proba_sell,
      price: decisionData.prediction.current_price,
      position_fraction: decisionData.prediction.position_fraction,
      timestamp: new Date(decisionData.timestamp),
      symbol: decisionData.symbol,
      timeframe: '1h', // Default timeframe
      atr_pct: decisionData.prediction.atr_pct || 0,
      ts_utc: decisionData.timestamp
    };
    
    this.addDecision(decision);
  }

  private handleReconnection(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.initializeWebSocket();
      }, delay);
    } else {
      console.error('Max reconnection attempts reached. WebSocket connection failed.');
    }
  }

  private addDecision(decision: TradingDecision): void {
    const currentDecisions = this.decisionsSubject.value;
    const updatedDecisions = [decision, ...currentDecisions].slice(0, 100); // Keep last 100 decisions
    this.decisionsSubject.next(updatedDecisions);
    this.updateStats(updatedDecisions);
  }

  private updateStats(decisions: TradingDecision[]): void {
    if (decisions.length === 0) return;

    const buyDecisions = decisions.filter(d => d.decision === 'BUY').length;
    const sellDecisions = decisions.filter(d => d.decision === 'SELL').length;
    const flatDecisions = decisions.filter(d => d.decision === 'FLAT').length;
    
    const averageProba = decisions.reduce((sum, d) => 
      sum + Math.max(d.proba_buy, d.proba_sell), 0) / decisions.length;
    
    const totalVolume = decisions.reduce((sum, d) => 
      sum + (d.position_fraction * d.price), 0);

    const stats: TradingStats = {
      totalDecisions: decisions.length,
      buyDecisions,
      sellDecisions,
      flatDecisions,
      averageProba,
      currentPrice: decisions[0]?.price || 0,
      totalVolume
    };

    this.statsSubject.next(stats);
  }

  getDecisions(): TradingDecision[] {
    return this.decisionsSubject.value;
  }

  sendWebSocketMessage(message: string): void {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(message);
    }
  }

  disconnect(): void {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
  }
}

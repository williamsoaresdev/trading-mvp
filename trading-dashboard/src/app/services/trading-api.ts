import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, interval } from 'rxjs';
import { map, catchError, startWith, switchMap } from 'rxjs/operators';
import { TradingDecision, HealthStatus, TradingStats } from '../models/trading.models';

@Injectable({
  providedIn: 'root'
})
export class TradingApi {
  private readonly API_BASE_URL = 'http://localhost:8000';
  private decisionsSubject = new BehaviorSubject<TradingDecision[]>([]);
  private statsSubject = new BehaviorSubject<TradingStats | null>(null);
  
  public decisions$ = this.decisionsSubject.asObservable();
  public stats$ = this.statsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.startPolling();
  }

  getHealth(): Observable<HealthStatus> {
    return this.http.get<HealthStatus>(`${this.API_BASE_URL}/health`);
  }

  getPredict(symbol: string = 'BTC/USDT', timeframe: string = '1h'): Observable<TradingDecision> {
    return this.http.get<TradingDecision>(`${this.API_BASE_URL}/predict`, {
      params: { symbol, timeframe }
    }).pipe(
      map(decision => ({
        ...decision,
        timestamp: new Date()
      }))
    );
  }

  private startPolling(): void {
    // Poll API every 30 seconds
    interval(30000).pipe(
      startWith(0),
      switchMap(() => this.getPredict()),
      catchError(error => {
        console.error('Error fetching trading decision:', error);
        return [];
      })
    ).subscribe(decision => {
      if (decision) {
        this.addDecision(decision);
      }
    });
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
}

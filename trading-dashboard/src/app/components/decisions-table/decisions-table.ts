import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { TradingApi } from '../../services/trading-api';
import { TradingDecision } from '../../models/trading.models';

@Component({
  selector: 'app-decisions-table',
  imports: [CommonModule],
  templateUrl: './decisions-table.html',
  styleUrl: './decisions-table.scss'
})
export class DecisionsTable implements OnInit {
  decisions$: Observable<TradingDecision[]>;

  constructor(private tradingApi: TradingApi) {
    this.decisions$ = this.tradingApi.decisions$;
  }

  ngOnInit(): void {}

  getDecisionClass(decision: string): string {
    switch (decision) {
      case 'BUY': return 'decision-buy';
      case 'SELL': return 'decision-sell';
      case 'FLAT': return 'decision-flat';
      default: return '';
    }
  }

  getDecisionIcon(decision: string): string {
    switch (decision) {
      case 'BUY': return '🟢';
      case 'SELL': return '🔴';
      case 'FLAT': return '⚪';
      default: return '❓';
    }
  }

  getConfidenceLevel(probaBuy: number, probaSell: number): number {
    return Math.max(probaBuy, probaSell);
  }

  trackByTimestamp(index: number, decision: TradingDecision): string {
    return decision.ts_utc;
  }
}

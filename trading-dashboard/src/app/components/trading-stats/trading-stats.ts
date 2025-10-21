import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { TradingApi } from '../../services/trading-api';
import { TradingStats as TradingStatsModel } from '../../models/trading.models';

@Component({
  selector: 'app-trading-stats',
  imports: [CommonModule],
  templateUrl: './trading-stats.html',
  styleUrl: './trading-stats.scss'
})
export class TradingStats implements OnInit {
  stats$: Observable<TradingStatsModel | null>;

  constructor(private tradingApi: TradingApi) {
    this.stats$ = this.tradingApi.stats$;
  }

  ngOnInit(): void {}

  getBuyPercentage(stats: TradingStatsModel): number {
    return stats.totalDecisions > 0 ? (stats.buyDecisions / stats.totalDecisions) * 100 : 0;
  }

  getSellPercentage(stats: TradingStatsModel): number {
    return stats.totalDecisions > 0 ? (stats.sellDecisions / stats.totalDecisions) * 100 : 0;
  }

  getFlatPercentage(stats: TradingStatsModel): number {
    return stats.totalDecisions > 0 ? (stats.flatDecisions / stats.totalDecisions) * 100 : 0;
  }
}

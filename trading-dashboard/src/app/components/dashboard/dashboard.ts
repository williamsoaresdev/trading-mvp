import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TradingStats } from '../trading-stats/trading-stats';
import { DecisionsTable } from '../decisions-table/decisions-table';
import { TradingApi } from '../../services/trading-api';
import { Observable } from 'rxjs';
import { HealthStatus } from '../../models/trading.models';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, TradingStats, DecisionsTable],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  health$: Observable<HealthStatus>;
  lastUpdate = new Date();

  constructor(private tradingApi: TradingApi) {
    this.health$ = this.tradingApi.getHealth();
  }

  ngOnInit(): void {
    // Update last update time every minute
    setInterval(() => {
      this.lastUpdate = new Date();
    }, 60000);
  }

  refreshData(): void {
    this.health$ = this.tradingApi.getHealth();
    this.lastUpdate = new Date();
  }
}

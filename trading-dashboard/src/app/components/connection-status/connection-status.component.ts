import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { TradingApi } from '../../services/trading-api';

@Component({
  selector: 'app-connection-status',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="connection-status" [ngClass]="statusClass">
      <div class="status-indicator">
        <div class="status-dot" [ngClass]="statusClass"></div>
        <span class="status-text">{{ statusText }}</span>
      </div>
      
      <div class="connection-actions" *ngIf="!isConnected">
        <button class="btn-reconnect" (click)="reconnect()">
          🔄 Reconnect
        </button>
      </div>
      
      <div class="real-time-controls" *ngIf="isConnected">
        <button 
          class="btn-toggle-trading" 
          [ngClass]="{'active': isTradingActive}"
          (click)="toggleRealTimeTrading()">
          {{ isTradingActive ? '⏹️ Stop' : '▶️ Start' }} Trading
        </button>
      </div>
    </div>
  `,
  styles: [`
    .connection-status {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 20px;
      background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3a 100%);
      border-radius: 12px;
      margin-bottom: 20px;
      border: 1px solid #333;
    }

    .status-indicator {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .status-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }

    .status-dot.connected {
      background: #10b981;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    .status-dot.disconnected {
      background: #ef4444;
      box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }

    .status-dot.connecting {
      background: #f59e0b;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }

    .status-text {
      color: #e5e7eb;
      font-weight: 500;
      font-size: 14px;
    }

    .connection-actions, .real-time-controls {
      display: flex;
      gap: 10px;
    }

    .btn-reconnect, .btn-toggle-trading {
      padding: 8px 16px;
      border: none;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .btn-reconnect {
      background: #3b82f6;
      color: white;
    }

    .btn-reconnect:hover {
      background: #2563eb;
      transform: translateY(-1px);
    }

    .btn-toggle-trading {
      background: #6b7280;
      color: white;
    }

    .btn-toggle-trading.active {
      background: #10b981;
    }

    .btn-toggle-trading:hover {
      background: #059669;
      transform: translateY(-1px);
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }

    .connected .status-text { color: #10b981; }
    .disconnected .status-text { color: #ef4444; }
    .connecting .status-text { color: #f59e0b; }
  `]
})
export class ConnectionStatusComponent implements OnInit, OnDestroy {
  isConnected = false;
  isTradingActive = false;
  private subscriptions: Subscription[] = [];

  constructor(private tradingApi: TradingApi) {}

  ngOnInit(): void {
    // Subscribe to connection status
    this.subscriptions.push(
      this.tradingApi.connectionStatus$.subscribe(status => {
        this.isConnected = status;
      })
    );

    // Check trading status periodically
    this.checkTradingStatus();
    setInterval(() => this.checkTradingStatus(), 10000); // Check every 10 seconds
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  get statusClass(): string {
    return this.isConnected ? 'connected' : 'disconnected';
  }

  get statusText(): string {
    if (this.isConnected) {
      return this.isTradingActive ? 'Live Trading Active' : 'Connected - Ready';
    }
    return 'WebSocket Disconnected';
  }

  reconnect(): void {
    // Force reconnection by reinitializing the service
    window.location.reload();
  }

  toggleRealTimeTrading(): void {
    if (this.isTradingActive) {
      this.tradingApi.stopRealTimeTrading().subscribe({
        next: () => {
          this.isTradingActive = false;
          console.log('Real-time trading stopped');
        },
        error: (error) => console.error('Error stopping trading:', error)
      });
    } else {
      this.tradingApi.startRealTimeTrading('BTC/USDT', 30).subscribe({
        next: () => {
          this.isTradingActive = true;
          console.log('Real-time trading started');
        },
        error: (error) => console.error('Error starting trading:', error)
      });
    }
  }

  private checkTradingStatus(): void {
    this.tradingApi.getTradingStatus().subscribe({
      next: (status) => {
        this.isTradingActive = status.is_running;
      },
      error: () => {
        // Ignore errors for status check
      }
    });
  }
}
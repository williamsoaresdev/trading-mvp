import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradingStats } from './trading-stats';

describe('TradingStats', () => {
  let component: TradingStats;
  let fixture: ComponentFixture<TradingStats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TradingStats]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TradingStats);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

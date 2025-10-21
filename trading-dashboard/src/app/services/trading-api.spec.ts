import { TestBed } from '@angular/core/testing';

import { TradingApi } from './trading-api';

describe('TradingApi', () => {
  let service: TradingApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TradingApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

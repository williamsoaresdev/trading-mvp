import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecisionsTable } from './decisions-table';

describe('DecisionsTable', () => {
  let component: DecisionsTable;
  let fixture: ComponentFixture<DecisionsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DecisionsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DecisionsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

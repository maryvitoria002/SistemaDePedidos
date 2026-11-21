import { TestBed } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { App } from './app';
import { routes } from './app.routes';
import { ApiErrorMapper } from './api/http-api';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideRouter(routes)],
    })
      .compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render the application brand', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.brand')?.textContent).toContain('Loja API');
  });

  it('should show a short stock error', () => {
    const mapper = new ApiErrorMapper();
    const error = new HttpErrorResponse({
      status: 400,
      error: { error: 'Estoque insuficiente para o produto Livro.' },
    });

    expect(mapper.map(error)).toBe('Estoque insuficiente para este produto.');
  });
});

import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Pedido } from '../models';
import { HttpApiConfig } from './http-api';

@Injectable({ providedIn: 'root' })
export class OrderApi {
  private readonly http = inject(HttpClient);
  private readonly config = inject(HttpApiConfig);

  list(): Observable<Pedido[]> {
    return this.http.get<Pedido[]>(`${this.config.baseUrl}/pedido/`);
  }

  get(id: string): Observable<Pedido> {
    return this.http.get<Pedido>(`${this.config.baseUrl}/pedido/${id}/`);
  }

  create(body: Record<string, unknown>): Observable<Pedido> {
    return this.http.post<Pedido>(`${this.config.baseUrl}/pedido/create/`, body);
  }

  update(id: string, body: Record<string, unknown>): Observable<Pedido> {
    return this.http.put<Pedido>(`${this.config.baseUrl}/pedido/${id}/update/`, body);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.config.baseUrl}/pedido/${id}/delete/`);
  }

  pay(id: string, formaPagamento: string): Observable<Pedido> {
    return this.http.post<Pedido>(
      `${this.config.baseUrl}/pedido/${id}/pagar/`,
      { forma_pagamento: formaPagamento },
    );
  }

  cancel(id: string): Observable<Pedido> {
    return this.http.post<Pedido>(`${this.config.baseUrl}/pedido/${id}/cancelar/`, {});
  }
}

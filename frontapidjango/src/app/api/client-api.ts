import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Cliente, Pedido } from '../models';
import { HttpApiConfig } from './http-api';

@Injectable({ providedIn: 'root' })
export class ClientApi {
  private readonly http = inject(HttpClient);
  private readonly config = inject(HttpApiConfig);

  list(): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.config.baseUrl}/cliente/`);
  }

  get(id: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.config.baseUrl}/cliente/${id}/`);
  }

  create(body: Record<string, unknown>): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.config.baseUrl}/cliente/create/`, body);
  }

  update(id: string, body: Record<string, unknown>): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.config.baseUrl}/cliente/${id}/update/`, body);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.config.baseUrl}/cliente/${id}/delete/`);
  }

  orders(id: string): Observable<Pedido[]> {
    return this.http.get<Pedido[]>(`${this.config.baseUrl}/cliente/${id}/pedidos/`);
  }
}

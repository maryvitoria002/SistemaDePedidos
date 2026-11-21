import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Produto } from '../models';
import { HttpApiConfig } from './http-api';

@Injectable({ providedIn: 'root' })
export class ProductApi {
  private readonly http = inject(HttpClient);
  private readonly config = inject(HttpApiConfig);

  list(): Observable<Produto[]> {
    return this.http.get<Produto[]>(`${this.config.baseUrl}/produto/`);
  }

  get(id: string): Observable<Produto> {
    return this.http.get<Produto>(`${this.config.baseUrl}/produto/${id}/`);
  }

  create(body: Record<string, unknown>): Observable<Produto> {
    return this.http.post<Produto>(`${this.config.baseUrl}/produto/create/`, body);
  }

  update(id: string, body: Record<string, unknown>): Observable<Produto> {
    return this.http.put<Produto>(`${this.config.baseUrl}/produto/${id}/update/`, body);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.config.baseUrl}/produto/${id}/delete/`);
  }
}

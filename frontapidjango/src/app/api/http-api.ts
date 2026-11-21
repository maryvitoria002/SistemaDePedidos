import { HttpErrorResponse } from '@angular/common/http';

export class HttpApiConfig {
  readonly baseUrl = '/api';
}

export class ApiErrorMapper {
  map(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      const body = error.error;
      if (typeof body === 'string') return body;
      if (body && typeof body === 'object') {
        const values = Object.values(body).flat();
        if (values.length) return values.map(String).join(' ');
      }
      return `Erro ${error.status}: ${error.statusText || 'requisição inválida'}`;
    }
    return 'Não foi possível conectar à API.';
  }
}

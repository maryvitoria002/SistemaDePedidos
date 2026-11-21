import { HttpErrorResponse } from '@angular/common/http';

export class HttpApiConfig {
  readonly baseUrl = '/api';
}

export class ApiErrorMapper {
  map(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      const body = error.error;

      // Algumas telas enviam uma mensagem simples no campo error.
      if (body && typeof body === 'object' && 'error' in body) {
        const message = String((body as { error: unknown }).error);
        return this.mapStockMessage(message);
      }

      if (typeof body === 'string') return this.mapStockMessage(body);
      if (body && typeof body === 'object') {
        const values = Object.values(body).flat();
        if (values.length) {
          const firstMessage = String(values[0]);
          return this.mapStockMessage(firstMessage);
        }
      }
      return `Erro ${error.status}: ${error.statusText || 'requisição inválida'}`;
    }
    return 'Não foi possível conectar à API.';
  }

  private mapStockMessage(message: string): string {
    if (/estoque insuficiente/i.test(message)) {
      return 'Estoque insuficiente para este produto.';
    }
    if (/não possui estoque informado/i.test(message)) {
      return 'Este produto não possui estoque disponível.';
    }
    return message;
  }
}

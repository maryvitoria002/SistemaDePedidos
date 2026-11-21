import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { OrderApi } from '../api/order-api';
import { ClientApi } from '../api/client-api';
import { ProductApi } from '../api/product-api';
import { ApiErrorMapper } from '../api/http-api';
import { Cliente, Pedido, PedidoItem, Produto } from '../models';

@Component({
  standalone: true,
  selector: 'app-orders',
  imports: [FormsModule, RouterLink],
  templateUrl: './orders.html',
})
export class Orders implements OnInit {
  private ordersApi = inject(OrderApi);
  private clientsApi = inject(ClientApi);
  private productsApi = inject(ProductApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  pedidos: Pedido[] = [];
  clientes: Cliente[] = [];
  produtos: Produto[] = [];
  showForm = false;
  error = '';
  success = '';
  clienteId = '';
  produtoId = '';
  quantidade = 1;
  itens: PedidoItem[] = [{ produto: '', quantidade: 1 }];
  loading = false;

  ngOnInit(): void {
    this.carregar();
  }

  carregar(): void {
    this.error = '';
    this.loading = true;
    this.ordersApi.list().subscribe({
      next: pedidos => {
        this.pedidos = pedidos;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
    this.clientsApi.list().subscribe({
      next: clientes => this.clientes = clientes,
      error: error => this.error = this.errors.map(error),
    });
    this.productsApi.list().subscribe({
      next: produtos => this.produtos = produtos,
      error: error => this.error = this.errors.map(error),
    });
  }

  criar(): void {
    if (!this.clienteId || this.itens.some(item => !item.produto || item.quantidade <= 0)) {
      this.error = 'Selecione cliente e produtos válidos.';
      return;
    }
    this.ordersApi.create({
      cliente: this.clienteId,
      itens: this.itens,
    }).subscribe({
      next: () => {
        this.success = 'Pedido criado.';
        this.showForm = false;
        this.itens = [{ produto: '', quantidade: 1 }];
        this.carregar();
      },
      error: error => this.error = this.errors.map(error),
    });
  }

  cancelar(pedido: Pedido): void {
    this.ordersApi.cancel(pedido.id).subscribe({
      next: () => this.carregar(),
      error: error => this.error = this.errors.map(error),
    });
  }

  excluir(pedido: Pedido): void {
    if (!confirm('Excluir este pedido?')) return;
    this.ordersApi.delete(pedido.id).subscribe({
      next: () => this.carregar(),
      error: error => this.error = this.errors.map(error),
    });
  }

  nomeCliente(clienteId: string): string {
    return this.clientes.find(cliente => cliente.id === clienteId)?.nome ?? clienteId.slice(0, 8);
  }

  adicionarItem(): void {
    this.itens.push({ produto: '', quantidade: 1 });
  }

  removerItem(index: number): void {
    if (this.itens.length > 1) this.itens.splice(index, 1);
  }
}

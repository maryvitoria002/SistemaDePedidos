import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ClientApi } from '../api/client-api';
import { ApiErrorMapper } from '../api/http-api';
import { Cliente, Pedido } from '../models';

@Component({
  standalone: true,
  selector: 'app-clients',
  imports: [FormsModule],
  templateUrl: './clients.html',
})
export class Clients implements OnInit {
  private clientsApi = inject(ClientApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  clientes: Cliente[] = [];
  showForm = false;
  error = '';
  success = '';
  loading = false;
  nome = '';
  cpf = '';
  email = '';
  telefone = '';
  tipo: 'COMUM' | 'VIP' = 'COMUM';
  clienteSelecionado: Cliente | null = null;
  pedidosCliente: Pedido[] = [];
  loadingPedidos = false;

  ngOnInit(): void {
    this.carregar();
  }

  carregar(): void {
    this.error = '';
    this.loading = true;
    this.clientsApi.list().subscribe({
      next: clientes => {
        this.clientes = clientes;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }

  criar(): void {
    this.error = '';
    this.clientsApi.create({
      nome: this.nome,
      cpf: this.cpf,
      email: this.email,
      telefone: this.telefone,
      tipo: this.tipo,
    }).subscribe({
      next: () => {
        this.success = 'Cliente criado.';
        this.nome = this.cpf = this.email = this.telefone = '';
        this.tipo = 'COMUM';
        this.showForm = false;
        this.carregar();
      },
      error: error => this.error = this.errors.map(error),
    });
  }

  excluir(cliente: Cliente): void {
    if (!confirm(`Excluir ${cliente.nome}?`)) return;
    this.clientsApi.delete(cliente.id).subscribe({
      next: () => this.carregar(),
      error: error => this.error = this.errors.map(error),
    });
  }

  consultarPedidos(cliente: Cliente): void {
    this.clienteSelecionado = cliente;
    this.loadingPedidos = true;
    this.pedidosCliente = [];
    this.error = '';
    this.clientsApi.orders(cliente.id).subscribe({
      next: pedidos => {
        this.pedidosCliente = pedidos;
        this.loadingPedidos = false;
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.loadingPedidos = false;
        this.cdr.detectChanges();
      },
    });
  }
}

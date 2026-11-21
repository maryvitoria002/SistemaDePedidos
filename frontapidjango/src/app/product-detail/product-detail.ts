import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ProductApi } from '../api/product-api';
import { ClientApi } from '../api/client-api';
import { OrderApi } from '../api/order-api';
import { ApiErrorMapper } from '../api/http-api';
import { Cliente, Produto } from '../models';

@Component({
  standalone: true,
  selector: 'app-product-detail',
  imports: [FormsModule, RouterLink],
  templateUrl: './product-detail.html',
})
export class ProductDetail implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private productsApi = inject(ProductApi);
  private clientsApi = inject(ClientApi);
  private ordersApi = inject(OrderApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  produto?: Produto;
  clientes: Cliente[] = [];
  clienteId = '';
  quantidade = 1;
  preco = '';
  estoque: number | null = null;
  peso = '';
  tamanhoArquivo: number | null = null;
  error = '';
  success = '';

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) return;
    this.productsApi.get(id).subscribe({
      next: produto => {
        this.produto = produto;
        this.preco = produto.preco;
        this.estoque = produto.estoque;
        this.peso = produto.peso ?? '';
        this.tamanhoArquivo = produto.tamanho_arquivo;
        this.cdr.detectChanges();
      },
      error: error => this.error = this.errors.map(error),
    });
    this.clientsApi.list().subscribe({
      next: clientes => {
        this.clientes = clientes;
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.cdr.detectChanges();
      },
    });
  }

  criarPedido(): void {
    if (!this.produto || !this.clienteId) {
      this.error = 'Selecione um cliente.';
      return;
    }
    if (this.quantidade <= 0) {
      this.error = 'Informe uma quantidade maior que zero.';
      return;
    }
    if (this.produto.tipo === 'FISICO') {
      const estoque = this.produto.estoque ?? 0;
      if (estoque < this.quantidade) {
        this.error = `Estoque insuficiente para ${this.produto.nome}. Disponível: ${estoque}.`;
        return;
      }
    }
    this.error = '';
    this.ordersApi.create({
      cliente: this.clienteId,
      itens: [{ produto: this.produto.id, quantidade: this.quantidade }],
    }).subscribe({
      next: () => this.router.navigate(['/pedidos']),
      error: error => this.error = this.errors.map(error),
    });
  }

  salvar(): void {
    if (!this.produto) return;
    const body: Record<string, unknown> = { preco: this.preco };
    if (this.produto.tipo === 'FISICO') {
      body['peso'] = this.peso;
      body['estoque'] = this.estoque;
    } else {
      body['tamanho_arquivo'] = this.tamanhoArquivo;
    }
    this.productsApi.update(this.produto.id, body).subscribe({
      next: produto => {
        this.produto = produto;
        this.success = 'Produto atualizado.';
      },
      error: error => this.error = this.errors.map(error),
    });
  }

  excluir(): void {
    if (!this.produto) return;
    if (!confirm('Excluir este produto?')) return;
    this.productsApi.delete(this.produto.id).subscribe({
      next: () => this.router.navigate(['/']),
      error: error => this.error = this.errors.map(error),
    });
  }
}

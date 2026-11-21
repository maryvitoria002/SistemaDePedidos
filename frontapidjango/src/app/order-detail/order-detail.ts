import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { OrderApi } from '../api/order-api';
import { ClientApi } from '../api/client-api';
import { ProductApi } from '../api/product-api';
import { ApiErrorMapper } from '../api/http-api';
import { Cliente, Pedido, Produto } from '../models';

@Component({
  standalone: true,
  selector: 'app-order-detail',
  imports: [RouterLink],
  templateUrl: './order-detail.html',
})
export class OrderDetail implements OnInit {
  private route = inject(ActivatedRoute);
  private ordersApi = inject(OrderApi);
  private clientsApi = inject(ClientApi);
  private productsApi = inject(ProductApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  pedido?: Pedido;
  cliente?: Cliente;
  produtos: Produto[] = [];
  error = '';

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) return;

    this.ordersApi.get(id).subscribe({
      next: pedido => {
        this.pedido = pedido;
        this.clientsApi.get(pedido.cliente).subscribe({
          next: cliente => {
            this.cliente = cliente;
            this.cdr.detectChanges();
          },
          error: error => this.error = this.errors.map(error),
        });
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.cdr.detectChanges();
      },
    });

    this.productsApi.list().subscribe({
      next: produtos => {
        this.produtos = produtos;
        this.cdr.detectChanges();
      },
      error: error => {
        this.error = this.errors.map(error);
        this.cdr.detectChanges();
      },
    });
  }

  nomeProduto(id: string): string {
    return this.produtos.find(produto => produto.id === id)?.nome ?? id.slice(0, 8);
  }

  precoUnitario(id: string): string {
    return this.produtos.find(produto => produto.id === id)?.preco ?? '0.00';
  }

  totalProduto(id: string, quantidade: number): string {
    const preco = Number(this.precoUnitario(id));
    return (preco * quantidade).toFixed(2);
  }
}

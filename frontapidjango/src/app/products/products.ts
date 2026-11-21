import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ProductApi } from '../api/product-api';
import { ApiErrorMapper } from '../api/http-api';
import { Produto } from '../models';

@Component({
  standalone: true,
  selector: 'app-products',
  imports: [FormsModule, RouterLink],
  templateUrl: './products.html',
})
export class Products implements OnInit {
  private productsApi = inject(ProductApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  produtos: Produto[] = [];
  showForm = false;
  error = '';
  success = '';
  loading = false;
  nome = '';
  preco = '';
  tipo: 'FISICO' | 'DIGITAL' = 'FISICO';
  peso = '';
  estoque: number | null = 0;
  tamanhoArquivo: number | null = null;

  ngOnInit(): void {
    this.carregar();
  }

  carregar(): void {
    this.error = '';
    this.loading = true;
    this.productsApi.list().subscribe({
      next: produtos => {
        this.produtos = produtos;
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
    this.success = '';
    const body: Record<string, unknown> = {
      nome: this.nome,
      preco: this.preco,
      tipo: this.tipo,
    };
    if (this.tipo === 'FISICO') {
      body['peso'] = this.peso;
      body['estoque'] = this.estoque;
    } else {
      body['tamanho_arquivo'] = this.tamanhoArquivo;
    }

    this.productsApi.create(body).subscribe({
      next: () => {
        this.success = 'Produto criado.';
        this.nome = '';
        this.preco = '';
        this.peso = '';
        this.estoque = 0;
        this.tamanhoArquivo = null;
        this.showForm = false;
        this.carregar();
      },
      error: error => this.error = this.errors.map(error),
    });
  }
}

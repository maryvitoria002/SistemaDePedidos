import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { OrderApi } from '../api/order-api';
import { ApiErrorMapper } from '../api/http-api';
import { Pedido } from '../models';

@Component({
  standalone: true,
  selector: 'app-payment',
  imports: [FormsModule, RouterLink],
  templateUrl: './payment.html',
})
export class Payment implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private ordersApi = inject(OrderApi);
  private errors = inject(ApiErrorMapper);
  private cdr = inject(ChangeDetectorRef);
  pedido?: Pedido;
  formaPagamento: 'PIX' | 'CARTAO_CREDITO' | 'BOLETO' = 'PIX';
  error = '';

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) return;
    this.ordersApi.get(id).subscribe({
      next: pedido => {
        this.pedido = pedido;
        this.cdr.detectChanges();
      },
      error: error => this.error = this.errors.map(error),
    });
  }

  pagar(): void {
    if (!this.pedido) return;
    this.error = '';
    this.ordersApi.pay(this.pedido.id, this.formaPagamento).subscribe({
      next: pedido => {
        this.pedido = pedido;
        this.router.navigate(['/pedidos']);
      },
      error: error => this.error = this.errors.map(error),
    });
  }
}

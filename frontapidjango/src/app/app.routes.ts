import { Routes } from '@angular/router';
import { Products } from './products/products';
import { ProductDetail } from './product-detail/product-detail';
import { Clients } from './clients/clients';
import { Orders } from './orders/orders';
import { Payment } from './payment/payment';
import { OrderDetail } from './order-detail/order-detail';

export const routes: Routes = [
  { path: '', component: Products, title: 'Produtos' },
  { path: 'produto/:id', component: ProductDetail, title: 'Produto' },
  { path: 'clientes', component: Clients, title: 'Clientes' },
  { path: 'pedidos', component: Orders, title: 'Pedidos' },
  { path: 'pedidos/:id', component: OrderDetail, title: 'Detalhes do pedido' },
  { path: 'pedidos/:id/pagar', component: Payment, title: 'Pagamento' },
  { path: '**', redirectTo: '' },
];

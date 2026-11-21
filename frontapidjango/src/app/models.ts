export interface Produto {
  id: string;
  nome: string;
  preco: string;
  tipo: 'FISICO' | 'DIGITAL';
  estoque: number | null;
  tamanho_arquivo: number | null;
  peso: string | null;
}

export interface Cliente {
  id: string;
  nome: string;
  cpf: string;
  email: string;
  telefone: string;
  tipo: 'COMUM' | 'VIP';
}

export interface Pedido {
  id: string;
  cliente: string;
  status: 'CRIADO' | 'PAGO' | 'CANCELADO';
  produtos: string[];
  itens?: PedidoItem[];
  valor_total: string;
  valor_com_desconto?: string;
  status_pagamento: 'PENDENTE' | 'PAGO' | 'CANCELADO';
  forma_pagamento: 'PIX' | 'CARTAO_CREDITO' | 'BOLETO' | null;
  valor_pago: string;
}

export interface PedidoItem {
  produto: string;
  quantidade: number;
}

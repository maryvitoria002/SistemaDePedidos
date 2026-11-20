from django.db import transaction
from decimal import Decimal

from .models import Pedido, PedidoProduto
from .payments import PaymentFactory
from produto.models import Produto, TipoProduto


class PedidoRepository:
    def __init__(self, pedido_manager=None, item_manager=None):
        self.pedido_manager = pedido_manager or Pedido.objects
        self.item_manager = item_manager or PedidoProduto.objects

    def listar(self):
        return self.pedido_manager.prefetch_related('itens__produto').all()

    def buscar(self, pedido_id):
        return self.pedido_manager.prefetch_related('itens__produto').get(pk=pedido_id)

    def criar(self, **dados):
        return self.pedido_manager.create(**dados)

    def criar_item(self, **dados):
        return self.item_manager.create(**dados)

    def excluir(self, pedido):
        pedido.delete()


class PedidoService:
    def __init__(self, repository=None):
        self.repository = repository or PedidoRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, pedido_id):
        return self.repository.buscar(pedido_id)

    @transaction.atomic
    def criar(self, *, cliente, produto=None, quantidade=None, itens=None, status=None):
        itens_normalizados = []

        if itens:
            itens_normalizados = [
                (item['produto'], item['quantidade'])
                for item in itens
            ]
        elif produto is not None and quantidade is not None:
            itens_normalizados = [(produto, quantidade)]
        else:
            raise ValueError('Informe pelo menos um item para o pedido.')

        totais_por_produto = {}
        for produto_item, quantidade_item in itens_normalizados:
            if quantidade_item <= 0:
                raise ValueError('A quantidade do pedido deve ser maior que zero.')
            totais_por_produto[produto_item.id] = (
                totais_por_produto.get(produto_item.id, 0) + quantidade_item
            )

        for produto_id, quantidade_total in totais_por_produto.items():
            produto_item = Produto.objects.select_for_update().get(pk=produto_id)
            if produto_item.tipo == TipoProduto.FISICO:
                if produto_item.estoque is None:
                    raise ValueError(
                        f'O produto {produto_item.nome} não possui estoque informado.'
                    )
                if produto_item.estoque < quantidade_total:
                    raise ValueError(
                        f'Estoque insuficiente para o produto {produto_item.nome}.'
                    )

        dados = {'cliente': cliente}
        if status is not None:
            dados['status'] = status
        pedido = self.repository.criar(**dados)

        for produto_item, quantidade_item in itens_normalizados:
            produto_atualizado = Produto.objects.select_for_update().get(pk=produto_item.id)
            if produto_atualizado.tipo == TipoProduto.FISICO:
                produto_atualizado.estoque -= quantidade_item
                produto_atualizado.save(update_fields=['estoque'])

            self.repository.criar_item(
                pedido=pedido,
                produto=produto_atualizado,
                quantidade=quantidade_item,
            )
        return pedido

    def atualizar(self, pedido, **dados):
        if pedido.status == 'PAGO':
            raise ValueError('Um pedido pago não pode ser alterado.')
        if pedido.status == 'CANCELADO':
            raise ValueError('Um pedido cancelado não pode ser alterado.')
        for campo, valor in dados.items():
            setattr(pedido, campo, valor)
        pedido.save()
        return pedido

    @transaction.atomic
    def pagar(self, pedido, forma_pagamento):
        if pedido.status == 'CANCELADO':
            raise ValueError('Um pedido cancelado não pode receber pagamento.')
        if not pedido.itens.exists():
            raise ValueError('O pedido deve possuir pelo menos um item.')
        if pedido.status == 'PAGO':
            raise ValueError('O pedido já está pago.')

        valor = PaymentFactory.calcular(forma_pagamento, pedido.valor_com_desconto)
        pedido.forma_pagamento = forma_pagamento
        pedido.valor_pago = valor.quantize(Decimal('0.01'))
        pedido.status_pagamento = 'PAGO'
        pedido.status = 'PAGO'
        pedido.save()
        return pedido

    @transaction.atomic
    def cancelar(self, pedido):
        if pedido.status == 'PAGO':
            raise ValueError('Um pedido pago não pode ser cancelado.')
        if pedido.status == 'CANCELADO':
            raise ValueError('O pedido já está cancelado.')

        pedido = Pedido.objects.select_for_update().prefetch_related('itens__produto').get(pk=pedido.pk)
        for item in pedido.itens.all():
            produto = Produto.objects.select_for_update().get(pk=item.produto_id)
            if produto.tipo == TipoProduto.FISICO:
                produto.estoque = (produto.estoque or 0) + item.quantidade
                produto.save(update_fields=['estoque'])

        pedido.status = 'CANCELADO'
        pedido.status_pagamento = 'CANCELADO'
        pedido.save()
        return pedido

    @transaction.atomic
    def excluir(self, pedido):
        if pedido.status in ('PAGO', 'CANCELADO'):
            raise ValueError('Pedidos pagos ou cancelados não podem ser excluídos.')

        pedido = Pedido.objects.select_for_update().prefetch_related('itens__produto').get(pk=pedido.pk)
        for item in pedido.itens.all():
            produto = Produto.objects.select_for_update().get(pk=item.produto_id)
            if produto.tipo == TipoProduto.FISICO:
                produto.estoque = (produto.estoque or 0) + item.quantidade
                produto.save(update_fields=['estoque'])
        self.repository.excluir(pedido)

from django.db import models
import uuid
from decimal import Decimal
from django.db.models import Sum, F

# Create your models here.

class StatusPedido(models.TextChoices):
    CRIADO = 'CRIADO',
    PAGO = 'PAGO',
    CANCELADO = 'CANCELADO',

class StatusPagamento(models.TextChoices):
    PENDENTE = 'PENDENTE'
    PAGO = 'PAGO'
    CANCELADO = 'CANCELADO'

class FormaPagamento(models.TextChoices):
    PIX = 'PIX'
    CARTAO_CREDITO = 'CARTAO_CREDITO'
    BOLETO = 'BOLETO'

class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    cliente = models.ForeignKey(
        'cliente.Cliente',
        on_delete=models.CASCADE,
        related_name='pedidos',
    )
    status = models.CharField(max_length=10, choices=StatusPedido.choices, default=StatusPedido.CRIADO)
    status_pagamento = models.CharField(
        max_length=10,
        choices=StatusPagamento.choices,
        default=StatusPagamento.PENDENTE,
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FormaPagamento.choices,
        blank=True,
        null=True,
    )
    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    produtos = models.ManyToManyField('produto.Produto', through='PedidoProduto', related_name='pedidos')
    @property
    def valor_total(self):
        return self.itens.aggregate(
            total=Sum(F('quantidade') * F('produto__preco'))
        )['total'] or 0

    @property
    def valor_com_desconto(self):
        from .discounts import DescontoComercial

        total = self.valor_total
        desconto = DescontoComercial.maior_desconto(self)
        return total * (Decimal('1') - desconto)

class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('produto.Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)


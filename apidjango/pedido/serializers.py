from rest_framework import serializers
from produto.models import Produto
from .models import Pedido, StatusPedido, StatusPagamento, FormaPagamento


class PedidoItemSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    quantidade = serializers.IntegerField(min_value=1)


class PedidoItemOutputSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)


class PedidoSerializer(serializers.ModelSerializer):
    produto = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(),
        write_only=True,
        required=False,
    )
    quantidade = serializers.IntegerField(write_only=True, required=False, min_value=1)
    itens = PedidoItemSerializer(many=True, required=False)
    valor_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    class Meta:
        model = Pedido
        fields = (
            'id', 'cliente', 'status', 'produtos', 'produto',
            'quantidade', 'itens', 'valor_total',
            'status_pagamento', 'forma_pagamento', 'valor_pago',
        )

    def validate_status(self, value):
        if value not in StatusPedido.values:
            raise serializers.ValidationError("Status inválido para o pedido.")
        if value in (StatusPedido.PAGO, StatusPedido.CANCELADO):
            raise serializers.ValidationError(
                'Use o endpoint de pagamento ou cancelamento para alterar o status.'
            )
        return value

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade do pedido deve ser maior que zero.")
        return value
    
    def validate(self, attrs):
        is_create = self.instance is None

        if is_create:
            itens = attrs.get('itens')
            produto = attrs.get('produto')
            quantidade = attrs.get('quantidade')

            if itens and (produto is not None or quantidade is not None):
                raise serializers.ValidationError(
                    'Use itens ou produto/quantidade, não os dois formatos.'
                )

            if itens:
                return attrs

            if produto is None or quantidade is None:
                raise serializers.ValidationError(
                    'Informe itens ou os campos produto e quantidade.'
                )

            return attrs

        if not is_create and attrs.get('produto') is not None:
            raise serializers.ValidationError(
                {'produto': 'O produto do pedido não pode ser alterado.'} 
            )

        if not is_create and attrs.get('cliente') is not None:
            raise serializers.ValidationError(
                {'cliente': 'O cliente do pedido não pode ser alterado.'} 
            )

        
        if not is_create and attrs.get('quantidade') is not None:
            raise serializers.ValidationError(
                {'quantidade': 'A quantidade do pedido não pode ser alterada.'}
            )
        if not is_create and attrs.get('itens') is not None:
            raise serializers.ValidationError(
                {'itens': 'Os itens do pedido não podem ser alterados.'}
            )
        return attrs

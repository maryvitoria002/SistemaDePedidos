from rest_framework import serializers
from .models import Produto, TipoProduto
from .validators import ProdutoValidator

class ProdutoSerializer(serializers.ModelSerializer):
    preco = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
    )
    tipo = serializers.ChoiceField(
        choices=TipoProduto.choices,
        required=False,
    )

    class Meta:
        model = Produto
        fields = '__all__'

    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço do produto não pode ser negativo.")
        return value

    def validate_nome(self, value):
        if not value:
            raise serializers.ValidationError("O nome do produto não pode ser vazio.")
        return value

    def validate(self, attrs):
        return ProdutoValidator.validate(attrs, self.instance)
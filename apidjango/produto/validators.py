from rest_framework import serializers
from .models import TipoProduto


class ProdutoValidator:
    validators = {}

    @classmethod
    def validate(cls, attrs, instance=None):
        if instance is None:
            for campo in ('nome', 'preco', 'tipo'):
                if campo not in attrs:
                    raise serializers.ValidationError(
                        {campo: 'Este campo é obrigatório.'}
                    )

        tipo = attrs.get('tipo', getattr(instance, 'tipo', None))
        validator = cls.validators.get(tipo)
        if validator:
            validator.validate(attrs, instance)
        return attrs


class ProdutoFisicoValidator:
    @staticmethod
    def validate(attrs, instance=None):
        if instance is None:
            for campo in ('peso', 'estoque'):
                if campo not in attrs or attrs[campo] is None:
                    raise serializers.ValidationError(
                        {campo: 'Este campo é obrigatório.'}
                    )
        if attrs.get('peso') is not None and attrs['peso'] <= 0:
            raise serializers.ValidationError(
                {'peso': 'O peso do produto físico deve ser maior que zero.'}
            )
        if attrs.get('estoque') is not None and attrs['estoque'] < 0:
            raise serializers.ValidationError(
                {'estoque': 'O estoque não pode ser negativo.'}
            )
        if attrs.get('tamanho_arquivo') is not None:
            raise serializers.ValidationError(
                {'tamanho_arquivo': 'Produto físico não deve ter tamanho de arquivo.'}
            )


class ProdutoDigitalValidator:
    @staticmethod
    def validate(attrs, instance=None):
        if instance is None and (
            'tamanho_arquivo' not in attrs or attrs['tamanho_arquivo'] is None
        ):
            raise serializers.ValidationError(
                {'tamanho_arquivo': 'Este campo é obrigatório.'}
            )
        if attrs.get('tamanho_arquivo') is not None and attrs['tamanho_arquivo'] <= 0:
            raise serializers.ValidationError(
                {'tamanho_arquivo': 'O tamanho deve ser maior que zero.'}
            )
        if attrs.get('peso') is not None:
            raise serializers.ValidationError(
                {'peso': 'Produto digital não deve ter peso.'}
            )
        if attrs.get('estoque') is not None:
            raise serializers.ValidationError(
                {'estoque': 'Produto digital não deve ter estoque.'}
            )


ProdutoValidator.validators = {
    TipoProduto.FISICO: ProdutoFisicoValidator,
    TipoProduto.DIGITAL: ProdutoDigitalValidator,
}

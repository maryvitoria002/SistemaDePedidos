from django.test import TestCase
from .serializers import ProdutoSerializer


class ProdutoSerializerTests(TestCase):
    def test_exige_dados_especificos_para_produto_fisico(self):
        serializer = ProdutoSerializer(data={
            'nome': 'Livro',
            'preco': '10.00',
            'tipo': 'FISICO',
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('peso', serializer.errors)

    def test_rejeita_preco_negativo(self):
        serializer = ProdutoSerializer(data={
            'nome': 'Livro',
            'preco': '-1.00',
            'tipo': 'FISICO',
            'peso': '1.00',
            'estoque': 1,
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('preco', serializer.errors)
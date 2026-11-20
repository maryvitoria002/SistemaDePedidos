from django.test import TestCase
from .serializers import ClienteSerializer
from .models import Cliente
from pedido.models import Pedido


class ClienteSerializerTests(TestCase):
    def test_rejeita_nome_em_branco(self):
        serializer = ClienteSerializer(data={'nome': ' ', 'email': 'a@a.com'})

        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)

    def test_cliente_pode_acessar_seus_pedidos(self):
        cliente = Cliente.objects.create(
            nome='Maria',
            email='maria@example.com',
        )
        Pedido.objects.create(cliente=cliente)

        self.assertEqual(cliente.pedidos.count(), 1)

from django.test import TestCase
from decimal import Decimal
from cliente.models import Cliente
from produto.models import Produto
from .models import Pedido
from .services import PedidoService
from .discounts import DescontoComercial
from .payments import PaymentFactory


class PedidoServiceTests(TestCase):
    def test_reduz_estoque_na_criacao_e_retorna_no_cancelamento(self):
        cliente = Cliente.objects.create(nome='Maria', email='estoque@example.com')
        produto = Produto.objects.create(
            nome='Livro',
            preco='10.00',
            tipo='FISICO',
            peso='1.00',
            estoque=5,
        )

        pedido = PedidoService().criar(
            cliente=cliente,
            produto=produto,
            quantidade=2,
        )
        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 3)

        PedidoService().cancelar(pedido)
        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 5)

    def test_cria_pedido_com_multiplos_produtos(self):
        cliente = Cliente.objects.create(nome='Maria', email='multi@example.com')
        livro = Produto.objects.create(
            nome='Livro',
            preco='10.00',
            tipo='FISICO',
            peso='1.00',
            estoque=5,
        )
        curso = Produto.objects.create(
            nome='Curso',
            preco='20.00',
            tipo='DIGITAL',
            tamanho_arquivo=100,
        )

        pedido = PedidoService().criar(
            cliente=cliente,
            itens=[
                {'produto': livro, 'quantidade': 2},
                {'produto': curso, 'quantidade': 1},
            ],
        )

        self.assertEqual(pedido.itens.count(), 2)
        self.assertEqual(pedido.valor_total, Decimal('40.00'))
        livro.refresh_from_db()
        self.assertEqual(livro.estoque, 3)

    def test_nao_cria_pedido_sem_estoque_suficiente(self):
        cliente = Cliente.objects.create(nome='Maria', email='semestoque@example.com')
        produto = Produto.objects.create(
            nome='Livro',
            preco='10.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )

        with self.assertRaises(ValueError):
            PedidoService().criar(
                cliente=cliente,
                produto=produto,
                quantidade=2,
            )

    def test_cria_pedido_com_item(self):
        cliente = Cliente.objects.create(nome='Maria', email='maria@example.com')
        produto = Produto.objects.create(
            nome='Livro',
            preco='10.00',
            tipo='FISICO',
            peso='1.00',
            estoque=2,
        )

        pedido = PedidoService().criar(
            cliente=cliente,
            produto=produto,
            quantidade=2,
        )

        self.assertEqual(pedido.itens.count(), 1)
        self.assertEqual(pedido.valor_total, 20)

    def test_cliente_vip_recebe_maior_desconto_comercial(self):
        cliente = Cliente.objects.create(
            nome='Maria VIP',
            email='vip@example.com',
            tipo='VIP',
        )
        produto = Produto.objects.create(
            nome='Produto caro',
            preco='600.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )
        pedido = PedidoService().criar(
            cliente=cliente,
            produto=produto,
            quantidade=1,
        )

        self.assertEqual(DescontoComercial.maior_desconto(pedido), Decimal('0.10'))
        self.assertEqual(pedido.valor_com_desconto, Decimal('540.00'))

    def test_pix_aplica_desconto_apos_desconto_comercial(self):
        cliente = Cliente.objects.create(
            nome='Maria',
            email='maria2@example.com',
        )
        produto = Produto.objects.create(
            nome='Produto',
            preco='600.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )
        pedido = PedidoService().criar(
            cliente=cliente,
            produto=produto,
            quantidade=1,
        )
        valor = PaymentFactory.calcular('PIX', pedido.valor_com_desconto)

        self.assertEqual(valor, Decimal('541.50'))

    def test_cartao_aplica_acrescimo_de_tres_porcento(self):
        valor = PaymentFactory.calcular('CARTAO_CREDITO', Decimal('100.00'))
        self.assertEqual(valor, Decimal('103.00'))

    def test_pagar_cartao_registra_valor_pago_com_acrescimo(self):
        cliente = Cliente.objects.create(nome='Maria', email='cartao@example.com')
        produto = Produto.objects.create(
            nome='Produto',
            preco='100.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )
        pedido = PedidoService().criar(
            cliente=cliente,
            produto=produto,
            quantidade=1,
        )

        pedido = PedidoService().pagar(pedido, 'CARTAO_CREDITO')

        self.assertEqual(pedido.valor_pago, Decimal('103.00'))

    def test_cartao_aplica_acrescimo_depois_do_desconto_vip(self):
        cliente = Cliente.objects.create(
            nome='Maria VIP',
            email='cartao-vip@example.com',
            tipo='VIP',
        )
        pedido = PedidoService().criar(
            cliente=cliente,
            itens=[
                {
                    'produto': Produto.objects.create(
                        nome='Toalha',
                        preco='13.00',
                        tipo='FISICO',
                        peso='1.00',
                        estoque=3,
                    ),
                    'quantidade': 3,
                },
                {
                    'produto': Produto.objects.create(
                        nome='Jacubitaba',
                        preco='20.00',
                        tipo='FISICO',
                        peso='1.00',
                        estoque=2,
                    ),
                    'quantidade': 2,
                },
                {
                    'produto': Produto.objects.create(
                        nome='The last of us',
                        preco='31.00',
                        tipo='FISICO',
                        peso='1.00',
                        estoque=1,
                    ),
                    'quantidade': 1,
                },
            ],
        )

        pedido = PedidoService().pagar(pedido, 'CARTAO_CREDITO')

        self.assertEqual(pedido.valor_total, Decimal('110.00'))
        self.assertEqual(pedido.valor_com_desconto, Decimal('99.00'))
        self.assertEqual(pedido.valor_pago, Decimal('101.97'))

    def test_boleto_nao_altera_valor(self):
        valor = PaymentFactory.calcular('BOLETO', Decimal('100.00'))
        self.assertEqual(valor, Decimal('100.00'))

    def test_pedido_pago_nao_pode_ser_atualizado(self):
        cliente = Cliente.objects.create(nome='Maria', email='maria3@example.com')
        produto = Produto.objects.create(
            nome='Produto',
            preco='100.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )
        pedido = PedidoService().criar(cliente=cliente, produto=produto, quantidade=1)
        pedido = PedidoService().pagar(pedido, 'PIX')

        with self.assertRaises(ValueError):
            PedidoService().atualizar(pedido, status='CRIADO')

    def test_pedido_cancelado_nao_pode_receber_pagamento(self):
        cliente = Cliente.objects.create(nome='Maria', email='maria4@example.com')
        produto = Produto.objects.create(
            nome='Produto',
            preco='100.00',
            tipo='FISICO',
            peso='1.00',
            estoque=1,
        )
        pedido = PedidoService().criar(cliente=cliente, produto=produto, quantidade=1)
        pedido = PedidoService().cancelar(pedido)

        with self.assertRaises(ValueError):
            PedidoService().pagar(pedido, 'PIX')


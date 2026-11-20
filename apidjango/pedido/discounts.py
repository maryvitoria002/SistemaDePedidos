from decimal import Decimal


class DiscountPolicy:
    def calcular(self, pedido) -> Decimal:
        raise NotImplementedError


class SemDesconto(DiscountPolicy):
    def calcular(self, pedido) -> Decimal:
        return Decimal('0')


class DescontoVIP(DiscountPolicy):
    def calcular(self, pedido) -> Decimal:
        if pedido.cliente.tipo == 'VIP':
            return Decimal('0.10')
        return Decimal('0')


class DescontoCompraAcimaDe500(DiscountPolicy):
    def calcular(self, pedido) -> Decimal:
        if pedido.valor_total >= Decimal('500.00'):
            return Decimal('0.05')
        return Decimal('0')


class DescontoComercial:
    policies = (
        DescontoVIP(),
        DescontoCompraAcimaDe500(),
    )

    @classmethod
    def maior_desconto(cls, pedido) -> Decimal:
        return max(policy.calcular(pedido) for policy in cls.policies)

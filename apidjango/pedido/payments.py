from decimal import Decimal


class PaymentStrategy:
    def aplicar(self, valor: Decimal) -> Decimal:
        raise NotImplementedError


class PixPayment(PaymentStrategy):
    def aplicar(self, valor: Decimal) -> Decimal:
        return valor * Decimal('0.95')


class CreditCardPayment(PaymentStrategy):
    def aplicar(self, valor: Decimal) -> Decimal:
        return valor * Decimal('1.03')


class BoletoPayment(PaymentStrategy):
    def aplicar(self, valor: Decimal) -> Decimal:
        return valor


class PaymentFactory:
    strategies = {
        'PIX': PixPayment(),
        'CARTAO_CREDITO': CreditCardPayment(),
        'BOLETO': BoletoPayment(),
    }

    @classmethod
    # serve para registrar novas estratégias de pagamento, 
    # caso seja necessário adicionar mais formas de pagamento no futuro.
    def registrar(cls, codigo: str, strategy: PaymentStrategy) -> None:
        cls.strategies[codigo] = strategy

    @classmethod
    def calcular(cls, codigo: str, valor: Decimal) -> Decimal:
        strategy = cls.strategies.get(codigo)
        if strategy is None:
            raise ValueError('Forma de pagamento inválida.')
        return strategy.aplicar(valor)

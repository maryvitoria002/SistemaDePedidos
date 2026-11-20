from .models import Cliente


class ClienteRepository:
    def __init__(self, manager=None):
        self.manager = manager or Cliente.objects

    def listar(self):
        return self.manager.all()

    def buscar(self, cliente_id):
        return self.manager.get(pk=cliente_id)

    def buscar_pedidos(self, cliente_id):
        return self.manager.get(pk=cliente_id).pedidos.all()

    def criar(self, **dados):
        return self.manager.create(**dados)

    def excluir(self, cliente):
        cliente.delete()


class ClienteService:
    def __init__(self, repository=None):
        self.repository = repository or ClienteRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, cliente_id):
        return self.repository.buscar(cliente_id)

    def buscar_pedidos(self, cliente_id):
        return self.repository.buscar_pedidos(cliente_id)

    def criar(self, **dados):
        return self.repository.criar(**dados)

    def atualizar(self, cliente, **dados):
        for campo, valor in dados.items():
            setattr(cliente, campo, valor)
        cliente.save()
        return cliente

    def excluir(self, cliente):
        self.repository.excluir(cliente)

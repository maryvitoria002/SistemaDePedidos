# Essa classe é responsável por interagir com o banco de dados para realizar operações relacionadas ao modelo Produto.
#  Ela encapsula a lógica de acesso aos dados, permitindo que outras partes do sistema interajam com os produtos sem
#  precisar conhecer os detalhes de como os dados são armazenados ou recuperados.

from .models import Produto


class ProdutoRepository:
    def __init__(self, manager=None):
        self.manager = manager or Produto.objects

    def listar(self):
        return self.manager.all()

    def buscar(self, produto_id):
        return self.manager.get(pk=produto_id)

    def criar(self, **dados):
        return self.manager.create(**dados)

    def excluir(self, produto):
        produto.delete()


class ProdutoService:
    def __init__(self, repository=None):
        self.repository = repository or ProdutoRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, produto_id):
        return self.repository.buscar(produto_id)

    def criar(self, **dados):
        return self.repository.criar(**dados)

    def atualizar(self, produto, **dados):
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        produto.save()
        return produto

    def excluir(self, produto):
        self.repository.excluir(produto)

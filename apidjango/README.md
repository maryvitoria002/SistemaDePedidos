# API Django - Sistema de Pedidos

<p align="center">
  <strong>API REST para cadastro de clientes, produtos e pedidos</strong>
</p>

<p align="center">
  <a href="https://github.com/maryvitoria002/apidjango">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-apidjango-181717?logo=github&logoColor=white">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/django-6.1.3-0C4B33?logo=django&logoColor=white">
  <img alt="DRF" src="https://img.shields.io/badge/Django_REST_Framework-3.18.3-a30000?logo=django&logoColor=white">
  <img alt="Banco de dados" src="https://img.shields.io/badge/database-SQLite-003B57?logo=sqlite&logoColor=white">
</p>

<p align="center">
  Uma API desenvolvida com Django e Django REST Framework para gerenciar o fluxo comercial de clientes, produtos físicos e digitais e pedidos com cálculo de descontos e formas de pagamento.
</p>

---

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de clientes
- Cadastro de clientes comuns e VIP
- Consulta dos pedidos associados a um cliente
- Cadastro de produtos físicos ou digitais
- Validações específicas para peso, estoque e tamanho de arquivo
- Criação e gerenciamento de pedidos
- Cálculo automático do valor total e do valor com desconto
- Desconto de 10% para clientes VIP
- Desconto de 5% para compras acima de R$ 500,00
- Pagamento por PIX, cartão de crédito ou boleto
- Regras de ciclo de vida para pedidos criados, pagos e cancelados
- Painel administrativo do Django

## Tecnologias

- **Python 3.12+**
- **Django 6.1.3**
- **Django REST Framework 3.18.3**
- **django-cors-headers 4.9.0**
- **SQLite**
- **Arquitetura em camadas** com models, serializers, services, repositories e strategies

## Estrutura do projeto

```text
apidjango/
├── cliente/         # Clientes comuns e VIP
├── pedido/          # Pedidos, itens, descontos e pagamentos
├── produto/         # Produtos físicos e digitais
├── pedidosis/       # Configuração principal do projeto
├── db.sqlite3       # Banco local de desenvolvimento
└── manage.py
```

## Primeiros passos

### Pré-requisitos

- Python 3.12 ou superior
- Git
- Pip

### Instalação no Windows

```powershell
git clone https://github.com/maryvitoria002/apidjango.git
cd apidjango

python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install Django==6.1.3 djangorestframework==3.18.3 django-cors-headers==4.9.0

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Instalação no Linux/macOS

```bash
git clone https://github.com/maryvitoria002/apidjango.git
cd apidjango

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install Django==6.1.3 djangorestframework==3.18.3 django-cors-headers==4.9.0

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A aplicação será disponibilizada em `http://127.0.0.1:8000/`.

O painel administrativo estará disponível em `http://127.0.0.1:8000/admin/`.

## Endpoints da API

Todos os recursos identificados por UUID são acessados por seu ID.

### Produtos

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/produto/` | Lista os produtos |
| `GET` | `/produto/<uuid:id>/` | Busca um produto |
| `POST` | `/produto/create/` | Cria um produto |
| `PUT` | `/produto/<uuid:id>/update/` | Atualiza parcialmente um produto |
| `DELETE` | `/produto/<uuid:id>/delete/` | Remove um produto |

Exemplo de produto físico:

```json
{
  "nome": "Livro de Python",
  "preco": "89.90",
  "tipo": "FISICO",
  "peso": "0.5",
  "estoque": 10
}
```

Exemplo de produto digital:

```json
{
  "nome": "Curso de Django",
  "preco": "149.90",
  "tipo": "DIGITAL",
  "tamanho_arquivo": 250
}
```

### Clientes

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/cliente/` | Lista os clientes |
| `GET` | `/cliente/<uuid:id>/` | Busca um cliente |
| `GET` | `/cliente/<uuid:id>/pedidos/` | Lista os pedidos do cliente |
| `POST` | `/cliente/create/` | Cria um cliente |
| `PUT` | `/cliente/<uuid:id>/update/` | Atualiza parcialmente um cliente |
| `DELETE` | `/cliente/<uuid:id>/delete/` | Remove um cliente |

Exemplo de cliente:

```json
{
  "nome": "Maria Silva",
  "cpf": "12345678901",
  "email": "maria@example.com",
  "telefone": "11999999999",
  "tipo": "VIP"
}
```

### Pedidos

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/pedido/` | Lista os pedidos |
| `GET` | `/pedido/<uuid:id>/` | Busca um pedido |
| `POST` | `/pedido/create/` | Cria um pedido com um item |
| `PUT` | `/pedido/<uuid:id>/update/` | Atualiza campos permitidos |
| `DELETE` | `/pedido/<uuid:id>/delete/` | Remove pedidos elegíveis |
| `POST` | `/pedido/<uuid:id>/pagar/` | Efetua o pagamento |
| `POST` | `/pedido/<uuid:id>/cancelar/` | Cancela o pedido |

Exemplo de criação:

```json
{
  "cliente": "uuid-do-cliente",
  "itens": [
    {
      "produto": "uuid-do-produto-1",
      "quantidade": 2
    },
    {
      "produto": "uuid-do-produto-2",
      "quantidade": 1
    }
  ]
}
```

O formato antigo com `produto` e `quantidade` continua aceito.

Exemplo de pagamento:

```json
{
  "forma_pagamento": "PIX"
}
```

As formas de pagamento aceitas são `PIX`, `CARTAO_CREDITO` e `BOLETO`.

## Regras de negócio

### Produtos

- Produtos físicos exigem peso e estoque.
- Produtos digitais exigem tamanho de arquivo.
- O preço não pode ser negativo.
- Campos exclusivos de um tipo não podem ser usados no outro.

### Clientes

- O nome não pode ficar vazio.
- O tipo padrão é `COMUM`.
- O tipo `VIP` habilita desconto comercial.

### Pedidos

- Um pedido é criado com o status `CRIADO` e pagamento `PENDENTE`.
- O pedido pode ser criado com um ou mais itens.
- A quantidade deve ser maior que zero.
- Produtos físicos têm o estoque reduzido na criação do pedido.
- Produtos físicos têm o estoque restaurado ao cancelar ou excluir um pedido ainda não pago.
- Cliente e produto não podem ser alterados depois da criação.
- Pedidos pagos ou cancelados não podem ser alterados ou excluídos.
- Um pedido pago não pode ser cancelado.
- Ao pagar, o pedido recebe o status `PAGO` e o pagamento recebe `PAGO`.
- Ao cancelar, o pedido e seu pagamento recebem `CANCELADO`.

### Descontos

O maior desconto comercial aplicável é utilizado:

| Condição | Desconto |
|---|---:|
| Cliente VIP | 10% |
| Valor bruto maior ou igual a R$ 500,00 | 5% |

### Pagamentos

O ajuste de pagamento é aplicado após os descontos comerciais:

| Forma | Ajuste |
|---|---:|
| PIX | -5% |
| Cartão de crédito | +3% |
| Boleto | Sem alteração |

## Testes

Execute toda a suíte de testes:

```bash
python manage.py test
```

Execute os testes de um aplicativo específico:

```bash
python manage.py test pedido
python manage.py test produto
python manage.py test cliente
```

## Banco de dados

O projeto utiliza SQLite em desenvolvimento. A configuração atual está localizada em `pedidosis/settings.py` e usa o arquivo `db.sqlite3` na raiz do projeto.

Para recriar o banco após mudanças nos models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Segurança e desenvolvimento

As configurações atuais incluem `DEBUG = True` e uma chave secreta de desenvolvimento. Antes de publicar em produção:

- substitua `SECRET_KEY`;
- configure `DEBUG = False`;
- defina `ALLOWED_HOSTS`;
- configure CORS de forma restritiva;
- utilize um banco de dados adequado ao ambiente;
- adicione variáveis de ambiente para os dados sensíveis.

## Autor

Desenvolvido por [Mary Vitória](https://github.com/maryvitoria002).

## Licença

As informações de licença não estão definidas neste repositório no momento.

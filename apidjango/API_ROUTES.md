# API — Rotas e parâmetros

## Base URL

```text
http://127.0.0.1:8000/
```

Todos os recursos são identificados por UUID. O corpo das requisições deve ser enviado em JSON:

```http
Content-Type: application/json
```

## Produtos

Prefixo: `/produto/`

### `GET /produto/`

Lista todos os produtos.

**Entrada:** nenhuma.

**Saída:** `200 OK`

```json
[
  {
    "id": "uuid",
    "nome": "Livro de Python",
    "preco": "89.90",
    "tipo": "FISICO",
    "estoque": 10,
    "tamanho_arquivo": null,
    "peso": "0.50"
  }
]
```

### `GET /produto/<uuid:id>/`

Busca um produto pelo ID.

**Entrada:**

| Parâmetro | Local | Tipo | Obrigatório |
|---|---|---|---|
| `id` | URL | UUID | Sim |

**Saída:**

- `200 OK`: dados do produto.
- `404 Not Found`: produto inexistente.

### `POST /produto/create/`

Cria um produto físico ou digital.

**Entrada:**

| Campo | Tipo | Obrigatório | Valores ou validação |
|---|---|---|---|
| `nome` | string | Sim | Não vazio |
| `preco` | decimal | Sim | Não negativo |
| `tipo` | string | Sim | `FISICO` ou `DIGITAL` |
| `peso` | decimal | Apenas físico | Maior que zero |
| `estoque` | inteiro | Apenas físico | Zero ou positivo |
| `tamanho_arquivo` | inteiro | Apenas digital | Maior que zero |

Produto físico:

```json
{
  "nome": "Livro de Python",
  "preco": "89.90",
  "tipo": "FISICO",
  "peso": "0.50",
  "estoque": 10
}
```

Produto digital:

```json
{
  "nome": "Curso de Django",
  "preco": "149.90",
  "tipo": "DIGITAL",
  "tamanho_arquivo": 250
}
```

**Saída:**

- `201 Created`: produto criado.
- `400 Bad Request`: dados inválidos ou incompatíveis com o tipo.

### `PUT /produto/<uuid:id>/update/`

Atualiza parcialmente um produto.

**Entrada:**

| Parâmetro | Local | Tipo |
|---|---|---|
| `id` | URL | UUID |
| Campos do produto | Body | Um ou mais campos válidos |

Exemplo:

```json
{
  "preco": "99.90",
  "estoque": 15
}
```

**Saída:**

- `200 OK`: produto atualizado.
- `400 Bad Request`: corpo vazio ou dados inválidos.
- `404 Not Found`: produto inexistente.

### `DELETE /produto/<uuid:id>/delete/`

Remove um produto.

**Entrada:**

| Parâmetro | Local | Tipo | Obrigatório |
|---|---|---|---|
| `id` | URL | UUID | Sim |

**Saída:**

- `204 No Content`: produto removido.
- `404 Not Found`: produto inexistente.

## Clientes

Prefixo: `/cliente/`

### `GET /cliente/`

Lista todos os clientes.

**Entrada:** nenhuma.

**Saída:** `200 OK`

```json
[
  {
    "id": "uuid",
    "nome": "Maria Silva",
    "cpf": "12345678901",
    "email": "maria@example.com",
    "telefone": "11999999999",
    "tipo": "VIP"
  }
]
```

### `GET /cliente/<uuid:id>/`

Busca um cliente pelo ID.

**Saída:**

- `200 OK`: dados do cliente.
- `404 Not Found`: cliente inexistente.

### `GET /cliente/<uuid:id>/pedidos/`

Lista os pedidos associados a um cliente.

**Entrada:**

| Parâmetro | Local | Tipo | Obrigatório |
|---|---|---|---|
| `id` | URL | UUID | Sim |

**Saída:**

- `200 OK`: lista de pedidos.
- `404 Not Found`: cliente inexistente.

### `POST /cliente/create/`

Cria um cliente.

**Entrada:**

| Campo | Tipo | Obrigatório | Valores ou validação |
|---|---|---|---|
| `nome` | string | Sim | Não vazio |
| `cpf` | string | Não | Até 11 caracteres |
| `email` | email | Sim | Email válido |
| `telefone` | string | Não | Até 20 caracteres |
| `tipo` | string | Não | `COMUM` ou `VIP`; padrão `COMUM` |

Exemplo:

```json
{
  "nome": "Maria Silva",
  "cpf": "12345678901",
  "email": "maria@example.com",
  "telefone": "11999999999",
  "tipo": "VIP"
}
```

**Saída:**

- `201 Created`: cliente criado.
- `400 Bad Request`: dados inválidos.

### `PUT /cliente/<uuid:id>/update/`

Atualiza parcialmente um cliente.

Exemplo:

```json
{
  "nome": "Maria Santos",
  "tipo": "COMUM"
}
```

**Saída:**

- `200 OK`: cliente atualizado.
- `400 Bad Request`: corpo vazio ou dados inválidos.
- `404 Not Found`: cliente inexistente.

### `DELETE /cliente/<uuid:id>/delete/`

Remove um cliente.

**Saída:**

- `204 No Content`: cliente removido.
- `404 Not Found`: cliente inexistente.

A exclusão pode remover os pedidos associados ao cliente devido ao relacionamento em cascata.

## Pedidos

Prefixo: `/pedido/`

### `GET /pedido/`

Lista todos os pedidos.

**Entrada:** nenhuma.

**Saída:** `200 OK`

```json
[
  {
    "id": "uuid",
    "cliente": "uuid",
    "status": "CRIADO",
    "produtos": ["uuid"],
    "valor_total": "179.80",
    "valor_com_desconto": "179.80",
    "status_pagamento": "PENDENTE",
    "forma_pagamento": null,
    "valor_pago": "0.00"
  }
]
```

### `GET /pedido/<uuid:id>/`

Busca um pedido pelo ID.

**Saída:**

- `200 OK`: dados do pedido.
- `404 Not Found`: pedido inexistente.

### `POST /pedido/create/`

Cria um pedido com um único item.

**Entrada:**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `cliente` | UUID | Sim | Cliente existente |
| `itens` | lista | Sim* | Lista com `produto` e `quantidade` |
| `produto` | UUID | Não* | Produto único no formato antigo |
| `quantidade` | inteiro | Não* | Quantidade no formato antigo |
| `status` | string | Não | Geralmente `CRIADO` |

`*` Use `itens` para mais de um produto ou o par `produto`/`quantidade` para um único produto.

Exemplo:

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

O formato antigo com `produto` e `quantidade` continua aceito para pedidos com um item.

**Saída:**

- `201 Created`: pedido criado.
- `400 Bad Request`: dados inválidos.

O pedido é criado com:

- `status`: `CRIADO`
- `status_pagamento`: `PENDENTE`
- `forma_pagamento`: `null`
- `valor_pago`: `0.00`

### `PUT /pedido/<uuid:id>/update/`

Atualiza parcialmente um pedido.

Exemplo:

```json
{
  "status": "CRIADO"
}
```

Não é permitido alterar `cliente`, `produto` ou `quantidade`.

Não é permitido definir diretamente `PAGO` ou `CANCELADO`; use os endpoints específicos.

**Saída:**

- `200 OK`: pedido atualizado.
- `400 Bad Request`: atualização inválida ou pedido pago/cancelado.
- `404 Not Found`: pedido inexistente.

### `DELETE /pedido/<uuid:id>/delete/`

Remove um pedido elegível.

**Saída:**

- `204 No Content`: pedido removido.
- `400 Bad Request`: pedido pago ou cancelado.
- `404 Not Found`: pedido inexistente.

### `POST /pedido/<uuid:id>/pagar/`

Efetua o pagamento de um pedido.

**Entrada:**

| Campo | Tipo | Obrigatório | Valores |
|---|---|---|---|
| `forma_pagamento` | string | Sim | `PIX`, `CARTAO_CREDITO` ou `BOLETO` |

Exemplo:

```json
{
  "forma_pagamento": "PIX"
}
```

**Saída:** `200 OK`

```json
{
  "id": "uuid",
  "cliente": "uuid",
  "status": "PAGO",
  "produtos": ["uuid"],
  "valor_total": "179.80",
  "valor_com_desconto": "179.80",
  "status_pagamento": "PAGO",
  "forma_pagamento": "PIX",
  "valor_pago": "170.81"
}
```

**Erros:**

- `400 Bad Request`: forma ausente ou inválida, pedido já pago/cancelado ou sem itens.
- `404 Not Found`: pedido inexistente.

#### Ajustes de pagamento

| Forma | Ajuste |
|---|---:|
| `PIX` | 5% de desconto |
| `CARTAO_CREDITO` | Acréscimo de 3% |
| `BOLETO` | Sem alteração |

### `POST /pedido/<uuid:id>/cancelar/`

Cancela um pedido.

**Entrada:** nenhum corpo necessário.

**Saída:** `200 OK`

```json
{
  "status": "CANCELADO",
  "status_pagamento": "CANCELADO"
}
```

**Erros:**

- `400 Bad Request`: pedido já cancelado ou já pago.
- `404 Not Found`: pedido inexistente.

## Painel administrativo

### `GET /admin/`

Acessa o painel administrativo do Django.

Crie uma conta administrativa com:

```bash
python manage.py createsuperuser
```

## Regras gerais

- Nome de cliente não pode ser vazio.
- Cliente pode ser `COMUM` ou `VIP`.
- Cliente VIP recebe 10% de desconto.
- Compras de pelo menos R$ 500 recebem 5% de desconto.
- O maior desconto aplicável é utilizado.
- Produto físico exige peso e estoque.
- Produto digital exige tamanho de arquivo.
- Campos exclusivos de um tipo não podem ser usados no outro.
- Quantidade de pedido deve ser maior que zero.
- Pedido pago não pode ser cancelado.
- Pedido pago ou cancelado não pode ser excluído.
- Pedido pago ou cancelado não pode ser alterado.
- Produtos físicos têm o estoque reduzido ao criar o pedido.
- Produtos físicos têm o estoque restaurado ao cancelar ou excluir um pedido ainda não pago.

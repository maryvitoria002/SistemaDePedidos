# Front API django

<p align="center">
  <strong>Interface web Angular para o Sistema de Pedidos</strong>
</p>

<p align="center">
  <img alt="Angular" src="https://img.shields.io/badge/Angular-22.3.0-DD0031?logo=angular&logoColor=white">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-6.0.2-3178C6?logo=typescript&logoColor=white">
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-22-339933?logo=node.js&logoColor=white">
  <img alt="Vitest" src="https://img.shields.io/badge/Vitest-5.0.0-6E9F18?logo=vitest&logoColor=white">
</p>


---




## Estrutura do projeto

```text
frontapidjango/
├── src/
│   └── app/
│       ├── api/             # Serviços de acesso à API
│       ├── clients/         # Cadastro e listagem de clientes
│       ├── orders/          # Listagem de pedidos
│       ├── order-detail/    # Detalhes do pedido
│       ├── payment/         # Pagamento do pedido
│       ├── products/        # Listagem de produtos
│       └── product-detail/  # Detalhes do produto
├── proxy.conf.json          # Proxy para execução local
├── proxy.docker.json        # Proxy para execucao com Docker
├── angular.json
├── package.json
└── Dockerfile
```

---


## Testes

Execute os testes unitários com Vitest:

```powershell
npm test -- --watch=false
```

Ou execute em modo interativo:

```powershell
npm test
```

O frontend também pode ser testado enquanto estiver em Docker:

```powershell
docker compose run --rm frontend npm test -- --watch=false
```

---

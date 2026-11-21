# Sistema de Pedidos

<p align="center">
  API REST em Django e interface em Angular para o gerenciamento de clientes, produtos e pedidos.
</p>

<p align="center">
  <img alt="Angular" src="https://img.shields.io/badge/Angular-22-DD0031?logo=angular&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django-6.1.3-092E20?logo=django&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white">
</p>

---

## Sumário

- [Visão geral](#visão-geral)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Opção de execução recomendada: Docker](#opção-recomendada-docker)
- [Executar normalmente, sem Docker](#executar-normalmente-sem-docker)
- [Exemplos da API](#exemplos-da-api)
- [Testes automatizados](#testes-automatizados)
- [Tecnologias](#tecnologias)

### READMEs específicos

- [Frontend Angular](frontapidjango/README.md)
- [Backend Django](apidjango/README.md)
- [Rotas da API](apidjango/API_ROUTES.md)

---

## Visão geral

O projeto utiliza dois servidores separados:

| Serviço | Tecnologia | Porta |
|---|---|---:|
| Frontend | Angular | `4200` |
| API | Django REST Framework | `8000` |

O Angular recebe as chamadas de `/api` e encaminha as requisições ao Django. O Docker Compose usa o servidor de desenvolvimento do Angular e o servidor de desenvolvimento do Django.

## Estrutura do projeto

```text
sistema-pedidos/
├── compose.yaml       # Orquestração Docker
├── apidjango/         # API Django e banco SQLite
└── frontapidjango/    # Aplicação Angular
```

---

# Opção recomendada: Docker

Esta é a forma mais rapida de executar o projeto completo.

## Pré-requisitos

- Docker Desktop
- Docker Compose

## Executar

Na raiz do repositório:

```powershell
docker compose up --build
```

Para iniciar em segundo plano:

```powershell
docker compose up --build -d
```

## Acessar

- **Aplicação Angular:** http://localhost:4200

## Encerrar

```powershell
docker compose down 
```

## Comandos úteis

```powershell
# Exibir status dos containers
docker compose ps

# Exibir logs
docker compose logs -f

# Exibir logs de apenas um servico
docker compose logs -f backend
docker compose logs -f frontend

# Executar os testes Django
docker compose run --rm backend python manage.py test
```

---

# Executar normalmente, sem Docker

As duas partes podem ser iniciadas separadamente em dois terminais.

## 1. Backend Django

### Pré-requisitos

- Python 3.12 ou superior

### Instalação

```powershell
cd apidjango

python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

A API ficará disponível em http://localhost:8000.

Para executar os testes:

```powershell
python manage.py test
```

---

## 2. Frontend Angular

Mantenha o backend Django em execução e abra um segundo terminal.

### Pré-requisitos

- Node.js 22 ou superior
- npm

### Instalação

```powershell
cd frontapidjango

npm install
npm start
```

O Angular ficará disponível em http://localhost:4200.

O proxy de desenvolvimento encaminha `/api` para http://localhost:8000.

Para executar os testes do frontend:

```powershell
npm test -- --watch=false
```

---

# Exemplos da API

## Criar produto físico

```powershell
curl -X POST http://localhost:8000/produto/create/ `
  -H "Content-Type: application/json" `
  -d '{\"nome\":\"Livro de Python\",\"preco\":\"89.90\",\"tipo\":\"FISICO\",\"peso\":\"0.5\",\"estoque\":10}'
```

# Testes automatizados

## Docker

```powershell
docker compose run --rm backend python manage.py test
```

## Execução local

```powershell
cd apidjango
python manage.py test
```

```powershell
cd frontapidjango
npm test -- --watch=false
```

---

# Tecnologias

- Angular 22
- Django 6.1.3
- Django REST Framework 3.18.3
- django-cors-headers
- SQLite
- Docker Compose

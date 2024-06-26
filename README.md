
# API de Cadastro de Artigos e Usuários

## Sobre o Projeto

Esta API foi desenvolvida com o objetivo de permitir a gestão de artigos e usuários em uma plataforma de publicação digital. Utilizando FastAPI, um moderno e rápido framework web para construção de APIs com Python 3.7+, o projeto oferece funcionalidades completas de CRUD para artigos e usuários, incluindo autenticação e autorização com tokens JWT.

## Funcionalidades

- **Usuários**: Cadastro, autenticação, atualização, e exclusão de usuários.
- **Artigos**: Criação, listagem, atualização, e exclusão de artigos.

## Tecnologias Utilizadas

- **FastAPI**: Para a construção da API e geração automática de documentação OpenAPI.
- **SQLAlchemy**: Como ORM para interação com o banco de dados.
- **Pydantic**: Para validação de dados e esquemas de serialização.
- **Uvicorn**: Como servidor ASGI para servir a aplicação.

## Como Começar

### Pré-requisitos

- Python 3.7+
- Pip

### Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Executando a Aplicação

Para iniciar o servidor, execute:

```bash
uvicorn main:app --reload
```

Isso iniciará a aplicação no endereço `http://localhost:8000`. A documentação auto-gerada da API estará disponível em `http://localhost:8000/docs`.

## Autenticação

Para acessar os endpoints protegidos, é necessário autenticar-se através do endpoint `/api/v1/usuarios/login`, que retornará um token JWT. Esse token deve ser incluído no cabeçalho de Autorização das requisições subsequentes como `Bearer <token>`.

## Contribuindo

Contribuições são muito bem-vindas! Se você tem uma sugestão para melhorar este projeto, por favor faça um fork do repositório e crie um pull request. Você também pode simplesmente abrir uma issue com a tag "enhancement".

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

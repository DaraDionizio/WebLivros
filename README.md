# WebLivros
WebLivros: Sistema de Gestão de Biblioteca Pessoal (SGBP) desenvolvido em Python/Django. Permite cadastro e organização de livros, marcação de status (Lido, Lendo, Quero Ler), e controle de empréstimos a amigos. Interface responsiva e intuitiva. Sua estante digital completa.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.14 + Django 6.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite3
- **Ambiente Virtual**: venv

## 📋 Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

## ⚙️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd WebLivros
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute as migrações do banco de dados
```bash
python manage.py migrate
```

### 5. Crie um superusuário para acessar o admin
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

O projeto estará disponível em: `http://127.0.0.1:8000/`

## 📁 Estrutura do Projeto

```
WebLivros/
├── .venv/                      # Ambiente virtual Python
├── Css/                        # Arquivos CSS
├── Img/                        # Imagens
├── Js/                         # Arquivos JavaScript
├── livros/                     # App Django principal
│   ├── migrations/             # Migrações do banco
│   ├── admin.py                # Configuração do admin
│   ├── models.py               # Modelos de dados
│   ├── urls.py                 # Rotas do app
│   └── views.py                # Views/Controllers
├── Proj_Weblivros/             # Configurações do projeto
│   ├── settings.py             # Configurações Django
│   ├── urls.py                 # Rotas principais
│   └── wsgi.py                 # Deploy WSGI
├── dashboard.html              # Dashboard principal
├── index.html                  # Página inicial
├── manage.py                   # Gerenciador Django
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

## 🔌 API Endpoints

- `GET /api/livros/` - Lista todos os livros
- `GET /api/livros/<id>/` - Obtém detalhes de um livro
- `POST /api/livros/criar/` - Cria um novo livro
- `PUT /api/livros/<id>/atualizar/` - Atualiza um livro
- `DELETE /api/livros/<id>/deletar/` - Deleta um livro

## 👨‍💼 Painel Administrativo

Acesse o painel admin em: `http://127.0.0.1:8000/admin/`

Use as credenciais criadas no passo 5 (createsuperuser).

## 🗄️ Modelo de Dados - Livro

- **titulo**: Título do livro
- **autor**: Nome do autor
- **editora**: Editora do livro
- **ano_publicacao**: Ano de publicação
- **isbn**: Código ISBN único
- **num_paginas**: Número de páginas
- **descricao**: Descrição do livro
- **capa_url**: URL da imagem da capa
- **data_cadastro**: Data de cadastro (automático)
- **data_atualizacao**: Data da última atualização (automático)

## 📝 Próximos Passos

Para continuar o desenvolvimento:

1. **Criar o superusuário**: Execute `python manage.py createsuperuser`
2. **Integrar o frontend com o backend**: Atualizar os arquivos JavaScript para consumir a API
3. **Adicionar funcionalidades**: Status de leitura, empréstimos, etc.
4. **Deploy**: Configurar para produção (Heroku, AWS, etc.)

## 🤝 Contribuindo

Sinta-se à vontade para contribuir com o projeto!

## 📄 Licença

Este projeto está sob a licença MIT.

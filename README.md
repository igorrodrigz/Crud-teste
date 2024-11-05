# CRUD para Teste de Conhecimento

A nossa aplicação é uma plataforma de gerenciamento de usuários que facilita o cadastro, autenticação e edição de informações pessoais. Com um design intuitivo e responsivo, ela permite que os usuários se cadastrem rapidamente, criando suas contas com informações básicas como nome, e-mail e senha.

## Índice
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)


## Funcionalidades
- **Cadastro de Usuários:** Permite que novos usuários se cadastrem, fornecendo informações como nome, e-mail e senha.
- **Login e Autenticação:** Usuários podem fazer login na aplicação de forma segura.
- **Edição de Perfil:** Usuários podem editar suas informações de perfil, como nome e e-mail.
- **Validação de Senha:** Implementa validação de senhas fortes durante o cadastro e a edição de perfil.
- **Gerenciamento de Sessões:** Permite que usuários permaneçam logados em suas contas com segurança.
- **Interface Amigável:** A aplicação possui uma interface responsiva e intuitiva, desenvolvida com HTML e Bootstrap.

## Tecnologias Utilizadas
- **Python:** Linguagem de programação principal utilizada para o desenvolvimento da aplicação.
- **Django:** Framework web utilizado para construir a aplicação.
- **HTML/CSS:** Linguagens de marcação e estilo utilizadas para criar a interface do usuário.
- **Bootstrap:** Framework CSS que facilita o design responsivo.
- **SQLite/MySQL:** Banco de dados utilizado para armazenar informações de usuários.

## Uso

-Acesse a aplicação no seu navegador através de http://127.0.0.1:8000/.
-Utilize a funcionalidade de cadastro para criar uma nova conta.
-Faça login usando as credenciais cadastradas.
-Navegue pelas funcionalidades disponíveis, como edição de perfil e gerenciamento de conta.

## Estrutura do projeto
nome-do-repositorio/
│
├── app/                  # Código-fonte da aplicação
│   ├── migrations/       # Migrations do banco de dados
│   ├── templates/        # Templates HTML
│   ├── static/           # Arquivos estáticos (CSS, JS)
│   ├── views.py          # Lógica de controle
│   ├── models.py         # Modelos de dados
│   └── urls.py           # URLs da aplicação
│
├── manage.py             # Script de gerenciamento do Django
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto

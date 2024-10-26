# Sistema de Reservas - Restaurante do Fernandasso

## Descrição
Este projeto é um sistema de reservas online desenvolvido para o Restaurante do Fernandasso. Ele permite aos clientes realizar reservas, verificar a disponibilidade de mesas, e explorar informações sobre o restaurante. O sistema também oferece uma interface administrativa para o gerenciamento de reservas e mesas disponíveis.

## Funcionalidades Principais

- **Autenticação de Usuários**:
  - Registro de novos usuários com validação de dados.
  - Login customizado com suporte a JWT (JSON Web Tokens).
  - Logout com redirecionamento para a página inicial.
  - Apenas usuários autenticados podem criar e visualizar reservas.

- **Gerenciamento de Reservas**:
  - Criação de novas reservas com verificação automática de disponibilidade de mesas.
  - Endpoint de verificação de disponibilidade de mesas para uma data específica.
  - Visualização de reservas para usuários autenticados.

- **Páginas Informativas**:
  - Página inicial com links para as principais seções.
  - Página "Sobre Nós" com detalhes sobre a história do restaurante e seu chef.
  - Depoimentos de clientes na página inicial.

## Estrutura do Projeto

### Páginas e Endpoints

| URL                        | Descrição                                               |
|----------------------------|---------------------------------------------------------|
| `/`                        | Página inicial                                          |
| `/login/`                  | Login de usuário                                        |
| `/logout/`                 | Logout de usuário                                       |
| `/register/`               | Registro de novo usuário                                |
| `/menu/`                   | Página com o menu do restaurante                        |
| `/sobre/`                  | Página sobre o restaurante                              |
| `/reservations/`           | Listagem de reservas do usuário                         |
| `/reservations/new/`       | Formulário para criação de nova reserva                 |
| `/check-availability/`     | Endpoint para verificar disponibilidade de mesas        |
| `/api/token/`              | Geração de token JWT para autenticação de usuário       |
| `/api/token/refresh/`      | Atualização do token JWT                                |

## Tecnologias Utilizadas

- **Backend**: Django e Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap, e Font Awesome
- **Autenticação**: JWT (JSON Web Tokens) com `djangorestframework-simplejwt`
- **Banco de Dados**: PostgreSQL (ou banco de dados configurado)

## Instalação

1. Clone este repositório e navegue até o diretório do projeto.
2. Crie um ambiente virtual e ative-o.
3. Instale as dependências listadas no arquivo `requirements.txt`.
4. Configure as informações do banco de dados no arquivo `settings.py`.
5. Execute as migrações para configurar o banco de dados.
6. Crie um superusuário para acessar o painel administrativo.
7. Inicie o servidor de desenvolvimento do Django.

## Testes

O sistema inclui testes unitários e de integração para as principais funcionalidades:
- Testes de autenticação para verificar o acesso de usuários autenticados e não autenticados.
- Testes de criação de reservas, incluindo verificação de disponibilidade de mesas.
- Testes de resposta do endpoint `/check-availability/` para datas válidas e inválidas.

Para executar os testes, use o comando:

python manage.py test

### Carregar Dados de Exemplo

Após configurar o banco de dados, você pode carregar dados de exemplo para os pratos com o seguinte comando:

python manage.py loaddata dish_data.json



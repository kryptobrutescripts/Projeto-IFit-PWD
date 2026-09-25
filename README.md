# IFit+

Plataforma web de acompanhamento de atividades físicas com gamificação, estatísticas, ranking, grupos, perfil de usuário e sistema de patentes e conquistas.

## Sobre o projeto

O IFit+ é uma aplicação web desenvolvida com Flask e SQLite para permitir que usuários registrem e acompanhem suas atividades físicas.

A plataforma permite cadastrar usuários, registrar atividades, acompanhar distância e duração, consultar estatísticas, visualizar rankings, participar de grupos, personalizar o perfil e acompanhar a progressão por meio de patentes e conquistas.

O projeto utiliza Flask no backend, SQLAlchemy para comunicação com o banco de dados SQLite, Bcrypt para armazenamento seguro das senhas e Jinja2 para renderização das páginas HTML.

A aplicação foi organizada de forma modular, separando os modelos do banco de dados, funções compartilhadas, rotas, templates HTML, estilos CSS, scripts JavaScript e recursos visuais.

---

## Recursos principais

* Cadastro de usuários.
* Login e logout.
* Senhas armazenadas utilizando hash com Bcrypt.
* Controle de sessão.
* Validação de dados no servidor.
* Cadastro de atividades físicas.
* Edição de atividades.
* Exclusão de atividades.
* Registro de distância e duração das atividades.
* Oito modalidades de atividades físicas.
* Estatísticas individuais.
* Estatísticas de distância por dia.
* Estatísticas agrupadas por modalidade.
* Gráficos na página de estatísticas.
* Ranking geral.
* Ranking filtrado por modalidade.
* Sistema de grupos.
* Criação de grupos.
* Entrada em grupos.
* Visualização dos grupos do usuário.
* Visualização dos membros de um grupo.
* Posição dos usuários no ranking.
* Perfil de usuário.
* Alteração de nome de exibição.
* Alteração de nome de usuário.
* Alteração de senha.
* Upload de foto de perfil.
* Remoção da foto de perfil.
* Validação das extensões das imagens enviadas.
* Nomes aleatórios para os arquivos de imagem.
* Sistema de patentes.
* Divisões dentro das patentes.
* Sistema de conquistas por quantidade de atividades.
* Insígnias específicas por modalidade.
* Insígnia especial para domínio de todas as modalidades.
* Patente Lendário.
* Banco de dados SQLite criado automaticamente pela aplicação.
* Criação automática das pastas necessárias durante a inicialização.

---

## Tecnologias utilizadas

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Bcrypt
* SQLAlchemy
* SQLite
* Jinja2
* HTML
* CSS
* JavaScript

---

## Estrutura do projeto

```text
IFit+/

├── README.md
├── requirements.txt
│
├── ghoul/
│   ├── __init__.py
│   ├── models.py
│   ├── route_core.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── achievements.py
│       ├── activities.py
│       ├── auth.py
│       ├── groups.py
│       ├── leaderboard.py
│       ├── profile.py
│       └── statistics.py
│
├── instance/
│   └── ifit+.db
│
├── static/
│   ├── badges/
│   │   ├── Caminhada/
│   │   ├── Ciclismo/
│   │   ├── Corrida/
│   │   ├── Elíptico/
│   │   ├── Natação/
│   │   ├── Patinação/
│   │   ├── Remo/
│   │   └── Trilha/
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │   ├── user_default.ico
│   │   └── user_images/
│   │
│   ├── javascript/
│   │   ├── modals.js
│   │   ├── particles.js
│   │   └── script.js
│   │
│   └── patentes/
│       ├── elite1.png
│       ├── elite2.png
│       ├── elite3.png
│       ├── elite4.png
│       ├── elite5.png
│       ├── lendario.png
│       ├── mestre1.png
│       ├── mestre2.png
│       ├── mestre3.png
│       ├── mestre4.png
│       ├── mestre5.png
│       ├── mestre_todas.png
│       ├── pro1.png
│       ├── pro2.png
│       ├── pro3.png
│       ├── pro4.png
│       ├── pro5.png
│       ├── recruta1.png
│       ├── recruta2.png
│       ├── recruta3.png
│       ├── recruta4.png
│       ├── recruta5.png
│       ├── veterano1.png
│       ├── veterano2.png
│       ├── veterano3.png
│       ├── veterano4.png
│       └── veterano5.png
│
└── templates/
    ├── base.html
    ├── cadastro_atividade.html
    ├── conquistas.html
    ├── create_group.html
    ├── dashboard.html
    ├── edit_activity.html
    ├── group_members.html
    ├── groups_panel.html
    ├── join_group.html
    ├── leaderboard.html
    ├── login.html
    ├── my_groups.html
    ├── profile.html
    ├── register.html
    ├── statistics.html
    │
    └── components/
        └── navbar.html
```

---

## Organização do backend

### `ghoul/__init__.py`

Responsável pela inicialização principal da aplicação Flask.

Entre suas responsabilidades estão:

* criação da aplicação;
* configuração dos diretórios de templates e arquivos estáticos;
* configuração da chave secreta;
* configuração da duração da sessão;
* configuração do diretório de upload das fotos;
* configuração do SQLite;
* inicialização do SQLAlchemy;
* inicialização do Bcrypt;
* criação das pastas necessárias;
* criação automática das tabelas do banco de dados;
* disponibilização do usuário atual para os templates.

A aplicação executa:

```python
with app.app_context():
    db.create_all()
```

durante a inicialização.

Por isso, as tabelas são criadas automaticamente quando ainda não existem.

---

### `ghoul/models.py`

Contém os modelos SQLAlchemy utilizados pela aplicação.

Atualmente existem três modelos principais:

* `User`
* `Activity`
* `Group`

Também existe a tabela associativa:

```text
group_members
```

utilizada para representar a relação entre usuários e grupos.

---

### `ghoul/route_core.py`

Contém funções compartilhadas pelo backend.

Entre elas estão:

* proteção de rotas que exigem login;
* categorias de atividades;
* cálculo da posição do usuário no ranking;
* cálculo das estatísticas;
* cálculo da distância por dia.

As modalidades são definidas no dicionário `CATEGORIES`.

---

## Organização das rotas

### `auth.py`

Responsável pelas funcionalidades principais de autenticação e navegação:

* página inicial;
* dashboard;
* login;
* logout;
* cadastro de usuário.

---

### `activities.py`

Responsável pelo gerenciamento das atividades:

* listagem;
* cadastro;
* edição;
* atualização;
* exclusão.

---

### `statistics.py`

Responsável pelas estatísticas do usuário.

Também disponibiliza endpoints utilizados pelos gráficos:

```text
/api/distance_by_day
/api/activities_by_category
/api/distance_by_category
```

---

### `leaderboard.py`

Responsável pelo quadro de líderes.

O ranking pode ser consultado:

* de forma geral;
* filtrado por modalidade.

A classificação utiliza a distância acumulada das atividades.

---

### `groups.py`

Responsável pelo sistema de grupos.

Permite:

* criar grupos;
* entrar em grupos;
* consultar grupos;
* visualizar grupos dos quais o usuário participa;
* visualizar os membros de um grupo.

---

### `profile.py`

Responsável pelas configurações do perfil.

Permite:

* visualizar o perfil;
* alterar nome de exibição;
* alterar nome de usuário;
* alterar senha;
* adicionar foto;
* remover foto.

As fotos recebem nomes aleatórios antes de serem armazenadas.

---

### `achievements.py`

Responsável pelo sistema de patentes e conquistas.

A progressão é calculada de acordo com a quantidade de atividades realizadas em cada modalidade.

As patentes disponíveis são:

```text
Recruta
Veterano
Elite
Pro
Mestre
Lendário
```

As cinco primeiras patentes possuem as divisões:

```text
I
II
III
IV
V
```

A patente Lendário é alcançada ao atingir o requisito final definido pelo sistema.

---

## Atividades

O IFit+ possui oito modalidades de atividades físicas:

* Caminhada
* Ciclismo
* Corrida
* Natação
* Trilha
* Remo
* Patinação
* Elíptico

Cada atividade possui:

* categoria;
* data;
* distância;
* duração;
* usuário responsável;
* data de criação do registro.

As categorias também possuem cores próprias utilizadas nos elementos estatísticos da aplicação.

---

## Estatísticas

A aplicação calcula estatísticas individuais a partir das atividades registradas pelo usuário.

São disponibilizadas informações como:

* distância total;
* duração total;
* quantidade total de atividades;
* quantidade de atividades por modalidade;
* distância acumulada por modalidade;
* distância registrada por dia.

As informações de estatísticas são utilizadas pelo frontend para gerar visualizações gráficas.

---

## Ranking

O IFit+ possui um quadro de líderes baseado na distância acumulada.

É possível visualizar o ranking geral ou selecionar uma modalidade específica.

O sistema calcula para cada usuário:

* posição;
* distância acumulada;
* duração acumulada;
* quantidade de atividades;
* patente ou insígnia correspondente.

Quando necessário, a posição pode ser exibida como `99+` para usuários que ultrapassam essa posição.

---

## Sistema de patentes e conquistas

O projeto possui um sistema de progressão baseado na quantidade de atividades realizadas.

A progressão possui cinco patentes principais:

```text
Recruta
Veterano
Elite
Pro
Mestre
```

Cada uma delas possui cinco divisões:

```text
I
II
III
IV
V
```

Depois de Mestre V, o usuário pode alcançar:

```text
Lendário
```

As conquistas são calculadas individualmente para cada modalidade.

O projeto também possui uma insígnia especial para usuários que alcançam pelo menos Mestre I em todas as modalidades.

---

## Banco de dados SQLite

O projeto utiliza SQLite como banco de dados.

O arquivo do banco fica em:

```text
instance/ifit+.db
```

O banco é criado automaticamente pela aplicação.

A pasta `instance` também é criada automaticamente caso ainda não exista.

Durante a inicialização, a aplicação executa:

```python
db.create_all()
```

Isso significa que não é necessário criar manualmente o banco de dados ou suas tabelas antes da primeira execução.

### Importante

O `db.create_all()` cria as tabelas que ainda não existem, mas **não recupera dados que foram apagados**.

Portanto, se o arquivo:

```text
instance/ifit+.db
```

for excluído, a aplicação criará um novo banco vazio na próxima inicialização.

Os usuários, atividades, grupos e demais registros existentes no banco anterior não serão recuperados.

---

## Instalação e execução no Windows

Abra o terminal dentro da pasta do projeto e execute:

```bat
python -m venv venv
```

Ative o ambiente virtual:

```bat
venv\Scripts\activate
```

Instale as dependências:

```bat
pip install -r requirements.txt
```

Inicie a aplicação:

```bat
python -m flask --app ghoul run --debug
```

Depois, abra no navegador:

```text
http://127.0.0.1:5000
```

---

## Linux ou macOS

Crie o ambiente virtual:

```bash
python3 -m venv venv
```

Ative:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python3 -m flask --app ghoul run --debug
```

A aplicação normalmente estará disponível em:

```text
http://127.0.0.1:5000
```

---

## Primeiro início

Na primeira execução, a aplicação:

1. inicia o Flask;
2. configura o SQLite;
3. cria a pasta `instance`, caso ela não exista;
4. cria a pasta utilizada para armazenar fotos de usuários;
5. inicializa o SQLAlchemy;
6. carrega os modelos;
7. executa `db.create_all()`;
8. cria as tabelas que ainda não existem;
9. carrega as rotas da aplicação.

Depois desse processo, o arquivo:

```text
instance/ifit+.db
```

passará a existir.

---

## Frontend

Os templates HTML estão localizados em:

```text
templates/
```

O arquivo:

```text
templates/base.html
```

funciona como estrutura base para as páginas.

O componente:

```text
templates/components/navbar.html
```

contém a barra de navegação compartilhada.

Os estilos principais estão em:

```text
static/css/style.css
```

Os scripts JavaScript estão em:

```text
static/javascript/
```

Atualmente existem:

* `script.js`: comportamentos gerais da interface;
* `modals.js`: modais e confirmações;
* `particles.js`: partículas e elementos decorativos.

---

## Recursos visuais

O projeto possui recursos gráficos para o sistema de gamificação.

As insígnias das modalidades estão em:

```text
static/badges/
```

As imagens das patentes estão em:

```text
static/patentes/
```

Também existe uma imagem padrão para usuários em:

```text
static/images/user_default.ico
```

As fotos enviadas pelos usuários são armazenadas em:

```text
static/images/user_images/
```

---

## Dependências

As dependências principais estão listadas em:

```text
requirements.txt
```

Atualmente:

```text
Flask
Flask-SQLAlchemy
Flask-Bcrypt
Werkzeug
```

Para instalar todas:

```bash
pip install -r requirements.txt
```

---

## Desenvolvimento

Durante o desenvolvimento, o comando recomendado é:

```bash
python -m flask --app ghoul run --debug
```

O parâmetro `--debug` permite recarregamento automático e exibe informações detalhadas de erro.

O modo `debug` deve ser utilizado apenas durante o desenvolvimento.

Para disponibilizar a aplicação em produção, deve-se utilizar um servidor WSGI apropriado e realizar as configurações de segurança necessárias.

---

## Arquivos que não devem ser versionados

Ao colocar o projeto no GitHub, recomenda-se não versionar arquivos gerados automaticamente ou dados locais.

Um `.gitignore` adequado para este projeto pode conter:

```gitignore
__pycache__/
*.py[cod]

venv/
.venv/
env/

instance/*.db

static/images/user_images/*
!static/images/user_images/.gitkeep
```

Isso evita enviar:

* cache do Python;
* ambiente virtual;
* banco SQLite local;
* fotos de usuários.

O arquivo:

```text
static/images/user_images/.gitkeep
```

pode ser mantido para preservar a pasta no Git.

---

## Banco de dados no GitHub

O arquivo:

```text
instance/ifit+.db
```

não precisa ser enviado para o GitHub.

A aplicação consegue criar um novo banco automaticamente quando o projeto é executado.

Dessa forma, cada instalação pode iniciar com um banco novo.

Além de evitar o versionamento de dados locais, isso também impede que informações de usuários sejam publicadas acidentalmente no repositório.

---

## Observações

Esta versão utiliza uma configuração local simples, adequada para desenvolvimento e demonstração.

A chave secreta do Flask está atualmente definida diretamente no código:

```python
app.secret_key = "chave_secreta"
```

Em um ambiente de produção, essa informação deve ser armazenada em uma variável de ambiente ou outro mecanismo seguro de configuração.

Da mesma forma, o servidor de desenvolvimento do Flask não deve ser utilizado como servidor público de produção.

---

## Versão

```text
IFit+ V0
```

Esta versão contém:

* autenticação;
* atividades;
* estatísticas;
* ranking;
* grupos;
* perfil;
* gamificação;
* patentes;
* conquistas;
* SQLite.

---

## Licença

Este projeto é destinado a fins acadêmicos, educacionais e de desenvolvimento.

Consulte os responsáveis pelo projeto antes de redistribuir ou utilizar o código em outros contextos.

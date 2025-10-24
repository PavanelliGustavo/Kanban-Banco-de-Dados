# Kanban de Transparência

## Setup inicial de desenvolvimento

Antes de tudo, certifique-se de ter o `Python` instalado na versão 3.12.3 ou superior.

Para verificar, execute em seu terminal:

```bash
python --version    # Windows
python3 --version   # Linux/WSL
```

Então, crie um ambiente virtual para instalar as dependências do projeto com o seguinte comando:

```bash
python -m venv .venv    # Windows
python3 -m venv .venv   # Linux/WSL
```

Agora ative seu ambiente virtual:

```bash
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/WSL
```

Por fim, instale as dependências com o comando:

```bash
pip install -r requirements.txt
```

Em caso de erro, certifique-se de que o comando `pip` está instalado com:

```bash
pip --version
```

Se não estiver, execute:

```bash
python -m ensurepip --default-pip    # Windows
sudo apt install python3-pip         # Linux/WSL
```

## Adição de novas dependências

Para adicionar novas dependências, primeiro certifique-se de que seu ambiente virtual existe e está ativado.

Então, execute o comando:

```bash
pip install nome_da_dependência
```

E por fim, atualize o arquivo `requirements.txt` com as novas dependências utilizando o comando:

```bash
pip freeze > requirements.txt
```

## Estrutura do projeto

O projeto apresenta a seguinte estrutura de diretórios:

```
KANBAN-BANCO-DE-DADOS/
│
├── .venv/
│
├── app/
│   ├── controllers/
│   │
│   ├── models/
│   │
│   ├── routes/
│   │
│   ├── sql/
│   │   ├── commands/
│   │   └── migrations/
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   │
│   ├── templates/
│   │
│   └── config.py
│
├── tests/
│
├── .gitignore
├── PROJECT-INSTRUCTIONS.md
├── README.md
├── requirements.txt
└── run.py
```

- `app/` é o diretório que contém todos os componentes estruturais do projeto (models, views, controllers, etc.).
- `app/controllers/` é o diretório que contem todas as implementações de controladoras, que devem estabelecer a comunicação entre views e models.
- `app/models/` é o diretório que contem todas as implementações de modelos, e é o único módulo que deve interagir diretamente com o banco de dados.
- `app/routes/` é o diretório onde devem ser declaradas todas as rotas do projeto, de forma que o usuário possa navegar entre telas.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template("login.html")
```

> **ℹ️ O que é uma rota?**  
> Em aplicações web, rotas são formas de associar URLs a funções do código. No exemplo acima, a URL `http://localhost:5000/login` está vinculada à função `login()`. Ao acessar essa URL no navegador, a função será executada e o template `login.html` será exibido.

- `app/sql/` é o diretório que registrará todos os comandos a serem executados no banco de dados.
- `app/sql/commands/` é o diretório que conterá os comandos SQL a serem utilizados pelas models, como comandos de consultas, inserções de dados e até o próprio comando de criação do banco de dados.
- `app/sql/migrations/` é o diretório que conterá todos os comandos SQL relacionados a migrações de banco de dados. As migrações devem funcionar como um histórico de todas as alterações feitas à estrutura do banco e devem seguir rigidamente a estrutura de nomenclatura `YYYYMMDD_HHmm_description.sql` (ex: `20251023_1659_add_email_to_users.sql`).

   - Não perca tempo pensando em uma descrição elaborada — a real importância do nome está no `timestamp`, já que ele garantirá que as migrações possam ser executadas em ordem.

> **ℹ️ O que é uma migração?**  
> No contexto de bancos de dados, migrações são comandos SQL que modificam a estrutura do banco após sua criação. Elas permitem que qualquer pessoa, com acesso ao script de criação e às migrações, possa reproduzir a mesma estrutura final do banco executando os arquivos em ordem.

> ⚠️ **Atenção:**  
> Todo arquivo contido em `app/sql/` deve conter a extensão `.sql`, e só devem ser colocados em um mesmo arquivo comandos cuja execução esteja intimamente atrelada (ex: criação das diferentes tabelas do banco de dados).

- `app/static/` é o diretório que encapsula a estilização e responsividade do front-end da aplicação.
- `app/static/css/` é o diretório que conterá os arquivos com extensão `.css`, responsáveis por estilizar os templates.
- `app/static/img/` é o diretório responsável por armazenar as imagens utilizadas no projeto, se houver.
- `app/static/js/` é o diretório que conterá os arquivos com extensão `.js`, encarregados de armazenar o código em JavaScript que fornecerá responsividade aos templates.
- `app/templates/` é o diretório que conterá os arquivos com extensão `.html`, e efetivamente representará as `views` da aplicação. O nome `templates` é pré-estabelecido para que o `Flask` consiga localizar e exibir as views da aplicação com o método `render_template()`.
- `tests/` é o diretório onde qualquer teste criado deve ser inserido.
- `run.py` é o arquivo principal de execução da aplicação, equivalente a uma `main`, porém seguindo a convenção de nomenclatura do `Flask`.
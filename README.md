# fequa
Ferramentas Que Adoro

Stacks:
Python, FastAPI, JWT, SqlAchemy, Postgresql

Link de acesso para teste e documentação da fequa API: http://35.88.134.121/

## Rotas
Registra usuário: POST /user
```commandline
body

{
  "username": "string",
  "email": "string",
  "password": "string",
  "confirm_password": "string"
}
```

Autentica usuário: POST /user/token
```commandline
application/x-www-form-urlencoded
grant_type = &username=usuario_cadastrado&password=usuario_cadastrado
```
Lista usuários: GET /users

Lista ferramentas: GET /tools

Registra ferramentas: POST /tools
```commandline
body

{
  "title": "string",
  "link": "string",
  "description": "string",
  "tags": [
    "string",
    "string-1",
    "string-N",
  ]
}
```

Lista ferramentas filtrando por id: GET /tools/
```commandline
query

/tools/?tag=tag_cadastrada
```

Deleta ferramenta filtrando por id: DELETE /tools/{id}
```commandline
path

id=id_da_ferranta
```


## Local Run

#### 1. Ative o virtualenv
```commandline
virtualenv venv
source venv/bin/activate
```

#### 2. Instalar Dependencias
```commandline
pip install -r /path/to/requirements.txt
```

#### 3. Variáveis de ambiente (.env)
As variáveis de ambiente estão no arquivo .env. Para conveniência o arquivo esta disponível.
Variáveis sensíveis a segurança foram omitidas.
Informe os valores para as variáveis (DBUSER, DBPASSWORD, DBBASE, DBHOST, SECRET_KEY)

#### 4. Run
Na pasta myapp
```commandline
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:3000 main:app

```
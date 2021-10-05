# E-Academy

Trata-se de um pequeno esboço de API focado em recuperar, incluir, remover e editar - de forma seletiva ou não - uma representação serializável de dados básicos de uma plataforma de e-learning (no caso, dados de estudante, cursos e matrícula).

## 🚀 Começando

Para obter o projeto utilizar:

```
$ git clone https://github.com/LePiN/virtual_academy.git
```

### 📋 Pré-requisitos

- Python 3
- Git
- VirtualEnv
- Django
- Django REST
- Postgresql


### 🔧 Instalação

Para criação do ambiente virtual:

- Criando e utilizando ambiente virtual Linux:
```
$ python -m venv .venv
$ source .venv/bin/activate
```

- Criando e utilizando ambiente virtual Windows:
```
$ python -m venv .venv
$ source .venv/Scripts/activate
```

Instalando dependências:
```
$ pip install -r requirements.txt
```

- Crie um banco de dados para o projeto no seu servidor Postgresql e coloque os dados de acesso em e-academy/settings.py
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "<nome do banco criado>",
        "USER": "<identificação do seu usuario do postgresql>",
        "PASSWORD": "<senha do seu usuario no postgresql>",
        "HOST": "<endereço do servidor, para testes, geralmente localhost>",
        "PORT": "<porta do servidor utilizada>",
    }
}
```

Preparando banco de dados da aplicação:
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Verificando servidor da aplicação:
```
$ python manage.py runserver
```
Com isso já será possivel navegar pelo projeto atraves da url http://127.0.0.1:8000/<end-points>.

## ⚙️ Executando os testes

Nessa versão, o esboço dos testes para os filtros de seleção de vitrines:
```
$ cd e-academy/
$ pytest
```

## 📦 Operações

- Verificar documentação automática: endereço-servidor-projeto (exemplo, http://127.0.0.1:8000/)

- As requisições da api estão todas em: url-projeto/api/v1/endpoint

### Cursos

- Requisitar todos os cursos:
```
método: GET
endpoint: url-projeto/api/v1/courses/
```

- Requisitar curso específica:
```
método: GET
endpoint: url-projeto/api/v1/courses/<course-pk: int>/
```

- Incluir novo curso:
```
método: POST
endpoint: url-projeto/api/v1/courses/
body: {
    "description": <string>,
    "duration": <int ou string no formato HH:MM:SS>,
    "holder_image": <image code>,
    "name": <string>
```

- Editar um curso existente:
```
método: PUT ou PATCH
endpoint: url-projeto/api/v1/courses/<course-pk: int>/
body: {
    "description": <string>,
    "duration": <int ou string no formato HH:MM:SS>,
    "holder_image": <image code>,
    "name": <string>
}
```

- Remover um curso específico:
```
método: DELETE
endpoint: url-projeto/api/v1/courses/<course-pk: int>/
```

### Estudantes

- Requisitar todos os estudantes:
```
método: GET
endpoint: url-projeto/api/v1/students/<course-pk: int> 
```

- Requisitar estudante específico:
```
método: GET
endpoint: url-projeto/api/v1/students/<student-pk: int> 
```

- Requisitar estudante por período de cadastro:
```
método: GET
endpoint: url-projeto/api/v1/students/?date_created_end=<data, formato YYYY-MM-DD>&date_created_start=<data, formato, YYYY-MM-DD>
```

- Incluir novo estudante:
```
método: POST
endpoint: url-projeto/api/v1/students/
body: {
    "avatar": <image code>,
    "name": <string>,
    "nickname": <string>,
    "phone": <string>
}
```

- Editar um estudante específico:
```
método: PUT ou PATCH
endpoint: url-projeto/api/v1/students/<student-pk: int> 
body: {
    "avatar": <image code>,
    "name": <string>,
    "nickname": <string>,
    "phone": <string>
}
```

- Remover um estudante específico:
```
método: DELETE
endpoint: url-projeto/api/v1/students/<student-pk: int>
```

### Matrículas

- Requisitar todas as matrículas:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/
```

- Requisitar uma matrícula específica:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/<enrollment-pk: int>/
```

- Requisitar matrículas com status específicos:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/?status=<opção string (AN, RE, AP)>
```

- Requisitar matrículas com aluno específico:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/?student=<int (id de um estudante válido)>
```

- Requisitar matrículas com curso específico:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/?course=<int (id de um curso válido)>
```

- Requisitar matrículas por período de inicio da matrícula:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/?date_enroll_end=<data, formato YYYY-MM-DD>&date_enroll_start=<data, formato, YYYY-MM-DD>
```

- Requisitar matrículas por período de término da matrícula:
```
método: GET
endpoint: url-projeto/api/v1/enrollments/?date_close_end=<data, formato YYYY-MM-DD>&date_close_start=<data, formato, YYYY-MM-DD>
```

- Incluir nova matrícula:
```
método: POST
endpoint: url-projeto/api/v1/enrollments/
body: {
    "course": <int (id de um curso válido)>,
    "date_close": <data, formato YYYY-MM-DD>,
    "score": <decimal>,
    "status": <opção string (AN, RE, AP)>,
    "student": <int (id de um estudante válido)>
}
```

- Editar uma nova matrícula:
```
método: PUT ou PATCH
endpoint: url-projeto/api/v1/enrollments/<enrollment-pk: int>/
body: {
    "course": <int (id de um curso válido)>,
    "date_close": <data, formato YYYY-MM-DD>,
    "score": <decimal>,
    "status": <opção string (AN, RE, AP)>,
    "student": <int (id de um estudante válido)>
}
```

- Remover uma matrícula:
```
método: DELETE
endpoint: url-projeto/api/v1/enrollments/<enrollment-pk: int>/
```

## 🛠️ Construído com

* [Django](https://docs.djangoproject.com/en/3.1/) - O framework web usado
* [Django-REST](https://pycodestyle.pycqa.org/en/latest/intro.html) - O módulo REST utilizado
* [Postgresql](https://www.postgresql.org/) - Banco de dados sugerido
* [Swagger](https://swagger.io/) - O gerador de documentação

## ✒️ Autores

* **Leandro Pieper Nunes** - *Trabalho Inicial* - [Leandro Pieper Nunes](https://github.com/LePiN)

## 🎁 Agradecimentos

* Grato a toda equipe Keeps pela oportunidade de participar da seleção.


---
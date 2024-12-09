<h1 align="center">Alu_JogoTeca</h1>

![badge](https://img.shields.io/badge/Flask-3.0.3-blue)
![badge](https://img.shields.io/badge/MySql-8.0CE-blue)
![badge](https://img.shields.io/badge/Status-%20Concluído-green)



![Imagem Flask](https://media.licdn.com/dms/image/D5612AQHA0KmK22P4JA/article-cover_image-shrink_600_2000/0/1701780419999?e=2147483647&v=beta&t=VJOcqpZ0sBraLinYyD6DXEpwz9n3jwRPb0teorBdUQk)



<h2>Funcionalidade</h2>

Material de estudo para desenvolver habilidades em Flask, com o objetivo de criar uma aplicação para realizar funções simples, como adicionar elementos em uma tabela e implementar um sistema de login.

<h2>Ferramentas</h2>

PYTHON 3.12

PIP 24.2

FLASK 3.0.3

BOOTSTRAP 5.3.3

jQuery 3.3.1

MYSQL CONNECTOR 9.0.0


<h2>Como Usar</h2>

<h3>Instale as dependências do requirements.txt em um ambiente virtual ou global da máquina "pip install -r requirements.txt"</h3>

<h3>Criar e configurar um arquivo config.py com essas variáveis, atentando as informações do banco de dados (sgdb,user, password), além de criar uma secret key para a aplicação flask.</h3>


import os

SECRET_KEY = 'XXXXXXXXXXX'


SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        user='XXXX',
        password='XXXXXXXXXXXXX',
        servidor='localhost',
        database='jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

<h3>Além do arquivo config.py, existe a necessidade de configurar um database, usando o prepara_banco.py. Já existe uma base para esse feito, sendo necessário fazer apenas algumas mudanças na configuração do mesmo.</h3>

conn = mysql.connector.connect(
        host='XXX.X.X.X',
        user='XXXX',
        password='XXXXXXXXXXXXX'
    )

<h3>Após essas mudanças, a aplicação já está pronta para ser executada, necessitando apenas rodar o jogoteca.py.</h3>

<h3>Já é esperado que o próprio python e o pip esteja instalado, caso contrario, não será possivel executar a aplicação.</h3>


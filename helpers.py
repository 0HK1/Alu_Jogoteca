import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField


class FormularioJogo(FlaskForm):
    nome = StringField('Nome Do Jogo', [validators.data_required(), validators.length(min=1, max=50)])
    categoria = StringField('Nome Da Categoria', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('Nome Do Console', [validators.data_required(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')

class RegistrarUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.length(min=1, max=8)])
    usuario = StringField('Nome de Usuário', [validators.data_required(), validators.length(min=1, max=20)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    register = SubmitField('Registrar')

def recuperaImg(id):
    for nome_arquivos in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivos:
            return nome_arquivos

    return 'capa_basica.jpg'


def deletaArquivo(id):
    arquivo = recuperaImg(id)
    if arquivo != 'capa_basica.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

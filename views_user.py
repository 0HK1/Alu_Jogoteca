from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Usuarios
from helpers import FormularioUsuario


# Rota para adição de dados de novos usuários
@app.route('/register')
def register():
    return render_template('register.html')


# Endpoint para certificar dados da rota register
@app.route('/autenticarRegistro', methods=['POST', ])
def autenticarRegistro():
    nome = request.form['nome']
    nickname = request.form['nickname']
    senha = request.form['senha']

    userCheck = Usuarios.query.filter_by(nome=nome).first()
    if userCheck:
        flash('Nickname Já Registrado')
        return redirect(url_for("register"))

    novoUsuario = Usuarios(nome=nome, nickname=nickname, senha=senha)
    db.session.add(novoUsuario)
    db.session.commit()
    return redirect(url_for('login'))


# Rota para logar usuários
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


# Endpoint para certificar dados da rota login
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso! ')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        session['usuario_logado'] = request.form['usuario']
        flash('Senha Incorreta')
        return redirect('/login')


# Removendo dados do Cache
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuario Deslogado')
    return redirect(url_for('index'))


# Removendo dados de Usuários do BD, botão inserido na tela de novosjogos
@app.route('/deletarConta')
def deletarConta():
    conta = session['usuario_logado']
    if not session['usuario_logado']:
        flash('Conta não logada')
        return redirect(url_for('login'))
    else:
        Usuarios.query.filter_by(nickname=conta).delete()
        db.session.commit()
        flash('Conta deletada')
        return redirect(url_for('index'))

from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos, Usuarios


# Desenvolvimento das Rotas


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='JOGOS', nomeUsuario="Davi Beserra", jogos=lista)


@app.route('/novosjogos')
def novosjogos():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novosjogos').replace("/", "")))

    else:
        return render_template('novosJogos.html', titulo='Novo Jogo', nomeUsuario='Davi Beserra')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('novosjogos'))

    novoJogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novoJogo)
    db.session.commit()

    return redirect(url_for('novosjogos'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar').replace("/", "")))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Jogo', nomeUsuario='Davi Beserra', jogo=jogo)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado Com Sucesso')

    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template('register.html')


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


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso! ')
            proxima_pagina = 'novosjogos'  # request.form['proxima']
            return redirect(url_for(proxima_pagina))
    else:
        session['usuario_logado'] = request.form['usuario']
        flash('Senha Incorreta')
        return redirect('/login')


@app.route('/logout', methods=['POST', ])
def logout():
    session['usuario_logado'] = None
    flash('Usuario Deslogado')
    return redirect(url_for('index'))

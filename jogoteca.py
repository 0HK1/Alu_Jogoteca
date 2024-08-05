from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Davi Beserra', '0HK', 'Coxinha123')
usuario2 = Usuario('Pedro Henrique', 'PH', 'FastAndSpeed')
usuario3 = Usuario('Livia Santos', 'lilica', 'lilicaplays')
usuarios = {usuario1.nickname : usuario1, usuario2.nickname : usuario2, usuario3.nickname : usuario3}


jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack And Slash', 'PS4')
jogo3 = Jogo('State of Decay', 'Surviver', 'XBox')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'Coxinha123'


@app.route('/')
def index():
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
    appjogo = Jogo(nome, categoria, console)
    lista.append(appjogo)
    return redirect(url_for('novosjogos'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():

    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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


app.run(debug=True)

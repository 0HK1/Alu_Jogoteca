from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recuperaImg, deletaArquivo, FormularioJogo
import time


# Desenvolvimento das Rotas

# rota principal
@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='JOGOS', nomeUsuario="Davi Beserra", jogos=lista)


# novo jogo
@app.route('/novosjogos')
def novosjogos():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novosjogos').replace("/", "")))
    form = FormularioJogo()
    return render_template('novosJogos.html', titulo='Novo Jogo', nomeUsuario='Davi Beserra', form=form)


# endpoint enviando dados de novos jgos para o servidor
@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novosjogos'))

    nome = form.nome.data
    categoria = form.nome.data
    console = form.nome.data

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('novosjogos'))

    novoJogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novoJogo)
    db.session.commit()
    uploads_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f'{uploads_path}/capa{novoJogo.id}-{timestamp}.jpg')

    return redirect(url_for('novosjogos'))


# Aplicando Imagem ao endpoint novosjogos
@app.route('/imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


# Rota para editar jogos da lista
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()
    capaJogo = recuperaImg(id)

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    return render_template('editar.html',
                           titulo='Editando Jogo',
                           nomeUsuario='Davi Beserra',
                           id=id,
                           capaJogo=capaJogo,
                           form=form)


# endpoint para exutar ediciões do 'editar'
@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        uploads_path = app.config['UPLOAD_PATH']
        arquivo = request.files['arquivo']
        timestamp = time.time()
        deletaArquivo(jogo.id)
        arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


# Endpoint para adicionar botão de deletar na lista da rota principal
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado Com Sucesso')

    return redirect(url_for('index'))

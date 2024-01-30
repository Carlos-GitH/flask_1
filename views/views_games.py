from flask    import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models   import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo

import time

@app.route('/')
def index():
    """
    This function handles the route '/' and renders the index.html template with the title set to 'Jogos' and the games fetched from the database. 
    It also performs a check for the 'usuario_logado' in the session and redirects to the login page if not present.
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    title = 'Jogos'
    games = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', title=title, games=games)

@app.route('/novo')
def novo():
    """
    Handle the '/novo' route, check if the user is logged in, and render the 'novo.html' template.
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima='novo'))
    title = 'Novo Jogo'
    form = FormularioJogo()
    return render_template('novo.html', title=title, form=form)

@app.route('/criar', methods=['POST'])
def criar():
    """
    Function for creating a new entry in the database based on POST request data.
    If user is not logged in, redirects to the login page. 
    Parameters: None
    Return: Redirects to 'login' if user is not logged in, 
            redirects to 'novo' if the game already exists, 
            otherwise redirects to 'index'.
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    form = FormularioJogo(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    nome      = form.nome.data
    categoria = form.categoria.data
    console   = form.console.data
    
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('novo'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    
    arquivo = request.files['archive']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}\capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima='edit'))
    title = 'Editando jogo'
    game = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = game.nome
    form.categoria.data = game.categoria
    form.console.data = game.console
    game_cover = recupera_imagem(id)
    return render_template('edit.html', title=title, id=id, game_cover=game_cover, form=form)

@app.route('/update', methods=['POST'])
def update():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()
        arquivo = request.files['archive']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}\capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))
    
@app.route('/delete/<int:id>')
def delete(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    jogo = Jogos.query.filter_by(id=id).first()
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/img/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('img', nome_arquivo)
from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__ (self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

Jogo1 = Jogo('God of War', 'Ação', 'PS4')
Jogo2 = Jogo('Skyrim', 'RPG', 'PS4')
Jogo3 = Jogo('Fifa', 'Esportes', 'PS4')
Jogo4 = Jogo('Dota', 'Moba', 'PC')
games = [Jogo1, Jogo2, Jogo3, Jogo4]

class Usuário:
    def __init__ (self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuário('Carlos Cavalcanti', 'Cavalcanti', '1234')
usuario2 = Usuário('Bruno', 'Bruno', '1234')
usuario3 = Usuário('Heitor', 'Heitor', '1234')

usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    title = 'Jogos'
    return render_template('index.html', title=title, games=games)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima='novo'))
    title = 'Novo Jogo'
    return render_template('novo.html', title=title)

@app.route('/criar', methods=['POST'])
def criar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    nome      = request.form['nome']
    categoria = request.form['categoria']
    console   = request.form['console']
    jogo      = Jogo(nome, categoria, console)
    games.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    title = 'Login'
    return render_template('login.html', title=title, proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima = request.form['proxima']
            if proxima == 'None':
                return redirect(url_for('index'))
            else:
                return redirect(url_for(proxima))
    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('login'))

app.run(debug=True)
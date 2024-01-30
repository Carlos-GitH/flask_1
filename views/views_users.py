from flask import render_template, request, redirect, url_for, session, flash
from jogoteca import app
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    """
    Route for handling user login. Retrieves proxima and title from request arguments,
    then renders the login.html template with the retrieved title and proxima.
    """
    form = FormularioUsuario()
    proxima = request.args.get('proxima')
    title = 'Login'
    return render_template('login.html', title=title, proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    """
    Authenticate the user using the provided credentials and handle the appropriate
    redirection and flash messages based on the outcome.
    """
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        return redirect(url_for('index'))

    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    """
    Logout the current user by clearing the session and redirecting to the login page.
    No parameters.
    Returns a redirect response to the login page.
    """
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('login'))
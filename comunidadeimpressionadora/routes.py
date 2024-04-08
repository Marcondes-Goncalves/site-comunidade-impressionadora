
from flask import flash, render_template, redirect, url_for, request

from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario

# url_for está sendo utilizado nos links das páginas HTML, o mesmo referência as funções referentes ao seu ROUTE.

lista_usuarios: list[str] = ["Marcondes", "Maria", "Ana", "João", "Rosa"]

@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/contato")
def contato() -> str:
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios() -> str:
    return render_template("usuarios.html", lista_usuarios = lista_usuarios)


@app.route("/login", methods = ["GET", "POST"])
def login() -> str:
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        #Exibir msg de login bem sucedido
        flash(f"Login feito com sucesso no E-mail: {form_login.email.data}", 'alert-success')
        #Redirecionar para homepage
        return redirect(url_for('home'))
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #Criptografa a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #Criar o usuário
        usuario = Usuario(username = form_criarconta.username.data, email = form_criarconta.email.data, senha = senha_cript)
        #Adicionar a sessão
        database.session.add(usuario)
        #Commit na sessão
        database.session.commit()
        #Exibir msg de conta criada com sucesso
        flash(f"Conta criada com sucesso no E-mail: {form_criarconta.email.data}", 'alert-success')
        #Redirecionar para homepage
        return redirect(url_for('home'))
    
    return render_template("login.html", form_login = form_login, form_criarconta = form_criarconta)


from flask import flash, render_template, redirect, url_for, request

from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user

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
        # Verificando se o E-mail existe na tabela
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        # Se o E-mail existir e a senha digitada for igual a senha que está na tabela...
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # Fazendo o login, se o usuário marcar a opção de lembrar dados o próximo login será feito automaticamente.
            login_user(usuario, remember = form_login.lembrar_dados.data)
            #Exibir msg de login bem sucedido
            flash(f"Login feito com sucesso no E-mail: {form_login.email.data}", 'alert-success')
            #Redirecionar para homepage
            return redirect(url_for('home'))
        else:
            flash(f"Falha no login! E-mail ou senha incorretos ", 'alert-danger')
    
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


@app.route('/sair')
def sair():
    logout_user()
    flash(f"Logout feito com sucesso", 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')


@app.route('/post/criar')
def criar_post():
    return render_template('criarpost.html')



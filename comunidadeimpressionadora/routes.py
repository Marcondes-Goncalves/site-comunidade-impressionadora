
from flask import flash, render_template, redirect, url_for, request

from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required

import secrets
import os

from PIL import Image

# url_for está sendo utilizado nos links das páginas HTML, o mesmo referência as funções referentes ao seu ROUTE.

# login_required é um decorator que possibilita bloquear páginas caso o usuário não esteja logado.


@app.route("/")
def home() -> str:
    posts = Post.query.order_by(Post.id.desc())
    return render_template("home.html", posts = posts)


@app.route("/contato")
def contato() -> str:
    return render_template("contato.html")


@app.route("/usuarios")
@login_required
def usuarios() -> str:
    lista_usuarios = Usuario.query.all()
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
            # Redireciona o usuário para a página que ele estava tentando acessar antes de fazer o login. 
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
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
        # Fazendo o login
        login_user(usuario)
        #Redirecionar para homepage
        return redirect(url_for('home'))
    
    return render_template("login.html", form_login = form_login, form_criarconta = form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f"Logout feito com sucesso", 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil = foto_perfil)


def salvar_imagem(imagem):
    #código aleatorio
    codigo: str = secrets.token_hex(8)
    #separando o nome e a extensão da imagem
    nome, extensao = os.path.splitext(imagem.filename)
    #juntando o nome o código e a extensão
    nome_arquivo: str = nome + codigo + extensao
    #Local que a imagem será salva
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    #reduzuir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    #salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    
    return nome_arquivo


def atualizar_cursos(form: FormEditarPerfil):
    lista_cursos: list[str] = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    # percorre toda a lista e concatena seus valores, os separandos com ;
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods = ["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        
        current_user.cursos = atualizar_cursos(form)

        database.session.commit()
        flash(f"Perfil atualizado com sucesso", 'alert-success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil = foto_perfil, form = form)


@app.route('/post/criar', methods = ["GET", "POST"])
@login_required
def criar_post():
    form = FormCriarPost()

    if form.validate_on_submit():
        post = Post(titulo = form.titulo.data, corpo = form.corpo.data, autor = current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-sucess')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form = form)



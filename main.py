
from flask import Flask, render_template, url_for
from forms import FormCriarConta, FormLogin

# url_for está sendo utilizado nos links das páginas HTML, o mesmo referência as funções referentes ao seu ROUTE. 

app = Flask(__name__)

lista_usuarios: list[str] = ["Marcondes", "Maria", "Ana", "João", "Rosa"]

app.config["SECRET_KEY"] = '8c5762d6223bc0970d3936c2c0deb095'

@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/contato")
def contato() -> str:
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios() -> str:
    return render_template("usuarios.html", lista_usuarios = lista_usuarios)


@app.route("/login")
def login() -> str:
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template("login.html", form_login = form_login, form_criarconta = form_criarconta)



if __name__ == "main":
    app.run(debug = True)

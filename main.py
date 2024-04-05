
from flask import Flask, render_template, url_for


app = Flask(__name__)

lista_usuarios: list[str] = ["Marcondes", "Maria", "Ana", "João", "Rosa"]

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", lista_usuarios = lista_usuarios)




if __name__ == "main":
    app.run(debug = True)

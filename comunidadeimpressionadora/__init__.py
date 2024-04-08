
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

app = Flask(__name__)

app.config["SECRET_KEY"] = '8c5762d6223bc0970d3936c2c0deb095'

# caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)

#Criptografa as senhas
bcrypt = Bcrypt(app)

from comunidadeimpressionadora import routes

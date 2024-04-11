
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

import sqlalchemy

import os

app = Flask(__name__)

app.config["SECRET_KEY"] = '8c5762d6223bc0970d3936c2c0deb095'

# caminho do banco de dados
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

database = SQLAlchemy(app)

#Gerênciador de Login
login_manager = LoginManager(app)
#definindo para onde o usuário será redirecionado, caso tente acessar alguma página sem estar logado.
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login para acessar essa página'
login_manager.login_message_category = 'alert-info'

#Criptografa as senhas
bcrypt = Bcrypt(app)

from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])    
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table( "usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados criada")
else:
    print("Base de dados já existente")

from comunidadeimpressionadora import routes

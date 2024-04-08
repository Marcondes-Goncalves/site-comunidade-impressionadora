
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# url_for está sendo utilizado nos links das páginas HTML, o mesmo referência as funções referentes ao seu ROUTE. 

app = Flask(__name__)

app.config["SECRET_KEY"] = '8c5762d6223bc0970d3936c2c0deb095'

# caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)

from comunidadeimpressionadora import routes
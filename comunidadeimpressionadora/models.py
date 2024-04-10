
from comunidadeimpressionadora import database, login_manager
from datetime import datetime
# UserMixin possui as funções necessárias para gerênciar o login do usuário.
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    
    id: int = database.Column(database.Integer, primary_key = True)
    username: str = database.Column(database.String, nullable = False)
    senha: str = database.Column(database.String, nullable = False)
    email: str = database.Column(database.String, nullable = False, unique = True)
    foto_perfil: str = database.Column(database.String, default = 'default.jpg')

    cursos: str = database.Column(database.String, nullable = False, default = 'Não Informado')

    posts = database.relationship('Post', backref = 'autor', lazy = True)

    def contar_posts(self):
        return len(self.posts)
    

class Post(database.Model):

    id = database.Column(database.Integer, primary_key = True)
    titulo = database.Column(database.String, nullable = False)
    corpo = database.Column(database.Text, nullable = False)
    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.now())

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable = False)



from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import  DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    
    username: str = StringField("Nome do Usuário", validators = [DataRequired()])
    email: str = StringField("E-mail", validators = [DataRequired(), Email()])
    senha: str = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    confirmacao = PasswordField("Confirmação de senha", validators = [DataRequired(), EqualTo("senha")])
    botao_submit_criarconta = SubmitField("Criar Conta")


    #Validando se o E-mail já foi cadastrado.
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, cadastre-se com outro E-mail ou faça login para continuar')
        

class FormLogin(FlaskForm):

    email: str = StringField("E-mail", validators = [DataRequired(), Email()])
    senha: str = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField("Lembrar dados de acesso")
    botao_submit_login = SubmitField("Fazer Login")


class FormEditarPerfil(FlaskForm):
    
    username: str = StringField("Nome do Usuário", validators = [DataRequired()])
    email: str = StringField("E-mail", validators = [DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators = [FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField("Confirmar Edição")

    #Validando se o E-mail já foi cadastrado.
    def validate_email(self, email):
        #verificar se o usuario mudou de E-mail
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse E-mail, Cadastre outro E-mail.')
            
            
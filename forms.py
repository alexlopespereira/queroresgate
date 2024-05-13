from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Regexp
from wtforms.widgets import HiddenInput
from defs import DEBUG


class ResgateForm(FlaskForm):
    email = EmailField('Seu Email: ', validators=[InputRequired(message='Preencha seu email'), Email()], description="joao@gmail.com")
    telefone = StringField("Seu telefone: ", validators=[InputRequired(message='Preencha seu telefone')])
    nome = StringField("Seu nome: ", validators=[InputRequired(message='Preencha seu nome')])
    endereco = StringField("Endereço p/ resgate: ", validators=[InputRequired(message='Preencha seu endereço')])
    latlong = StringField(u'Marque no mapa a sua localização:', widget=HiddenInput())
    outrapessoa = BooleanField("Estou pedindo para outra pessoa")
    telefoneoutrapessoa = StringField("Telefone do outro: ")
    nomeoutrapessoa = StringField("Nome do outro: ")
    numpessoas = IntegerField("Número de pessoas")
    numanimais = IntegerField("Número de animais")
    informar = SubmitField('Solicitar Resgate')





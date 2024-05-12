from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms.widgets import HiddenInput
from defs import DEBUG


class ResgateForm(FlaskForm):
    email = EmailField('Email: ', validators=[InputRequired(message='Preencha seu email'), Email()], description="joao@gmail.com")
    telefone = StringField("Telefone: ", validators=[InputRequired(message='Preencha seu telefone')])
    nome = StringField("Nome: ", validators=[InputRequired(message='Preencha seu nome')])
    endereco = StringField("Endereço: ", validators=[InputRequired(message='Preencha seu endereço')])
    latlong = StringField(u'Marque no mapa a sua localização:', widget=HiddenInput())
    informar = SubmitField('Solicitar Resgate')





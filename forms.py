from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import HiddenInput
from defs import DEBUG


class ResgateForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired(), Email()], description="joao@gmail.com")
    telefone = StringField("Telefone: ", validators=[DataRequired()])
    nome = StringField("Nome: ", validators=[DataRequired()])
    endereco = StringField("Endereço: ", validators=[DataRequired()])
    latlong = StringField(u'Marque no mapa a sua localização:', widget=HiddenInput())
    informar = SubmitField('Informar')





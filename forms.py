from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Regexp
from wtforms.widgets import HiddenInput
from wtforms.widgets import TextArea
from wtforms.widgets.core import TableWidget

from defs import DEBUG, city_tuples


class ResgateForm(FlaskForm):
    telefone = StringField("Seu telefone: ", validators=[InputRequired(message='Preencha seu telefone')])
    nome = StringField("Seu nome: ", validators=[InputRequired(message='Preencha seu nome')])
    endereco = StringField("Endereço: ", validators=[InputRequired(message='Preencha seu endereço')])
    complemento = StringField("Complemento: ")
    pontoreferencia = StringField("Ponto de Referencia: ")
    numero = StringField("Numero: ")
    bairro = StringField("Bairro: ", validators=[InputRequired(message='Preencha seu bairo')])
    cep = StringField("CEP: ")
    observacoes = StringField("Observacoes: ", widget=TextArea())
    estado = SelectField("Estado: ", choices=[("RS", "RS")], validators=[DataRequired()], default="RS")
    cidade = SelectField('Cidade', choices=city_tuples, validators=[DataRequired()], default="Porto Alegre")
    latlong = StringField(u'Marque no mapa a sua localização:', widget=HiddenInput())
    outrapessoa = BooleanField("Estou pedindo para outra pessoa")
    idosos = BooleanField("Estou pedindo para outra pessoa")
    criancas = BooleanField("Estou pedindo para outra pessoa")
    pessoacomdeficiencia = BooleanField("Estou pedindo para outra pessoa")
    telefoneoutrapessoa = StringField("Telefone do outro: ")
    nomeoutrapessoa = StringField("Nome do outro: ")
    numpessoas = IntegerField("Número de pessoas")
    numanimais = IntegerField("Número de animais")
    resgate_pra_voce = RadioField('Label', choices=[('yes', 'Sim'), ('no', 'Não')], widget=TableWidget(with_table_tag=False), default='yes' )
    consentimento = BooleanField("Ao enviar essa solicitação, você concorda com o compartilhamento dos dados informados com as equipes voluntárias e órgãos públicos atuantes nos resgates.", default=True)






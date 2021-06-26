from datetime import datetime

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, RadioField, FloatField, IntegerField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import HiddenInput
# from recaptcha3 import Recaptcha3Field
from defs import DEBUG


class VacinaForm(FlaskForm):
    vacina = RadioField('Vacina que tomei: ', choices=[('coronavac', 'Coronavac'), ('astrazeneca', 'Astrazeneca'), ('pfizer', 'Pfizer')],
                        validators=[DataRequired()])
    email = EmailField('Email: ',validators=[DataRequired(), Email()], description="joao@gmail.com")
    idade = IntegerField("Idade: ", description="50", validators=[DataRequired()])
    data = StringField("Data da vacinação: ", default=datetime.today().strftime("%d-%m-%Y"), validators=[DataRequired()])
    if not DEBUG:
        recaptcha = RecaptchaField()
    latlong = StringField(u'LagLong', widget=HiddenInput(), default='-15.7801,-47.9292')

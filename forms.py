from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, RadioField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import HiddenInput
from defs import DEBUG

class VacinaForm(FlaskForm):
    vacina = RadioField('Vacina que tomei:', choices=[('coronavac','Coronavac'),('astrazeneca','Astrazeneca'), ('pfizer','Pfizer')],
                         validators=[DataRequired()])
    email = EmailField('Email:', [DataRequired(), Email()])
    if not DEBUG:
        recaptcha = RecaptchaField()
    latlong = StringField(u'LagLong', widget=HiddenInput(), default='-15.7801,-47.9292')

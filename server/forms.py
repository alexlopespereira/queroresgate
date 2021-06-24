from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class VacinaForm(FlaskForm):
    vacina = RadioField('Label', choices=[('coronavac','Coronavac'),('astrazeneca','Astrazeneca'), ('pfizer','Pfizer')],
                         validators=[DataRequired()])
    email = EmailField('Email address', [DataRequired(), Email()])
from datetime import datetime

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, RadioField, IntegerField, DateTimeField, SelectField, SelectMultipleField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import HiddenInput, ListWidget, CheckboxInput
from defs import DEBUG


class VacinaForm(FlaskForm):
    vacina = RadioField('Vacina que tomei: ', choices=[('coronavac', 'Coronavac'), ('astrazeneca', 'Astrazeneca'), ('pfizer', 'Pfizer'), ('jansen', 'Jansen')],
                        validators=[DataRequired()])
    email = EmailField('Email: ',validators=[DataRequired(), Email()], description="joao@gmail.com")
    idade = IntegerField("Idade: ", description="50", validators=[DataRequired()])
    data = StringField("Data da vacinação: ", default=datetime.today().strftime("%d-%m-%Y"), validators=[DataRequired()])
    desperdicio = SelectField(u'Há doses remanescentes hoje: ', choices=[(1, 'Sim'), (0, 'Não')], default=0, coerce=int)
    if not DEBUG:
        recaptcha = RecaptchaField()
    latlong = StringField(u'Marque no mapa o seu local de vacinação:', widget=HiddenInput())


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class AlertaForm(FlaskForm):
    vacina = MultiCheckboxField('Me alerte para doses remanescentes da:',
        choices=[('coronavac', 'Coronavac'), ('astrazeneca', 'Astrazeneca'), ('pfizer', 'Pfizer'), ('jansen', 'Jansen')]
    )
    email = EmailField('Email: ', validators=[DataRequired(), Email()], description="joao@gmail.com")
    if not DEBUG:
        recaptcha = RecaptchaField()
    latlong = StringField(u'Clique para mover sua região de interesse:', widget=HiddenInput())
    registrar = SubmitField('Registrar Área de Interesse')
    descadastrar = SubmitField('Remover Alerta')


class DescadastrarForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired(), Email()], description="joao@gmail.com")

# class AlertaForm(FlaskForm):
#     item_id = HiddenField()
#     want = BooleanField()
#
#
# class VacinaListForm(FlaskForm):
#     def __init__(self, *args, **kwargs):
#         super(VacinaListForm, self).__init__(*args, **kwargs)
#
#         # just a little trickery to get custom labels
#         # on the list's checkboxes
#         for item_form in self.items:
#             for item in kwargs['data']['items']:
#                 if item.item_id == item_form.item_id.data:
#                     item_form.want.label = ''
#                     item_form.label = item.name
#
#     items = FieldList(FormField(AlertaForm), widget=ListWidget(prefix_label=False))
#


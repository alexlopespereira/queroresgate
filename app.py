import json
import sys
import urllib
import os
# from flask_recaptcha import ReCaptcha
import requests as requests
from flask import Flask, render_template, flash
from flask import request
from datetime import datetime

from forms import ResgateForm
from defs import DEBUG, SIDE
import dateutil.parser
from flask_bootstrap import Bootstrap
# from flaskext.markdown import Markdown

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
APP_PORT = 8080


app = Flask(__name__)
# recaptcha = ReCaptcha(app=app)
bootstrap = Bootstrap(app)
# Markdown(app)

app.config['SECRET_KEY'] = SECRET_KEY
# app.config['RECAPTCHA_ENABLED'] = True
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc9Y1obAAAAAM-7g3G29a_-CHg2O0Cl81YAR-0l'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc9Y1obAAAAAN6YQEC1nLkyAp03FQMpemNiKc7M'
# app.config['RECAPTCHA_THEME'] = 'white'
# app.config['RECAPTCHA_TYPE'] = 'image'
# app.config['RECAPTCHA_SIZE'] = 'compact'
# app.config['RECAPTCHA_USE_SSL'] = False
# app.config['RECAPTCHA_RTABINDEX'] = 10

records = []



def descadastrar_notificacao(email):
    #TODO: implementar o descadastro
    return True


def get_geolocation(ip):
    url = 'http://freegeoip.net/json/{}'.format(ip)
    r = requests.get(url)
    j = json.loads(r.text)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        form = ResgateForm(request.form)
        if form.validate_on_submit():
            latlong = form.latlong.data
            email = form.email.data
            localtion = [float(f) for f in latlong.split(',')]
            # enviar email
            return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=False, popup_message="Estou aqui",
                                   email=form.email.data, origem=localtion)
        else:
            flash('Todos os campos são obrigatórios', category='error')
            return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, popup_message="Estou aqui")

    else:
        form = ResgateForm()
        return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, popup_message="Estou aqui")


# @app.route('/solicitar', methods=['GET', 'POST'])
# def solicitar():
#     if request.method == "POST":
#         form = NotificacaoForm(request.form)
#         if form.validate_on_submit():
#             latlong = form.latlong.nome
#             global records
#             records = []
#             for v in form.vacina.nome:
#                 records.append({"location": latlong, "vacina": v, "date": datetime.utcnow().isoformat(),
#                                 'email': form.email.nome, "id": f"{form.email.nome}_{v}"})
#             orig = [float(f) for f in latlong.split(',')]
#             return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=False, email=form.email.nome, origem=orig,
#                                    popup_message="Sua área foi registrada aqui", side=SIDE)
#         else:
#             flash('Todos os campos são obrigatórios', category='error')
#             return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, side=SIDE)
#     else:
#         form = NotificacaoForm()
#         return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, side=SIDE)
#

@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')



if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    else:
        if DEBUG:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT, ssl_context='adhoc')
        else:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT)  # , ssl_context='adhoc')

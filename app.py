import json
import sys
import urllib

import elasticsearch
from elasticsearch.helpers import bulk
from flask_recaptcha import ReCaptcha
import requests as requests
from flask import Flask, render_template, flash
from flask import request
from datetime import datetime

from elk.settings_notificacao import body_settings_notificacao
from forms import VacinaForm, NotificacaoForm, DescadastrarForm  # , VacinaListForm
from defs import es, ES_VACINEI_INDEX, body_settings_vacinei, APP_PORT, DASHBOARD_URL, DEBUG, SECRET_KEY, SIDE, ES_NOTIFICACAO_INDEX
import dateutil.parser
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown


def check_or_create_index(esc, index, settings):
    response = esc.indices.exists(index)
    if response is True:
        return "EXISTED"
    else:
        esc.indices.create(index, body=settings)
        return "CREATED"


try:
    check_or_create_index(es, ES_VACINEI_INDEX, body_settings_vacinei)
    check_or_create_index(es, ES_NOTIFICACAO_INDEX, body_settings_notificacao)
except elasticsearch.exceptions.ConnectionError as e:
    print(e)
    pass

app = Flask(__name__)
recaptcha = ReCaptcha(app=app)
Bootstrap(app)
Markdown(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc9Y1obAAAAAM-7g3G29a_-CHg2O0Cl81YAR-0l'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc9Y1obAAAAAN6YQEC1nLkyAp03FQMpemNiKc7M'
app.config['RECAPTCHA_THEME'] = 'white'
app.config['RECAPTCHA_TYPE'] = 'image'
app.config['RECAPTCHA_SIZE'] = 'compact'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_RTABINDEX'] = 10
brasilia = [-15.7801, -47.9292]
records = []


def gendata():
    global records
    for r in records:
        doc = {"doc": r, "_id": f"{r['email']}_{r['vacina']}", '_op_type': 'update', 'doc_as_upsert': True, '_index': ES_NOTIFICACAO_INDEX}
        yield doc


def descadastrar_notificacao(email):
    #TODO: implementar o descadastro
    return True


def get_geolocation(ip):
    url = 'http://freegeoip.net/json/{}'.format(ip)
    r = requests.get(url)
    j = json.loads(r.text)


@app.route('/', methods=['GET', 'POST'])
def index():
    current_hour = datetime.utcnow().hour
    inappropriate_time = current_hour > 21 or current_hour < 15
    if request.method == "POST":
        form = VacinaForm(request.form)
        if form.validate_on_submit():
            latlong = form.latlong.data
            data_vacinacao = dateutil.parser.parse(form.data.data)
            es.index(ES_VACINEI_INDEX,
                     body={"location": latlong, "idade": form.idade.data, "data_vacinacao": data_vacinacao, "desperdicio": form.desperdicio.data == 1,
                           "vacina": form.vacina.data, "date": datetime.utcnow().isoformat(), "email": form.email.data},
                     id=form.email.data, doc_type="_doc")
            orig = [float(f) for f in latlong.split(',')]
            return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=False, popup_message="Me vacinei aqui",
                                   email=form.email.data, inappropriate_time=inappropriate_time, origem=orig)
        else:
            flash('Todos os campos são obrigatórios', category='error')
            return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, popup_message="Me vacinei aqui",
                                   inappropriate_time=inappropriate_time)

    else:
        form = VacinaForm()
        return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, popup_message="Me vacinei aqui",
                               inappropriate_time=inappropriate_time)


@app.route('/visualizar', methods=['GET'])
def visualizar():
    return render_template('visualizar.html', dashboard_url=DASHBOARD_URL)


@app.route('/notificacao', methods=['GET', 'POST'])
def notificacao():
    if request.method == "POST":
        form = NotificacaoForm(request.form)
        if form.validate_on_submit():
            if 'registrar' in request.form:
                latlong = form.latlong.data
                global records
                records = []
                for v in form.vacina.data:
                    records.append({"location": latlong, "vacina": v, "date": datetime.utcnow().isoformat(),
                                    'email': form.email.data, "id": f"{form.email.data}_{v}"})
                bulk(es, gendata())
                orig = [float(f) for f in latlong.split(',')]
                return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=False, email=form.email.data, origem=orig,
                                       popup_message="Sua área foi registrada aqui", side=SIDE)
            else:
                ret = descadastrar_notificacao(form.email.data)
                if ret:
                    msg = "Sua notificação foi removida com sucesso"
                else:
                    msg = "Ocorreu um problema ao remover sua notificação. Tente novamente mais tarde."
                return render_template('mensagem.html', msg=msg)
        else:
            flash('Todos os campos são obrigatórios', category='error')
            return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, side=SIDE)
    else:
        form = NotificacaoForm()
        # form = VacinaForm(data=MultiDict(data_items))
        return render_template('notificacao.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, side=SIDE)


@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@app.route('/descadastrar', methods=['POST'])
def descadastrar():
    descadastrar_form = DescadastrarForm()
    return render_template('notificacao.html', descadastrar_form=descadastrar_form)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    else:
        if DEBUG:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT, ssl_context='adhoc')
        else:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT)  # , ssl_context='adhoc')

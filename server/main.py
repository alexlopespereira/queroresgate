import json
import sys
from flask_recaptcha import ReCaptcha
import requests as requests
from flask import Flask, render_template, jsonify
from flask import request
from datetime import datetime
from forms import VacinaForm
from defs import es, ES_VACINEI_INDEX, body_settings_vacinei
import re

def check_or_create_index(esc, index, settings):
    response = esc.indices.exists(index)
    if response is True:
        return "EXISTED"
    else:
        esc.indices.create(index, body=settings)
        return "CREATED"


check_or_create_index(es, ES_VACINEI_INDEX, body_settings_vacinei)

SECRET_KEY = 'development'
app = Flask(__name__)
recaptcha = ReCaptcha(app=app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LflH3UUAAAAAN04iK_OASgI59B26iA-gPJBoDVO'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LflH3UUAAAAAMP-x2-Dgf0R40rTTGcWoqSwG7LP'
app.config['RECAPTCHA_THEME'] = 'white'
app.config['RECAPTCHA_TYPE'] = 'image'
app.config['RECAPTCHA_SIZE'] = 'compact'
app.config['RECAPTCHA_RTABINDEX'] = 10
brasilia = [-15.7801, -47.9292]

def get_geolocation(ip):
    url = 'http://freegeoip.net/json/{}'.format(ip)
    r = requests.get(url)
    j = json.loads(r.text)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = VacinaForm(request.form)
    orig = brasilia
    if request.method == "POST" and form.validate_on_submit():
        # print(form.vacina.data)
        # ip = request.remote_addr
        latlong = form.latlong.data
        es.index(ES_VACINEI_INDEX, body={"location": latlong,
                                         "vacina": form.vacina.data, "date": datetime.utcnow().isoformat()}, id=form.email.data, doc_type="_doc")
        orig = latlong.split(',')
    else:
        print(form.errors)
    # lat, long = get_geolocation(ip)


    return render_template('index.html', form=form, origem=orig)


@app.route('/visualizar', methods=['GET'])
def visualizar():
    return render_template('visualizar.html')



if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    else:
        app.run(debug=True, host='0.0.0.0') #, ssl_context='adhoc')

import json
import sys
import os
import requests as requests
from flask import Flask, render_template, flash, abort
from flask import request

from forms import ResgateForm
from defs import DEBUG, VERIFY_URL
from flask_bootstrap import Bootstrap


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
APP_PORT = 8080


app = Flask(__name__)
# recaptcha = ReCaptcha(app=app)
bootstrap = Bootstrap(app)
# Markdown(app)

app.config['SECRET_KEY'] = SECRET_KEY
# app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

records = []



def descadastrar_notificacao(email):
    #TODO: implementar o descadastro
    return True


def get_geolocation(ip):
    url = 'http://freegeoip.net/json/{}'.format(ip)
    r = requests.get(url)
    j = json.loads(r.text)


@app.route('/', methods=['GET'])
def index():
    form = ResgateForm()
    return render_template('index.html', form=form, torecaptcha=DEBUG == False, tosubmit=True, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY)

@app.route('/solicitar', methods=['POST'])
def solicitar():
    form = ResgateForm(request.form)
    secret_response = request.form['g-recaptcha-response']

    verify_response = requests.post(url=f'{VERIFY_URL}?secret={RECAPTCHA_PRIVATE_KEY}&response={secret_response}').json()

    if verify_response['success'] == False or verify_response['score'] < 0.5:
        abort(401)

    latlong = form.latlong.data
    email = form.email.data
    localtion = [float(f) for f in latlong.split(',')]

    return render_template('message.html', msg="Enviamos um email para as forças de segurança com os seus dados.")

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

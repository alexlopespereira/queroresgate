import datetime
import json
import sys
import os
import requests as requests
from flask import Flask, render_template, abort, flash
from flask import request
from requests.structures import CaseInsensitiveDict
from forms import ResgateForm
from defs import DEBUG, VERIFY_URL, contatos
from flask_bootstrap import Bootstrap

from dotenv import load_dotenv, find_dotenv

from github import create_issue
from send_email import send_email

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
GEOAPIFY_KEY = os.getenv('GEOAPIFY_KEY')
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
    return render_template('index.html', form=form, torecaptcha=DEBUG == False, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY)

@app.route('/solicitar', methods=['POST'])
def solicitar():
    form = ResgateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        secret_response = request.form['g-recaptcha-response']

        verify_response = requests.post(url=f'{VERIFY_URL}?secret={RECAPTCHA_PRIVATE_KEY}&response={secret_response}').json()

        # if verify_response['success'] == False or verify_response['score'] < 0.5:
        #     abort(401)

        latlong = form.latlong.data
        email = form.email.data
        nome = form.nome.data
        telefone = form.telefone.data
        endereco = form.endereco.data
        outrapessoa = form.outrapessoa.data
        nomeoutrapessoa = form.nomeoutrapessoa.data
        telefoneoutrapessoa = form.telefoneoutrapessoa.data
        numpessoas = form.numpessoas.data
        numanimais = form.numanimais.data

        if email == '' or nome == '' or telefone == '' or endereco == '':
            flash('Todos os campos são obrigatórios', category='error')
            return render_template('index.html', form=form, torecaptcha=DEBUG == False, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY, error_message="Preencha todos os campos")
        location = [float(f) for f in latlong.split(',')]
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={location[0]}&lon={location[1]}&apiKey={GEOAPIFY_KEY}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        try:
            resp = requests.get(url, headers=headers)
            data = json.loads(resp.text)
        except Exception as e:
            return render_template('message.html', msg="Não foi possível processar a sua solicitação. Tente novamente mais tarde.")

        city = data['features'][0]['properties']['city']
        state = data['features'][0]['properties']['state']
        county = data['features'][0]['properties']['county']
        geocoding_address = data['features'][0]['properties']['formatted']
        if state.upper() != "RIO GRANDE DO SUL" and county.upper() != "RIO GRANDE DO SUL" and county.upper() != 'FEDERAL DISTRICT':
            return render_template('message.html', msg="No momento só cadastramos os dados de contato dos órgãos de defesa civil do Rio Grande do Sul.")
        else:
            if city in contatos.keys():
                orgao = contatos[city]['orgao']
                dest_email = contatos[city]['email']
            else:
                orgao = contatos["Porto Alegre"]['orgao']
                dest_email = contatos["Porto Alegre"]['email']
            send_email(orgao, dest_email, nome, email, telefone, endereco, latlong, geocoding_address, numpessoas, numanimais, outrapessoa, telefoneoutrapessoa, nomeoutrapessoa)
            if outrapessoa:
                body = f"""- Nome do solicitante: {nome}
                            - Telefone do solicitante: {telefone}
                            - Endereço informado: {endereco}
                            - Endereço geo: {geocoding_address}
                            - Nome do necessitado: {nomeoutrapessoa}
                            - Telefone do necessitado: {telefoneoutrapessoa}
                            - Número de pessoas: {numpessoas}
                            - Número de animais: {numanimais}
                            - Data / Hora: {datetime.datetime.now()}
                            - [Geolocalizacao](http://maps.google.com/?q={latlong})
                            """
            else:
                body = f"""- Nome: {nome}
                        - Email: {email}
                        - Telefone: {telefone}
                        - Endereço informado: {endereco}
                        - Endereço geo: {geocoding_address}
                        - Número de pessoas: {numpessoas}
                        - Número de animais: {numanimais}
                        - Data / Hora: {datetime.datetime.now()}
                        - [Geolocalizacao](http://maps.google.com/?q={latlong})
                        """

            create_issue(f"demanda de: {nome} / {city}", body)
            return render_template('message.html', msg="Enviamos um email para as forças de segurança com os seus dados.")
    else:
        flash('Todos os campos são obrigatórios', category='danger')
        return render_template('index.html', form=form, torecaptcha=DEBUG == False, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY, error_message="Preencha todos os campos")
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

import datetime
import json
import sys
import os
import requests as requests
from flask import Flask, render_template, abort, flash
from flask import request
from requests.structures import CaseInsensitiveDict
from forms import ResgateForm
from defs import DEBUG, VERIFY_URL, contatos, cities, city_tuples
from flask_bootstrap import Bootstrap

from dotenv import load_dotenv, find_dotenv

from github import create_issue
from google_api import get_geocode_from_zipcode, add_line_to_sheet
from send_email import send_email
import pytz

timezone = pytz.timezone('Etc/GMT+3')

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
GEOAPIFY_KEY = os.getenv('GEOAPIFY_KEY')
SHEET_KEY = os.getenv('SHEET_KEY')
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
    # form.cidade.choices = city_tuples
    return render_template('index.html', form=form, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY)

@app.route('/solicitar', methods=['POST'])
def solicitar():
    form = ResgateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        secret_response = request.form['g-recaptcha-response']

        verify_response = requests.post(url=f'{VERIFY_URL}?secret={RECAPTCHA_PRIVATE_KEY}&response={secret_response}').json()

        if verify_response['success'] == False or verify_response['score'] < 0.5:
            abort(401)

        latlong = form.latlong.data
        telefone = form.telefone.data
        nome = form.nome.data
        telefoneoutrapessoa = form.telefoneoutrapessoa.data
        nomeoutrapessoa = form.nomeoutrapessoa.data

        cep = form.cep.data
        rua = form.endereco.data
        numero = form.numero.data
        complemento = form.complemento.data
        bairro = form.bairro.data
        cidade = form.cidade.data
        pontoreferencia = form.pontoreferencia.data
        estado = form.estado.data

        numpessoas = form.numpessoas.data
        numanimais = form.numanimais.data

        idosos = form.idosos.data
        criancas = form.criancas.data
        pessoacomdeficiencia = form.pessoacomdeficiencia.data

        location = [float(f) for f in latlong.split(',')]
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={location[0]}&lon={location[1]}&apiKey={GEOAPIFY_KEY}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        try:
            resp = requests.get(url, headers=headers)
            data = json.loads(resp.text)
        except Exception as e:
            return render_template('message.html', msg=f"Não foi possível processar a sua solicitação. Tente novamente mais tarde. Erro:{form.errors}")

        city = data['features'][0]['properties']['city']
        state = data['features'][0]['properties']['state']
        county = data['features'][0]['properties']['county']
        geocoding_address = data['features'][0]['properties']['formatted']
        if state.upper() != "RIO GRANDE DO SUL" and county.upper() != "RIO GRANDE DO SUL" and county.upper() != 'FEDERAL DISTRICT':
            return render_template('message.html', msg="No momento só cadastramos os dados de contato dos órgãos de defesa civil do Rio Grande do Sul.")
        else:
            if not DEBUG:
                if city in contatos.keys():
                    orgao = contatos[city]['orgao']
                    dest_email = contatos[city]['email']
                else:
                    orgao = contatos["Porto Alegre"]['orgao']
                    dest_email = contatos["Porto Alegre"]['email']
            else:
                orgao = "Defesa Civil da CIDADE X"
                dest_email = "alexlopespereira@gmail.com"

            utc_now = datetime.datetime.now(pytz.utc)
            utc_minus_3 = utc_now.astimezone(timezone)
            send_email(orgao, dest_email, form.data, geocoding_address, utc_minus_3)
            sheets_data = [nome, telefone, nomeoutrapessoa, telefoneoutrapessoa, rua, numero, complemento, bairro, pontoreferencia, estado, numpessoas, numanimais, idosos, criancas, pessoacomdeficiencia, f"http://maps.google.com/?q={latlong}"]
            add_line_to_sheet(sheets_data, SHEET_KEY)
            if form.resgate_pra_voce.data == 'yes':
                body = f"""- Nome do solicitante: {nome}
                            - Telefone do solicitante: {telefone}
                            - Resgate foi pra quem solicitou: Sim
                            - Rua: {rua}
                            - Número: {numero}
                            - Complemento: {complemento}
                            - Bairro: {bairro}
                            - Ponto de Referência: {pontoreferencia}
                            - Cidade: {cidade}
                            - CEP: {cep}                               
                            - Estado: {estado}
                            - Endereço geo: {geocoding_address}                            
                            - Número de pessoas: {numpessoas}
                            - Há idosos: {"Sim" if idosos else "Não"}
                            - Há crianças: {"Sim" if criancas else "Não"}
                            - Há pessoas com deficiência: {"Sim" if pessoacomdeficiencia else "Não"}
                            - Número de animais: {numanimais}
                            - Data / Hora: {utc_minus_3}
                            - [Geolocalizacao](http://maps.google.com/?q={latlong})
                            """
            else:
                body =  f"""- Nome do solicitante: {nomeoutrapessoa}
                            - Telefone do solicitante: {telefoneoutrapessoa}
                            - Resgate foi pra quem solicitou: Não
                            - Rua: {rua}
                            - Número: {numero}
                            - Complemento: {complemento}
                            - Bairro: {bairro}
                            - Ponto de Referência: {pontoreferencia}
                            - Cidade: {cidade}
                            - CEP: {cep}                               
                            - Estado: {estado}
                            - Endereço geo: {geocoding_address}                            
                            - Número de pessoas: {numpessoas}
                            - Há idosos: {"Sim" if idosos else "Não"}
                            - Há crianças: {"Sim" if criancas else "Não"}
                            - Há pessoas com deficiência: {"Sim" if pessoacomdeficiencia else "Não"}
                            - Número de animais: {numanimais}
                            - Data / Hora: {utc_minus_3}
                            - [Geolocalizacao](http://maps.google.com/?q={latlong})
                            """

            create_issue(f"demanda de: {nome} / {city}", body)
            return render_template('message.html', msg="Enviamos um email para as forças de segurança com os seus dados.")
    else:
        flash('Os seguintes campos são obrigatórios', category='danger')
        form.cidade.choices = city_tuples
        return render_template('index.html', form=form, torecaptcha=DEBUG == False, popup_message="Estou aqui", site_key=RECAPTCHA_PUBLIC_KEY, error_message="Preencha todos os campos")
@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@app.route('/address', methods=['POST'])
def address():
    print(request)
    data_addr = get_geocode_from_zipcode(json.loads(request.data)['zipCode'])
    return data_addr


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    else:
        if DEBUG:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT, ssl_context='adhoc')
        else:
            app.run(debug=True, host='0.0.0.0', port=APP_PORT)  # , ssl_context='adhoc')

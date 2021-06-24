import json
import sys
from flask_recaptcha import ReCaptcha
import requests as requests
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

from forms import VacinaForm

SECRET_KEY = 'development'
app = Flask(__name__)
recaptcha = ReCaptcha(app=app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_SITE_KEY'] = '6LflH3UUAAAAAN04iK_OASgI59B26iA-gPJBoDVO'
app.config['RECAPTCHA_SECRET_KEY'] = '6LflH3UUAAAAAMP-x2-Dgf0R40rTTGcWoqSwG7LP'
app.config['RECAPTCHA_THEME'] = 'white'

app.config['RECAPTCHA_TYPE'] = 'image'
app.config['RECAPTCHA_SIZE'] = 'compact'
app.config['RECAPTCHA_RTABINDEX'] = 10


db = SQLAlchemy(app)

BASECOORDS = [-13.9626, 33.7741]

def get_geolocation(ip):
    url = 'http://freegeoip.net/json/{}'.format(ip)
    r = requests.get(url)
    j = json.loads(r.text)
    city = j['city']

    print(city)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VacinaForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        print(form.vacina.data)
        ip = request.remote_addr
        # lat, long = get_geolocation(ip)
    else:
        print(form.errors)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    else:
        app.run(debug=True, host='0.0.0.0') #, ssl_context='adhoc')

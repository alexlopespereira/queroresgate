import os

from elasticsearch import Elasticsearch
from elk.settings_vacinei import body_settings_vacinei

DEBUG = os.environ.get('DEBUG') == "True"
SECRET_KEY = os.environ.get('SECRET_KEY') or 'developmentdfgsdg43539405332dfgsdf'
ES_HOST = os.environ.get('ES_HOST') or 'e.vacinei.org'
ES_PORT = os.environ.get('ES_PORT') or '9200'
ES_USER = os.environ.get('ES_USER') or 'elastic'
ES_PASSWORD = os.environ.get('ES_PASSWORD') or 'pass'  ## Setar Variavel de Ambiente
ES_USE_SSL = os.environ.get('ES_USE_SSL') == "True"
ES_VERIFY_CERTS = os.environ.get('ES_VERIFY_CERTS') == "True"
DASHBOARD_URL = os.environ.get('DASHBOARD_URL') or 'https://k.vacinei.org:5601/app/dashboards#/view/e6ac2260-d63a-11eb-b7e8-bdf162e86103?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))&show-time-filter=true&hide-filter-bar=true'

if ES_USE_SSL:
    APP_PORT = 443
    ES_URL = "https://{0}".format(ES_HOST)
else:
    APP_PORT = 5000
    ES_URL = "http://{0}:{1}".format(ES_HOST, ES_PORT)
ES_VACINEI_INDEX = os.environ.get('ES_ESOCIAL_INDEX') or 'vacinei__vacinei'
job_vacinei = {"index": ES_VACINEI_INDEX, "settings": body_settings_vacinei, "namespace": "default"}
INDEXES = {'vacinei': job_vacinei}

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}],
    http_auth=(ES_USER, ES_PASSWORD),
    use_ssl=ES_USE_SSL,
    verify_certs=ES_VERIFY_CERTS
)



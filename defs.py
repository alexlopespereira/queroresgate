import os
from elasticsearch import Elasticsearch
try:
    from elk.settings_mensagens import body_settings_mensagens
    from elk.settings_vacinei import body_settings_vacinei
except Exception:
    from settings_mensagens import body_settings_mensagens
    from settings_vacinei import body_settings_vacinei

DEBUG = os.environ.get('DEBUG') == "True"
SECRET_KEY = os.environ.get('SECRET_KEY') or 'developmentdfgsdg43539405332dfgsdf'
ES_HOST = os.environ.get('ES_HOST') or 'e.vacinei.org'
ES_PORT = os.environ.get('ES_PORT') or '9200'
ES_USER = os.environ.get('ES_USER') or 'elastic'
ES_PASSWORD = os.environ.get('ES_PASSWORD') or 'pass'  ## Setar Variavel de Ambiente
ES_USE_SSL = os.environ.get('ES_USE_SSL') == "True"
ES_VERIFY_CERTS = os.environ.get('ES_VERIFY_CERTS') == "True"
DASHBOARD_URL = os.environ.get('DASHBOARD_URL') or "https://k.vacinei.org:5601/app/dashboards?auth_provider_hint=anonymous1#/view/e6ac2260-d63a-11eb-b7e8-bdf162e86103?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-3d%2Cto%3Anow))&show-time-filter=true&hide-filter-bar=true"
SIDE = os.environ.get('SIDE') or 0.02

if ES_USE_SSL:
    APP_PORT = 8080
    ES_URL = "https://{0}".format(ES_HOST)
else:
    APP_PORT = 5000
    ES_URL = "http://{0}:{1}".format(ES_HOST, ES_PORT)
ES_VACINEI_INDEX = os.environ.get('ES_VACINEI_INDEX') or 'vacinei__vacinei'
ES_NOTIFICACAO_INDEX = os.environ.get('ES_NOTIFICACAO_INDEX') or 'alerta__alerta'
ES_MENSAGENS_INDEX = os.environ.get('ES_MENSAGENS_INDEX') or 'mensagens__mensagens'
job_vacinei = {"index": ES_VACINEI_INDEX, "settings": body_settings_vacinei, "namespace": "default"}
job_notificacao = {"index": ES_NOTIFICACAO_INDEX, "settings": body_settings_vacinei, "namespace": "default"}
job_mensagens = {"index": ES_MENSAGENS_INDEX, "settings": body_settings_mensagens, "namespace": "default"}
INDEXES = {'vacinei': job_vacinei, 'notificacao': job_notificacao, 'mensagens': job_mensagens}

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': ES_PORT}],
    http_auth=(ES_USER, ES_PASSWORD),
    use_ssl=ES_USE_SSL,
    verify_certs=ES_VERIFY_CERTS
)



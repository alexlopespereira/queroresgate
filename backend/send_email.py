import os
from time import sleep

import yagmail

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

vacinei_user = 'demanda.resgate@gmail.com'
vacinei_app_password = GMAIL_PASSWORD

direct_user = 'alexlopespereira@gmail.com'
direct_app_password = 'minhasenha'


def send_email(org_dest, nome, email, google_maps_url):
    subject = 'Alerta de Vacina Disponível'
    html = f"""\
    <html>
      <body>
        <p>Prezado representante do(a) {org_dest},<br>
           Informamos que a pessoa abaixo qualificada solicitou resgate por meio da nossa plataforma. 
        </p>
        <p>
        
        <a href="{google_maps_url}">aqui</a>  <br>
           Recomendamos ligar no local de vacinação para validar a informação antes de comparecer. <br>
           Você pode remover esta notificação em <a href="https://vacinei.org/alerta">https://vacinei.org/alerta</a>  <br>
        </p>
      </body>
    </html>
    """
    content = [html]
    with yagmail.SMTP(vacinei_user, vacinei_app_password) as yag:
        ret = yag.send(email, subject, content)
    return True

# Se quiser testar, só usar a linha abaixo
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos')

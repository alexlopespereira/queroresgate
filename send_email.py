import os
from time import sleep

import yagmail

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
BCC_ADDRESS = os.getenv('BCC_ADDRESS')

GMAIL_USER = 'demanda.resgate@gmail.com'


def send_email(org_dest, dest_email, nome, email, telefone, endereco, localizacao):
    subject = 'Notificação de solicitação de resgate'
    html = f"""\
    <html>
      <body>
        <p>Prezado representante do(a) {org_dest},<br>
           Informamos que a pessoa abaixo qualificada solicitou resgate por meio da nossa plataforma. 
        </p>
         <ul>
          <li>Nome: {nome}</li>
          <li>Email: {email}</li>
          <li>Telefone: {telefone}</li>
          <li>Endereço: {endereco}</li>
          <li><a href="http://maps.google.com/?q={localizacao}">Geolocalizacao</a></li>
        </ul> 
      <br>
      </body>
    </html>
    """
    content = [html]
    with yagmail.SMTP(GMAIL_USER, GMAIL_PASSWORD) as yag:
        ret = yag.send(dest_email, subject, content, bcc=BCC_ADDRESS)
    return True

# Se quiser testar, só usar a linha abaixo
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos')


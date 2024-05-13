import os
import datetime

import yagmail

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
BCC_ADDRESS = os.getenv('BCC_ADDRESS')

GMAIL_USER = 'demanda.resgate@gmail.com'


def send_email(org_dest, dest_email, nome, email, telefone, endereco, localizacao, geo_address, numpessoas, numanimais, outrapessoa=None, telefoneoutrapessoa=None, nomeoutrapessoa=None):
    subject = 'Notificação de solicitação de resgate'
    if outrapessoa:
        html = f"""\
                <html>
                  <body>
                    <p>Prezado representante do(a) {org_dest},<br>
                       Informamos que a pessoa abaixo qualificada solicitou resgate por meio da nossa <a href="https://www.queroresgate.com.br">plataforma</a>. 
                    </p>
                     <ul>
                      <li>Nome do solicitante: {nome}</li>
                      <li>Telefone do solicitante: {telefone}</li>
                      <li>Endereço informado: {endereco}</li>
                      <li>Endereço geo: {geo_address}</li>
                      <li>Data / Hora: {datetime.datetime.now()}</li>
                      <li>Nome do necessitado: {nomeoutrapessoa}</li>
                      <li>Telefone do necessitado: {telefoneoutrapessoa}</li>
                      <li>Número de pessoas: {numpessoas}</li>
                      <li>Número de animais: {numanimais}</li>
                      <li><a href="http://maps.google.com/?q={localizacao}">Geolocalizacao</a></li>
                    </ul> 
                  <br>
                  </body>
                </html>
                """
    else:
        html = f"""\
        <html>
          <body>
            <p>Prezado representante do(a) {org_dest},<br>
               Informamos que a pessoa abaixo qualificada solicitou resgate por meio da nossa <a href="https://www.queroresgate.com.br">plataforma</a>. 
            </p>
             <ul>
              <li>Nome: {nome}</li>
              <li>Email: {email}</li>
              <li>Telefone: {telefone}</li>
              <li>Endereço informado: {endereco}</li>
              <li>Endereço geo: {geo_address}</li>
              <li>Data / Hora: {datetime.datetime.now()}</li>
              <li>Número de pessoas: {numpessoas}</li>
              <li>Número de animais: {numanimais}</li>
              <li><a href="http://maps.google.com/?q={localizacao}">Geolocalizacao</a></li>
            </ul> 
          <br>
          </body>
        </html>
        """
    content = [html]
    with yagmail.SMTP(GMAIL_USER, GMAIL_PASSWORD) as yag:
        ret = yag.send(dest_email, subject, content, bcc=BCC_ADDRESS)
    return True, html

# Se quiser testar, só usar a linha abaixo
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos')
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos', 'teste_nome','teste_nome','teste_nome')


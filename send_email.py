import os
import datetime

import yagmail

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BCC_ADDRESSES = os.getenv('BCC_ADDRESSES').split(',')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_USER = 'demanda.resgate@gmail.com'

def send_email(org_dest, dest_email, data, geo_address, lat_long_from_addres, data_hora):
    subject = 'Notificação de solicitação de resgate'
    if data['resgate_pra_voce'] == 'yes':
        html = f"""\
                <html>
                  <body>
                    <p>Prezado representante do(a) {org_dest},<br>
                       Informamos que a pessoa abaixo qualificada solicitou resgate por meio da nossa <a href="https://www.queroresgate.com.br">plataforma</a>. 
                    </p>
                     <ul>
                      <li>Nome do solicitante: {data['nome']}</li>
                      <li>Telefone do solicitante: {data['telefone']}</li>
                      <li>Resgate foi pra quem solicitou: Sim</li>
                      <li>Rua: {data['rua']}</li>
                      <li>Número: {data['numero']}</li>
                      <li>Complemento: {data['complemento']}</li>
                      <li>Bairro: {data['bairro']}</li>
                      <li>Ponto de Referencia: {data['pontoreferencia']}</li>
                      <li>Cidade: {data['cidade']}</li>
                      <li>Estado: {data['estado']}</li>
                      <li>CEP: {data['cep']}</li>
                      <li>Endereço geo: {geo_address}</li>
                      <li>Data / Hora: {data_hora}</li>
                      <li>Número de pessoas: {data['numpessoas']}</li>
                      <li>Há idosos: {data['idosos']}</li>
                      <li>Há crianças: {data['criancas']}</li>
                      <li>Há pessoas com deficiência: {data['pessoacomdeficiencia']}</li>
                      <li>Número de animais: {data['numanimais']}</li>
                      <li><a href="http://maps.google.com/?q={data['latlong']}">Geolocalizacao do celular</a></li>
                      <li><a href="http://maps.google.com/?q={lat_long_from_addres}">Geolocalizacao do enedereço</a></li>
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
                      <li>Nome do solicitante: {data['nomeoutrapessoa']}</li>
                      <li>Telefone do solicitante: {data['telefoneoutrapessoa']}</li>
                      <li>Resgate foi pra quem solicitou: Não</li>
                      <li>Rua: {data['rua']}</li>
                      <li>Número: {data['numero']}</li>
                      <li>Complemento: {data['complemento']}</li>
                      <li>Bairro: {data['bairro']}</li>
                      <li>Ponto de Referencia: {data['pontoreferencia']}</li>
                      <li>Cidade: {data['cidade']}</li>
                      <li>Estado: {data['estado']}</li>
                      <li>CEP: {data['cep']}</li>
                      <li>Endereço geo: {geo_address}</li>
                      <li>Data / Hora: {data_hora}</li>
                      <li>Número de pessoas: {data['numpessoas']}</li>
                      <li>Há idosos: {data['idosos']}</li>
                      <li>Há crianças: {data['criancas']}</li>
                      <li>Há pessoas com deficiência: {data['pessoacomdeficiencia']}</li>
                      <li>Número de animais: {data['numanimais']}</li>
                      <li><a href="http://maps.google.com/?q={data['latlong']}">Geolocalizacao do celular</a></li>
                      <li><a href="http://maps.google.com/?q={lat_long_from_addres}">Geolocalizacao do enedereço</a></li>
                    </ul> 
                  <br>
                  </body>
                </html>
                """

    content = [html]
    with yagmail.SMTP(GMAIL_USER, GMAIL_PASSWORD) as yag:
        ret = yag.send(dest_email, subject, content, bcc=BCC_ADDRESSES)
    return True, html

# Se quiser testar, só usar a linha abaixo
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos')
# send_email('teste_org', 'teste_nome', 'queroresgate2024@gmail.com', 'https://estado.rs.gov.br/simbolos', 'teste_nome','teste_nome','teste_nome')


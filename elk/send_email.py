from time import sleep

import pandas as pd
import yagmail

vacinei_user = 'vacinei.org@gmail.com'
vacinei_app_password = 'mgbhbmxclumskbks'

direct_user = 'alexlopespereira@gmail.com'
direct_app_password = 'kiierelodivysfwm'


def send_email(to, nreports, type_vacina, google_maps_url):
    subject = 'Alerta de Vacina Disponível'
    html = f"""\
    <html>
      <body>
        <p>Ola {to},<br>
           Informamos que <b>{nreports}</b> usuários reportaram que hoje há doses remanescentes da vacina <b>{type_vacina}</b> na sua região de interesse aproximadamente <a href="{google_maps_url}">aqui</a>  <br>
           Recomendamos ligar no local de vacinação para validar a informação antes de comparecer. <br>
           
           Você pode remover esta notificação em <a href="https://vacinei.org/alerta">https://vacinei.org/alerta</a>  <br> 
        </p>
      </body>
    </html>
    """
    content = [html]

    with yagmail.SMTP(vacinei_user, vacinei_app_password) as yag:
        ret = yag.send(to, subject, content)

    return True


def mala_direta(skip=0):

    file = '../data/MalaDireta.xlsx'
    df_destinatarios = pd.read_excel(file, usecols=['Sexo', 'Primeiro Nome', 'Email'])

    subject = 'Ajuda com divulgação de site para ajudar na vacinação'
    for i, c in df_destinatarios.iloc[skip:,:].iterrows():
        prezado = "Prezado" if c['Sexo'] == 'H' else "Prezada"
        html = f"""\
        <html>
          <body>
            <p>{prezado} {c['Primeiro Nome']},<br>
               Meu nome é Alex Pereira, peguei seu contato com uma amiga da Camara dos Deputados. Meu contato é por um motivo nobre.
               Gostaria de pedir sua ajuda para divulgar o site que eu fiz (<a href="https://vacinei.org">https://vacinei.org</a>) para ajudar a melhorar a eficiência da vacinação (diminuir as perdas de vacina).<br>
               O funcionamento é simples. Quem se vacinou pode informar qual vacina tomou e se há doses remanescentes naquele dia, naquele local.
               Que quiser se vacinar, pode cadastrar a sua região de interesse no site pra receber notificações por e-mail da disponibilidade de vascinas remanescentes (sobras que serão perdidas se não usadas no mesmo dia).

               Consegue me ajudar (ou ajudar o Brasil, no caso) ?

               PS.: No início da pandemia, eu também desenvolvi o aplicativo Xô Corona que foi selecionado nesse (<a href="https://vacinei.org">desafio organizado pelo Ministério Público de Pernambuco</a>). O aplicativo não esta mais em funcionamento.

               Atenciosamente,
               --
               Alex Lopes Pereira
               61 99616-9186
               https://www.linkedin.com/in/alex-pereira-920b244/
            </p>
          </body>
        </html>
        """
        content = [html]

        with yagmail.SMTP(direct_user, direct_app_password) as yag:
            ret = yag.send(c['Email'], subject, content)
            print(f"Enviado para {c['Email']}")
            sleep(1)


# if __name__ == '__main__':
    # send_email('alexlopespereira@gmail.com', 10, 'pfizer', "https://www.google.com/maps/search/?api=1&query=-15.795026,-47.852150")
    # mala_direta(117)

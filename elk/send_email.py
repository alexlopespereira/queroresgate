import yagmail

def send_email(to, nreports, type_vacina, google_maps_url):
    user = 'vacinei.org@gmail.com'
    app_password = 'mgbhbmxclumskbks'
    subject = 'Alerta de Vacina Disponível'
    html = f"""\
    <html>
      <body>
        <p>Ola {to},<br>
           Informamos que <b>{nreports}</b> usuários reportaram que hoje há doses remanescentes da vacina <b>{type_vacina}</b> na sua região de interesse <a href="{google_maps_url}">aqui</a>  <br>
           Recomendamos ligar no local de vacinação para validar a informação antes de comparecer. <br>
           
           Você pode remover este alerta em <a href="https://vacinei.org/alerta">https://vacinei.org/alerta</a>  <br> 
        </p>
      </body>
    </html>
    """
    content = [html]

    with yagmail.SMTP(user, app_password) as yag:
        ret = yag.send(to, subject, content)

    return True


if __name__ == '__main__':
    send_email('alexlopespereira@gmail.com', 10, 'pfizer', "https://www.google.com/maps/search/?api=1&query=-15.795026,-47.852150")
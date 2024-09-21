from decouple import Config, RepositoryEnv
import requests

# Carregar variáveis do arquivo .env
config = Config(RepositoryEnv('.env'))


def send_email_via_mailgun():
    # Obter variáveis do .env
    api_key = config('MAILGUN_API_KEY')
    domain = config('MAILGUN_DOMAIN')
    from_email = config('MAILGUN_FROM_EMAIL')
    to_email = config('MAILGUN_TO_EMAIL')

    url = f'https://api.mailgun.net/v3/{domain}/messages'
    auth = ('api', api_key)
    data = {
        'from': from_email,
        'to': to_email,
        'subject': 'Hello from Mailgun',
        'text': 'This is a test email sent using Mailgun API.'
    }

    response = requests.post(url, auth=auth, data=data)

    if response.status_code == 200:
        print("Email sent successfully.")
    else:
        print(
            f"Failed to send email: {response.status_code} - {response.text}")


# Chame a função para enviar o e-mail
send_email_via_mailgun()

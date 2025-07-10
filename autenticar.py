import requests
import base64
import os
from dotenv import load_dotenv


def retornar_token():
    load_dotenv()
    MY_KEY = os.getenv('MY_KEY')
    url = 'https://autenticacao.sapi.serpro.gov.br/authenticate'
    myKey = MY_KEY
    key = base64.b64encode(myKey.encode()).decode()

    data = {
        'grant_type': 'client_credentials',
    }

    cert_content = os.getenv("PRIVATE_CERT_PEM")

    with open('cert.pem', 'w') as pem_file:
        pem_file.write(cert_content)

    key_content = os.getenv("PRIVATE_KEY_PEM")

    with open('key.pem', 'w') as pem_file:
        pem_file.write(key_content)

    x = requests.post(
        url,
        headers={
            'Authorization': f'Basic {key}',
            'role-type': 'TERCEIROS',
            'Content-type': 'application/x-www-form-urlencoded',
        },
        data=data,
        cert=('cert.pem', 'key.pem')
    )

    acess_token = x.json().get('access_token')
    jwt = x.json().get('jwt_token')
    if os.path.exists('cert.pem'):
        os.remove('cert.pem')
    if os.path.exists('key.pem'):
        os.remove('key.pem')
    return acess_token, jwt

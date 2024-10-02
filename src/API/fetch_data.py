import os
from json import loads
from typing import Dict
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_jwt_token():
    """_summary_

    :raises Exception: _description_
    :return: _description_
    """
    user = os.getenv('APIUSER')
    password = os.getenv('PASSWORD')

    payload = {
        'username': user,
        'password': password
    }
    response = requests.post(os.getenv('AUTH_URL'), json=payload)

    if response.status_code == 200:
        return response.json().get('access')
    else:
        raise Exception('Failed to authenticate', response.status_code, response.text)


def get_combined_viewset_from_json() -> Dict:
    """Get data from a saved json

    :return: Collected data from teachers
    """
    data = {}
    with open('Data/all_data.json', 'r', encoding='utf-8') as json_file:
        content = json_file.read()
        data = loads(content)

    return data

def get_combined_viewset(jwt_token:str) -> Dict:
    """ Recupera um viewset contendo várias informações da base de dados

    :param jwt_token: Token para autenticação JWT
    :raises Exception: Excessão personalizada para caso a requisição retorne com erro.
    :return: Um dicionário contendo os dados solicitados
    """
    api_url = 'https://web-production-9a4d.up.railway.app/api/api'
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch data', response.status_code, response.text)

def get_competences(jwt_token: str) -> Dict:
    """_summary_

    :param jwt_token: _description_
    :raises Exception: _description_
    :return: _description_
    """
    api_url = 'https://web-production-9a4d.up.railway.app/api/listar-competencias/'
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch data', response.status_code, response.text)

def get_competences_from_json() -> Dict:
    """_summary_

    :return: _description_
    """
    data = {}
    with open('Data/all_data.json', 'r', encoding='utf-8') as json_file:
        content = json_file.read()
        data = loads(content)

    return data['competencias']


# Fazer uma requisição autenticada
# combined_data = get_combined_viewset(jwt_token)
# competences = get_competences(jwt_token)
# print(competences)

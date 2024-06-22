import requests
from dotenv import load_dotenv
import requests, os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente

def get_jwt_token():
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

def get_combined_viewset(jwt_token:str) ->dict:
    """
    # Recupera um viewset contendo várias informações da base de dados

    ## Args:
        `jwt_token (str)`: Token para autenticação JWT

    ## Raises:
        `Exception`: Excessão personalizada para caso a requisição retorne com erro.
        
    ----
    ## Returns:
        `dict`: Um dicionário contendo os dados solicitados
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

def get_competences(jwt_token):
    api_url = 'https://web-production-9a4d.up.railway.app/api/listar-competencias/'
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch data', response.status_code, response.text)


# Fazer uma requisição autenticada
# combined_data = get_combined_viewset(jwt_token)
# competences = get_competences(jwt_token)
# print(competences)

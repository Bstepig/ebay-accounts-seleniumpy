import requests
from tools.config import PHONE_VERIFICATION_API_KEY, PHONE_VERIFICATION_SERVICE, PHONE_VERIFICATION_COUNTRY, PHONE_VERIFICATION_PROVIDER


def get_number():
    url = f'https://{PHONE_VERIFICATION_PROVIDER}/stubs/handler_api.php'
    params = {
        'api_key': PHONE_VERIFICATION_API_KEY,
        'action': 'getNumber',
        'service': PHONE_VERIFICATION_SERVICE,
        'country': PHONE_VERIFICATION_COUNTRY,
    }
    response = requests.get(url, params=params)
    body = response.json()

    print(body)

    return {
        'id': body['id'],
        'number': body['number'],
    }


def get_activation(id: str | int):
    url = f'https://{PHONE_VERIFICATION_PROVIDER}/stubs/handler_api.php'
    params = {
        'api_key': PHONE_VERIFICATION_API_KEY,
        'action': 'getStatus',
        'id': id,
    }
    response = requests.get(url, params=params)
    body = response.json()

    print(body)

    return {
        'status': body['status'],
        'code': body['code'],
    }

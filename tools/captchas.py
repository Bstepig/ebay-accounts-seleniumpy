import requests
from tools.config import CAPTCHA_API_KEY, RECAPTCHA_API_KEY, CAPTCHA_PROVIDER, RECAPTCHA_PROVIDER
from tools.shortcuts import wait


def solve_captcha(body: str):
    url = f'{CAPTCHA_PROVIDER}/in.php'
    data = {
        "key": CAPTCHA_API_KEY,
        "method": 'base64',
        "body": body,
        "json": 1
    }
    response = requests.post(url, data).json()

    if response['status'] == 1:
        return response['request']

    raise Exception(response)


def solve_recaptcha(sitekey: str, pageurl: str):
    url = f'{RECAPTCHA_PROVIDER}/in.php'
    data = {
        "key": RECAPTCHA_API_KEY,
        "method": 'userrecaptcha',
        "googlekey": sitekey,
        "pageurl": pageurl,
        "json": 1
    }
    response = requests.post(url, data).json()

    if response['status'] == 1:
        return response['request']

    raise Exception(response)


def get_captcha_solve(id: str):
    while True:
        url = f'{CAPTCHA_PROVIDER}/out.php'
        wait(3, 5)
        data = {
            "key": CAPTCHA_API_KEY,
            "action": 'get',
            "id": id,
            "json": 1
        }
        response = requests.get(url, params=data).json()
        if response['status'] == 1:
            return response['request']
        if response['status'] != 0:
            raise Exception(response)


def get_recaptcha_solve(id: str):
    while True:
        url = f'{RECAPTCHA_PROVIDER}/out.php'
        wait(3, 5)
        data = {
            "key": RECAPTCHA_API_KEY,
            "action": 'get',
            "id": id,
            "json": 1
        }
        response = requests.get(url, params=data).json()
        if response['status'] == 1:
            return response['request']
        if response['status'] != 0:
            raise Exception(response)

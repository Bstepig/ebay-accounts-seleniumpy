import requests
import time
from keys import CAPTCHA_API_KEY, RECAPTCHA_API_KEY


def solve_captcha(body: str):
    url = 'http://rucaptcha.com/in.php'
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
    url = 'http://rucaptcha.com/in.php'
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
        res_url = 'http://rucaptcha.com/res.php'
        time.sleep(3)
        data = {
            "key": RECAPTCHA_API_KEY,
            "action": 'get',
            "id": id,
            "json": 1
        }
        response = requests.get(res_url, params=data).json()
        if response['status'] == 1:
            return response['request']
        if response['status'] != 0:
            raise Exception(response)

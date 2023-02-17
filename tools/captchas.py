import json
import requests
from tools.config import CAPTCHA_API_KEY, RECAPTCHA_API_KEY, CAPTCHA_PROVIDER, RECAPTCHA_PROVIDER
from tools.shortcuts import wait
from twocaptcha import TwoCaptcha

config = {
            'server':           CAPTCHA_PROVIDER,
            'apiKey':           CAPTCHA_API_KEY,
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
        }
captcha_solver = TwoCaptcha(**config)

reconfig = {
            'server':           RECAPTCHA_PROVIDER,
            'apiKey':           RECAPTCHA_API_KEY,
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
        }
recaptcha_solver = TwoCaptcha(**config)


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
        url = f'{CAPTCHA_PROVIDER}/res.php'
        wait(3, 5)
        data = {
            "key": CAPTCHA_API_KEY,
            "action": 'get',
            "id": id,
            "json": 1
        }
        response = requests.get(url, params=data)
        content = response.content
        text = response.text
        try:
            json_text = response.json()
            if json_text['status'] == 1:
                return json_text['request']
            if json_text['status'] != 0:
                raise Exception(json_text)
        except json.decoder.JSONDecodeError as e:
            print(e)
        print('content', content)
        print('text', text)
        return text
        # if response['status'] == 1:
        #     return response['request']
        # if response['status'] != 0:
        #     raise Exception(response)


def get_recaptcha_solve(id: str):
    while True:
        url = f'{RECAPTCHA_PROVIDER}/res.php'
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

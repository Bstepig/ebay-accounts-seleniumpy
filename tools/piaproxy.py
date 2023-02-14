import requests
from tools.config import PIAPROXY_IP, PIAPROXY_PORT, PIAPROXY_COUNTRY


def load_pia_proxy(port):
    url = f'http://{PIAPROXY_IP}:{PIAPROXY_PORT}/api/get_ip_list'
    params = {
        'num': 1,
        't': 2,
        'country': PIAPROXY_COUNTRY,
        'ip_time': 1,
        'port': port,
    }
    response = requests.get(url, params)
    status = response.status_code
    body = response.json()

    if status != 200:
       raise Exception(f'Problem with piaproxy: {body["msg"]}. {status} {body}')

    if body['code'] == -1:
       raise Exception(f'Problem with piaproxy: {body["msg"]}')

    data = body['data'][0]

    zip = data['zip']
    city = data['city'].capitalize()
    state = data['state'].capitalize()
    out_ip = data['out_ip']
    ip = data['ip']
    proxy = f'{ip}:{port}'

    return {
        'zip': zip,
        'city': city,
        'state': state,
        'out_ip': out_ip,
        'ip': ip,
        'port': port,
        'proxy': proxy,
    }

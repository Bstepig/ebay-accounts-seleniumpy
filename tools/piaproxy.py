import requests

piaproxy_ip = 'localhost'
piaproxy_port = '50101'
piaproxy_country = 'DE'



def load_pia_proxy(port):
    url = f'http://{piaproxy_ip}:{piaproxy_port}/api/get_ip_list'
    params = {
        'num': 1,
        't': 2,
        'country': piaproxy_country,
        'ip_time': 1,
        'port': port,
    }
    response = requests.get(url, params)
    status = response.status_code
    body = response.json()

    if status != 200:
       raise Exception(f'Problem with piaproxy: {body["msg"]}. {status} {body}')

    if body['code'] == -1:
       print(body['msg'])
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

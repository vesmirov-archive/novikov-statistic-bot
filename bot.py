import os

import requests
from dotenv import load_dotenv

DDU_PREFIX = 'ddu'
ZALIV_PREFIX = 'zal'
REG_PREFIX = 'reg'

load_dotenv()

API_URL = 'https://cloud.roistat.com/api/v1/{}?'
API_KEY = os.getenv('API_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')

KEY_ARG = f'key={API_KEY}'
PROJECT_ARG = f'project={PROJECT_ID}'


headers = {'content-type': 'application/json'}
payload = {
    "dimensions": ["landing_page"],
    "metrics": ["marketing_cost"],
    "period": {
        "from": "2021-05-19T00:00:00+0300",
        "to": "2021-05-19T23:59:59+0300"
    }
}
url = API_URL.format(f'project/analytics/data') + KEY_ARG + '&' + PROJECT_ARG

response = requests.post(url, json=payload, headers=headers).json()

landing_pages = {'ddu': {}, 'zaliv': {}, 'reg': {}, 'other': {}}
for item in response['data'][0]['items']:
    name = item['dimensions']['landing_page']['title']
    value = item['metrics'][0]['value']
    if name[0:3] == DDU_PREFIX:
        landing_pages['ddu'].update({name: value})
    elif name[0:3] == ZALIV_PREFIX:
        landing_pages['zaliv'].update({name: value})
    elif name[0:3] == REG_PREFIX:
        landing_pages['reg'].update({name: value})
    else:
        landing_pages['other'].update({name: value})

print(landing_pages)

{
    "ddu": {
        "ddu.novikov-pravo.ru": 466.62,
        "ddu.novikov-pravo.ru/calc": 2178.168,
        "ddu.novikov-pravo.ru/priemka": 36.168,
    },
    "zaliv": {
        "zaliv.novikov-pravo.ru/ocenka": 4694.388,
        "zaliv.novikov-pravo.ru": 1862.424,
        "zaliv.novikov-pravo.ru/ocenka_usherba2/v3.php": 1334.1456,
        "zaliv.novikov-pravo.ru/ekspertiza": 5511.12,
        "zaliv.grafo77.ru": 186.876,
    },
    "reg": {},
    "other": {
        "Неизвестное значение": 0,
        "novikov-pravo.ru": 0,
        "mrqz.me/609684d03dcafd003eb3319c": 1447.62,
    },
}


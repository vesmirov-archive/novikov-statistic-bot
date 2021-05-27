import requests

DDU_PREFIX = 'ddu'
PRIEMKA_ENDING = 'priemka'
ZALIV_PREFIX = 'zal'
REG_PREFIX = 'reg'


API_URL = 'https://cloud.roistat.com/api/v1/{}?'


def get_landing_values(key, project, day):
    landing_pages = {
        'ddu': {},
        'priemka': {},
        'zaliv': {},
        'reg': {},
        'other': {}
    }

    headers = {'content-type': 'application/json'}
    url = (
        API_URL.format('project/analytics/data')
        + f'key={key}' + '&' + f'project={project}'
    )
    payload = {
        'dimensions': ['landing_page'],
        'metrics': ['marketing_cost'],
        'period': {
            'from': f'{day}T00:00:00+0300',
            'to': f'{day}T23:59:59+0300',
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return landing_pages

    data = response.json()
    for item in data['data'][0]['items']:
        name = item['dimensions']['landing_page']['title']
        value = item['metrics'][0]['value']
        if name[0:3] == DDU_PREFIX:
            if name[-7:] == PRIEMKA_ENDING:
                landing_pages['priemka'].update({name: value})
            else:
                landing_pages['ddu'].update({name: value})
        elif name[0:3] == ZALIV_PREFIX:
            landing_pages['zaliv'].update({name: value})
        elif name[0:3] == REG_PREFIX:
            landing_pages['reg'].update({name: value})
        else:
            landing_pages['other'].update({name: value})
    return landing_pages


def get_category_values(key, project, day):
    categories = {}

    landing_pages = get_landing_values(key, project, day)
    for category, landings in landing_pages.items():
        categories[category] = sum(landings.values())
    return categories

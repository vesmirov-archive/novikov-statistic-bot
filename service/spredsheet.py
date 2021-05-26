import time

import pygsheets

START_DATE = 16075

ROW_SHIFT = 2

CATEGORIES_WRITE = {
    'zaliv': 'E',
    'ddu': 'F',
    'priemka': 'G',
    'reg': 'H',
}

CATEGORIES_READ = {
    'zaliv': {
        'Расходы': 'E',
        'Договоров': 'K',
        'Заявок': 'Q',
        'Стоимость заявки': 'W',
        'Стоимость сделки': 'AC',
        'КЭВ': 'AI',
    },
    'ddu': {
        'Расходы': 'F',
        'Договоров': 'L',
        'Заявок': 'R',
        'Стоимость заявки': 'X',
        'Стоимость сделки': 'AD',
        'КЭВ': 'AJ',
    },
    'priemka': {
        'Расходы': 'G',
        'Договоров': 'M',
        'Заявок': 'S',
        'Стоимость заявки': 'Y',
        'Стоимость сделки': 'AE',
        'КЭВ': 'AK',
    },
    'reg': {
        'Расходы': 'H',
        'Договоров': 'N',
        'Заявок': 'T',
        'Стоимость заявки': 'Z',
        'Стоимость сделки': 'AF',
        'КЭВ': 'AL',
    },
    'average': {
        'Всего расходов': 'AO',
        'Всего договоров': 'AP',
        'Всего заявок': 'AQ',
    }
}


def write_data_to_google_sheet(manager, sheet_key, page_id, data):
    sheet = manager.open_by_key(sheet_key)
    page = sheet.worksheet('id', page_id)
    row = str(int(time.time()) // 100000 - START_DATE + ROW_SHIFT)

    for name, value in data.items():
        if name in CATEGORIES_WRITE:
            cell = CATEGORIES_WRITE[name] + row
            page.update_value(cell, value)


def get_data_from_google_sheet(manager, sheet_key, page_id):
    sheet = manager.open_by_key(sheet_key)
    page = sheet.worksheet('id', page_id)
    row = str(int(time.time()) // 100000 - START_DATE + ROW_SHIFT)

    data = {}
    for category in CATEGORIES_READ:
        data[category] = {}
        for value in CATEGORIES_READ[category]:
            cell = CATEGORIES_READ[category][value] + row
            content = page.get_value(cell)
            data[category].update({value: content})
    return data
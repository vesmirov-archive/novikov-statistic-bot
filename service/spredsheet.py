import time

import pygsheets

START_DATE = 16074

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
        'Стоимость заявки': 'AC',
        'Стоимость сделки': 'AI',
        'Оценок': 'W',
        'КЭВ': 'AO',
    },
    'ddu': {
        'Расходы': 'F',
        'Договоров': 'L',
        'Заявок': 'R',
        'Стоимость заявки': 'AD',
        'Стоимость сделки': 'AJ',
        'Получено ИНН': 'X',
        'КЭВ': 'AP',
    },
    'priemka': {
        'Расходы': 'G',
        'Договоров': 'M',
        'Заявок': 'S',
        'Стоимость заявки': 'AE',
        'Стоимость сделки': 'AK',
        'Направлений на осмотр': 'Y',
        'КЭВ': 'AQ',
    },
    'reg': {
        'Расходы': 'H',
        'Договоров': 'N',
        'Заявок': 'T',
        'Стоимость заявки': 'AF',
        'Стоимость сделки': 'AL',
        'Встреч': 'Z',
        'КЭВ': 'AR',
    },
    'average': {
        'Всего расходов': 'AU',
        'Всего договоров': 'AV',
        'Всего заявок': 'AW',
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

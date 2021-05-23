import time

import pygsheets

START_DATE = 16217
ROW_SHIFT = 2

CATEGORIES = {
    'zaliv': 'E',
    'ddu': 'F',
    'priemka': 'G',
    'reg': 'H'
}


def write_data_to_google_sheet(manager, sheet_key, page_id, data):
    sheet = manager.open_by_key(sheet_key)
    page = sheet.worksheet('id', page_id)
    row = str(int(time.time()) // 100000 - START_DATE + ROW_SHIFT)

    for name, value in data.items():
        if name in CATEGORIES:
            cell = CATEGORIES[name] + row
            page.update_value(cell, value)

import datetime

import pygsheets
from dotenv import dotenv_values

from service.landings import get_category_values
from service.spredsheet import write_data_to_google_sheet

env = dotenv_values('.env')

# roistat
API_KEY = env.get('API_KEY')
PROJECT = env.get('PROJECT_ID')

# google
SHEET_KEY = env.get('SHEET_KEY')
WORKSHEET_ID = env.get('WORKSHEET_ID')
SERVICE_FILE = env.get('SERVICE_FILE')


def main():
    today = datetime.date.today()
    data = get_category_values(API_KEY, PROJECT, today)

    manager = pygsheets.authorize(service_file=SERVICE_FILE)
    write_data_to_google_sheet(manager, SHEET_KEY, WORKSHEET_ID, data)


if __name__ == '__main__':
    main()

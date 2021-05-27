import datetime

import telebot
import pygsheets
from dotenv import dotenv_values

from service import db
from service.spredsheet import get_data_from_google_sheet

env = dotenv_values('.env')

# roistat
API_KEY = env.get('API_KEY')
PROJECT = env.get('PROJECT_ID')

# telegram
TOKEN = env.get('TELEGRAM_TOKEN')
CHAT = env.get('TELEGRAM_CHAT_ID')

# google
SHEET_KEY = env.get('SHEET_KEY')
WORKSHEET_ID = env.get('WORKSHEET_ID')
SERVICE_FILE = env.get('SERVICE_FILE')

# users
USER_1=env.get('TELEGRAM_TO_1')

def main():
    connect, cursor = db.connect_database(env)

    bot = telebot.TeleBot(TOKEN)
    manager = pygsheets.authorize(service_file=SERVICE_FILE)

    result = ['Daily statistic']
    data = get_data_from_google_sheet(manager, SHEET_KEY, WORKSHEET_ID)
    for category, values in data.items():
        result.append(f'{category.upper()}:')
        result.extend([f'{name} - {val}' for name, val in values.items()])
        result.append('')
    
    cursor.execute("SELECT user_id, is_admin FROM users")
    users = cursor.fetchall()

    for user in users:
        if user[1]:
            bot.send_message(
                user[0],'\n'.join(result)
            )

    connect.close()


if __name__ == '__main__':
    main()

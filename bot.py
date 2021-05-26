
import datetime

import telebot
import pygsheets
from dotenv import dotenv_values

from service.landings import get_landing_values, get_category_values
from service.spredsheet import (
    write_data_to_google_sheet,
    get_data_from_google_sheet,
)

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

# messages
START = (
    "Hi {}! I'm a Novikov LC bot.\n"
    "I can send, store and process statistic data from \n"
    "https://roistat.com/\n"
    "and send you daily results, if you on my list.\n"
    "For any questions you can contact with "
    "@vilagov or @karlos979."
    )
HELP = (
    'Commands:\n'
    '/yesterday - get spendings for yesterday\n'
    '/statistic - get statistic for yesterday\n'
    '/update - update values if were not updated'
)


bot = telebot.TeleBot(TOKEN)
manager = pygsheets.authorize(service_file=SERVICE_FILE)


markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = telebot.types.KeyboardButton('/statistic')
itembtn2 = telebot.types.KeyboardButton('/yesterday')
itembtn3 = telebot.types.KeyboardButton('/today')
itembtn4 = telebot.types.InlineKeyboardButton('/help', url='help')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Say hi to user"""

    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, START.format(name), reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help_text(message):
    """Send help text with command list"""

    bot.send_message(message.from_user.id, HELP)


@bot.message_handler(commands=['yesterday'])
def send_spendings_for_yesterday(message):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    lands = get_landing_values(API_KEY, PROJECT, yesterday)
    result = ['Roistat spendings for yesterday']
    for name, values in lands.items():
        result.append(f'{name.upper()}:')
        result.extend([f'{round(p)} - {l}' for l, p in values.items()])
        result.append('')
    
    bot.send_message(
        message.from_user.id,
        '\n'.join(result),
        disable_web_page_preview=True
    )


@bot.message_handler(commands=['today'])
def send_spendings_for_today(message):
    today = datetime.date.today()
    lands = get_landing_values(API_KEY, PROJECT, today)
    result = ['Roistat spendings for today']
    for name, values in lands.items():
        result.append(f'{name.upper()}:')
        result.extend([f'{round(p)} - {l}' for l, p in values.items()])
        result.append('')
    
    bot.send_message(
        message.from_user.id,
        '\n'.join(result),
        disable_web_page_preview=True
    )


@bot.message_handler(commands=['statistic'])
def send_statistic(message):
    result = ['Novikov LC statistic']
    data = get_data_from_google_sheet(manager, SHEET_KEY, WORKSHEET_ID)
    for category, values in data.items():
        result.append(f'{category.upper()}:')
        result.extend([f'{name} - {val}' for name, val in values.items()])
        result.append('')
    bot.send_message(message.from_user.id,'\n'.join(result))


bot.polling()

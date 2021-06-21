"""
    Bot's module with specified commands
"""

import datetime

from dotenv import dotenv_values
import pygsheets
import telebot

from service import db
from service.landings import get_landing_values, get_category_values
from service.spredsheet import (
    get_data_from_google_sheet,
    write_data_to_google_sheet
)

env = dotenv_values('.env')

# roistat
API_KEY = env.get('API_KEY')
PROJECT = env.get('PROJECT_ID')

# telegram
TOKEN = env.get('TELEGRAM_STATISTIC_TOKEN')
CHAT = env.get('TELEGRAM_CHAT_ID')

# google
SHEET_KEY = env.get('SHEET_KEY')
WORKSHEET_ID = env.get('WORKSHEET_STATISTIC_ID')
CLIENT_SECRET_FILE = env.get('CLIENT_SECRET_FILE')

# messages
START = (
    'Привет {}! Я бот юридического центра Новиков.\n'
    'Я могу отправлять, фиксировать и просчитывать '
    'данные из https://roistat.com/ '
    'и отправлять ежедневную статистику в чат.\n'
    'По любым вопросам можно обратиться к '
    '@vilagov или @karlos979.'
)
START_ANONIMUS = (
    'У вас нет прав для использования данного бота.\n'
    'Обратитесь к @vilagov или @karlos979, если уверены '
    'что вам нужен доступ.'
)
HELP = (
    'Команды:\n'
    '/today - отобразить расходы за сегодняшний день\n'
    '/yesterday - отобразить расходы за вчерашний день\n'
    '/statistic - собрать статистику за сегодня\n'
    '/update - обновить данные за сегодняшний день\n'
    '/users - отобразить список пользователей\n'
    '/adduser - добавить пользователя'
)


bot = telebot.TeleBot(TOKEN)
manager = pygsheets.authorize(service_account_file=CLIENT_SECRET_FILE)
connect, cursor = db.connect_database(env)

markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
itembtn1 = telebot.types.KeyboardButton('/statistic')
itembtn2 = telebot.types.KeyboardButton('/today')
itembtn3 = telebot.types.KeyboardButton('/yesterday')
itembtn4 = telebot.types.InlineKeyboardButton('/help')
itembtn5 = telebot.types.InlineKeyboardButton('/users')
itembtn6 = telebot.types.InlineKeyboardButton('/adduser')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)


def permission_check(func):
    """
        User permission check decorator.
        If user id not in database, send 'deny access' message.
    """

    def inner(message):
        if db.user_has_permissions(cursor, message.from_user.id):
            func(message)
        else:
            bot.send_message(message.from_user.id, START_ANONIMUS)
    return inner


@bot.message_handler(commands=['start'])
@permission_check
def greet_user(message):
    """Greet user"""

    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, START.format(name), reply_markup=markup)


@bot.message_handler(commands=['help'])
@permission_check
def send_help_text(message):
    """Send help-text to user"""

    bot.send_message(message.from_user.id, HELP)


@bot.message_handler(commands=['yesterday'])
@permission_check
def send_spendings_for_yesterday(message):
    """Show spendings in roistat for yesterday"""

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    lands = get_landing_values(API_KEY, PROJECT, yesterday)
    result = ['Расходы на рекламу за вчера']
    for name, values in lands.items():
        result.append(f'{name.upper()}:')
        result.extend([f'{round(pr)} - {land}' for land, pr in values.items()])
        result.append('')

    bot.send_message(
        message.from_user.id,
        '\n'.join(result),
        disable_web_page_preview=True
    )


@bot.message_handler(commands=['today'])
@permission_check
def send_spendings_for_today(message):
    """Show spendings in roistat for today"""

    today = datetime.date.today()
    lands = get_landing_values(API_KEY, PROJECT, today)
    result = ['Расходы на рекламу за сегодня']
    for name, values in lands.items():
        result.append(f'{name.upper()}:')
        result.extend([f'{round(pr)} - {land}' for land, pr in values.items()])
        result.append('')

    bot.send_message(
        message.from_user.id,
        '\n'.join(result),
        disable_web_page_preview=True
    )


@bot.message_handler(commands=['statistic'])
@permission_check
def send_statistic(message):
    """Show all statistic for today"""

    result = ['Статистика за сегодня']
    data = get_data_from_google_sheet(manager, SHEET_KEY, WORKSHEET_ID)
    for category, values in data.items():
        result.append(f'{category.upper()}:')
        result.extend([f'{name} - {val}' for name, val in values.items()])
        result.append('')
    bot.send_message(message.from_user.id, '\n'.join(result))


@bot.message_handler(commands=['update'])
@permission_check
def update_data(message):
    """Update data manualy in google worksheet"""

    today = datetime.date.today()
    data = get_category_values(API_KEY, PROJECT, today)
    write_data_to_google_sheet(manager, SHEET_KEY, WORKSHEET_ID, data)

    bot.send_message(
        message.from_user.id,
        'Данные в таблице заменены на актуальные'
    )


@bot.message_handler(commands=['users'])
@permission_check
def send_list_users(message):
    """Show all added users to this bot"""

    users = db.list_users(cursor)
    bot.send_message(message.from_user.id, users)


@bot.message_handler(commands=['adduser'])
@permission_check
def start_adding_user(message):
    """Add user to this bot"""

    message = bot.send_message(
        message.from_user.id,
        'Отправьте данные добавляемого пользователя в следующем формате:\n'
        '<ID_пользователя> <имя_пользователя> <админ_доступ_(да/нет)>\n\n'
        'Пример:\n'
        '123456789 vilagov да'
    )
    bot.register_next_step_handler(message, adding_user)


def adding_user(message):
    """User adding process"""

    data = message.text.split()

    if len(data) == 3:
        try:
            user_id = int(data[0])
            username = data[1]
            is_admin = True if data[2] == 'да' else False
        except ValueError:
            bot.send_message(
                message.from_user.id, 'Отправленный формат неверен.')
        finally:
            db.add_user(cursor, connect, user_id, username, is_admin)
            bot.send_message(
                message.from_user.id,
                f'Пользователь "{username}" добавлен.'
            )
    else:
        bot.send_message(message.from_user.id, 'Отправленный формат неверен.')


try:
  bot.polling()
except Exception as e:
  print(e)

connect.close()

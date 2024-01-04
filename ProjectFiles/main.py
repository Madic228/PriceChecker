import requests
import telebot
from telebot import types

from ProjectFiles.db.DataBaseHelper import DataBaseHelper


bot = telebot.TeleBot("6798262829:AAGlgaecBZRfuJOTckQhbfbZzRFi1KxB8_Y")

@bot.message_handler(commands=['start'])
def start(message): 
    DataBaseHelper.create_tables()
    username = message.from_user.username  # Получение имени пользователя
    if not DataBaseHelper.user_exists(username):  # Проверка на существование пользователя
        DataBaseHelper.add_user(username)  # Добавление пользователя в базу данных

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Список товаров')
    btn2 = types.KeyboardButton('Добавить товары')
    btn3 = types.KeyboardButton('Удалить все товары')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,f'Приветствуем {message.from_user.first_name}! Выберите действие:', reply_markup=markup)
    main_menu(message)


def main_menu(message):

    bot.register_next_step_handler(message, on_click)
    return


def on_click(message):
    if message.text == 'Список товаров':
        good_list(message)

    elif message.text == 'Добавить товары':
        add_good(message)

    elif message.text == 'Удалить все товары':
        delete_all(message)

    else:
        bot.send_message(message.chat.id, 'Команда, введите команду.')
        main_menu(message)
    return

def delete_all(message):
    username = message.from_user.username
    # DataBaseHelper.delete_all(username)
    bot.send_message(message.chat.id, 'Все ваши товары сняты с отлеживания')
    main_menu(message)
    return

def good_list(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('товар1', callback_data='keybut')
    btn2 = types.InlineKeyboardButton('товар2', callback_data='keybut')
    btn3 = types.InlineKeyboardButton('товар3', callback_data='keybut')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,'ваши товары:', reply_markup=markup)
    main_menu(message)
    return

def add_good(message):
    bot.send_message(message.chat.id, 'Введите ссылку на товар:')
    bot.register_next_step_handler(message, url_check)
    return

def url_check(message):
    try:
        url = message.text.strip()
        if requests.get(url).status_code == 200:
            bot.send_message(message.chat.id, f'{url}')
            main_menu(message)
            return
    except Exception:
        bot.send_message(message.chat.id, "что-то не так")
        bot.send_message(message.chat.id, "Вы в главном меню")
        main_menu(message)
        return

@bot.message_handler()
def free_text(message):
    bot.send_message(message.chat.id, 'ft')
    on_click(message)
    return

bot.infinity_polling()
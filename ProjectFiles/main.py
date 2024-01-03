import telebot
from telebot import types
import DataBaseHelper

bot = telebot.TeleBot("6798262829:AAGlgaecBZRfuJOTckQhbfbZzRFi1KxB8_Y")

@bot.message_handler(commands=['start'])
def start(message):
    DataBaseHelper.create_tables()
    DataBaseHelper.add_user(message.from_user.username)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Список товаров', callback_data='good_list')
    btn2 = types.InlineKeyboardButton('Добавить товары', callback_data='add_good')
    btn3 = types.InlineKeyboardButton('Удалить все товары', callback_data='delete_all')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     f'Приветствуем {message.from_user.first_name}, выберите действие:',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'good_list':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,'вот список всех ваших товаров:')
    if callback.data == 'add_good':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Введите URI товара на sbermegamarket:')
    if callback.data == 'delete_all':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Все товары удалены:')

@bot.message_handler(commands=['goodlist'])
def start(message):
    class XClass(object):
        def __init__(self):
            self.message = message
            self.data = 'good_list'

    callback_message(XClass())

@bot.message_handler(commands=['addgood'])
def start(message):
    class XClass(object):
        def __init__(self):
            self.message = message
            self.data = 'add_good'
    callback_message(XClass())

@bot.message_handler(commands=['deleteall'])
def start(message):
    class XClass(object):
        def __init__(self):
            self.message = message
            self.data = 'delete_all'

    callback_message(XClass())

@bot.message_handler()
def free_text(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Список товаров', callback_data='good_list')
    btn2 = types.InlineKeyboardButton('Добавить товары', callback_data='add_good')
    btn3 = types.InlineKeyboardButton('Удалить все товары', callback_data='delete_all')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     'Выберите команду:',
                     reply_markup=markup)


bot.infinity_polling()
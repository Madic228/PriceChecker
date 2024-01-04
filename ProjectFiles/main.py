import re
from datetime import datetime

import requests
import telebot
from telebot import types

from ProjectFiles.db.DataBaseHelper import DataBaseHelper
from ProjectFiles.PriceParser.parser_detail import MegaMarketSeleniumParser


bot = telebot.TeleBot("6798262829:AAGlgaecBZRfuJOTckQhbfbZzRFi1KxB8_Y")
urls_to_track = {}


@bot.message_handler(commands=['start'])
def start(message): 
    DataBaseHelper.create_tables()
    telegram_id = message.from_user.id
    if not DataBaseHelper.user_exists(telegram_id):
        DataBaseHelper.add_user(telegram_id, message.from_user.username)

    # Добавление пользователя в базу данных

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
    telegram_id = message.from_user.id
    DataBaseHelper.delete_tracked_products(telegram_id)
    bot.send_message(message.chat.id, 'Все ваши товары сняты с отслеживания')
    main_menu(message)


def good_list(message):
    telegram_id = message.from_user.id
    tracked_products = DataBaseHelper.get_tracked_products(telegram_id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    for product in tracked_products:
        button_text = product['name']
        callback_data = f"product_{product['product_id']}"
        btn = types.InlineKeyboardButton(button_text, callback_data=callback_data)
        markup.add(btn)
    bot.send_message(message.chat.id, 'Ваши отслеживаемые товары:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def show_product_details(call):
    product_id = call.data.split("_")[1]
    product_info = DataBaseHelper.get_product_info(product_id)
    if product_info:
        # Форматируем и отправляем сообщение с информацией о товаре
        message_text = f"{product_info['name']}\nЦена: {product_info['price']}\nURL: {product_info['url']}"
        bot.send_photo(call.message.chat.id, product_info['image_url'], caption=message_text)
    else:
        bot.send_message(call.message.chat.id, "Информация о товаре не найдена.")
    main_menu(call.message)


def add_good(message):
    user_id = message.from_user.id
    urls_to_track[user_id] = []  # Инициализация списка URL для данного пользователя
    bot.send_message(message.chat.id, 'Введите ссылку на товар или напишите "Готово", чтобы завершить:')
    bot.register_next_step_handler(message, process_url_input)


def process_url_input(message):
    user_id = message.from_user.id
    if message.text.lower() == 'готово':
        confirm_urls(message)
    elif re.match(r'https://megamarket.ru/catalog/details/', message.text.strip()):
        urls_to_track[user_id].append(message.text.strip())
        bot.send_message(message.chat.id, 'URL добавлен. Введите следующий URL или напишите "Готово", чтобы завершить.')
        bot.register_next_step_handler(message, process_url_input)
    else:
        bot.send_message(message.chat.id, "URL должен начинаться с 'https://megamarket.ru/catalog/details/'")
        bot.register_next_step_handler(message, process_url_input)

def confirm_urls(message):
    markup = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Принять список товаров", callback_data="confirm")
    markup.add(confirm_button)
    bot.send_message(message.chat.id, "Нажмите кнопку для подтверждения списка товаров", reply_markup=markup)


#
def url_check(message):
    url = message.text.strip()
    if re.match(r'https://megamarket.ru/catalog/details/', url):
        parser = MegaMarketSeleniumParser()
        product_info = parser.parse_product(url)
        if product_info:
            parser.save_to_db(product_info, url)
            bot.send_message(message.chat.id, "Товар успешно добавлен для отслеживания")
        else:
            bot.send_message(message.chat.id, "Не удалось получить информацию о товаре")
        parser.close_browser()
    else:
        bot.send_message(message.chat.id, "URL должен начинаться с 'https://megamarket.ru/catalog/details/'")
    main_menu(message)

@bot.callback_query_handler(func=lambda call: call.data == "confirm")
def handle_confirm(call):
    parser = MegaMarketSeleniumParser()
    telegram_id = call.from_user.id
    urls = urls_to_track.pop(telegram_id, []) # Получение и удаление списка URL для данного пользователя

    for url in urls:  # Используйте urls здесь
        product_info = MegaMarketSeleniumParser().parse_product(url)
        if product_info:
            # Сохраняем информацию о товаре в базу данных
            parser.save_to_db(product_info, url)
            # Добавляем товар в список отслеживаемых
            product_id = DataBaseHelper.get_product_id(url)
            DataBaseHelper.track_product(telegram_id, product_id, datetime.now().date())
            bot.send_message(call.message.chat.id, f"Товар '{product_info['title']}' добавлен для отслеживания.")
        else:
            bot.send_message(call.message.chat.id, f"Не удалось получить информацию о товаре по URL: {url}")

    parser.close_browser()
    bot.send_message(call.message.chat.id, "Все товары обработаны и добавлены для отслеживания.")
    main_menu(call.message)




@bot.message_handler()
def free_text(message):
    bot.send_message(message.chat.id, 'ft')
    on_click(message)
    return

bot.infinity_polling()
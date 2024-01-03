import telebot
from telebot import types

bot = telebot.TeleBot("6798262829:AAGlgaecBZRfuJOTckQhbfbZzRFi1KxB8_Y")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "start")

@bot.message_handler(commands=['goodlist'])
def start(message):
    bot.send_message(message.chat.id, "goodlist")

@bot.message_handler(commands=['addgood'])
def start(message):
    bot.send_message(message.chat.id, "addgood")

@bot.message_handler(commands=['deletegood'])
def start(message):
    bot.send_message(message.chat.id, "deletegood")

@bot.message_handler(commands=['deleteall'])
def start(message):
    bot.send_message(message.chat.id, "deleteall")

@bot.message_handler()
def free_text(message):
    bot.send_message(message.chat.id, 'выберите команду')



bot.infinity_polling()
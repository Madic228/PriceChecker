import telebot
from telebot import types

bot = telebot.TeleBot("6798262829:AAGlgaecBZRfuJOTckQhbfbZzRFi1KxB8_Y")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat_id, "Привет")
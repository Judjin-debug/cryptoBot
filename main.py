import telebot.types
import requests
import json

from extensions import APIException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Enter command to the bot in the next format: \n<currency name> ' \
           '<which currency to convert to> ' \
           '<quantity of initial currency>\n' \
           'See the list of available currencies: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def handle_start_help(message: telebot.types.Message):
    text = ['Available currencies:']
    for key in keys:
        text.append(key)
    text = '\n'.join(text)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise APIException('Wrong number of parameters')
    except APIException as ce:
        bot.send_message(message.chat.id, getattr(ce, 'message', repr(ce)))
    else:
        try:
            quote, base, amount = CryptoConverter.convert(*values)
        except APIException as ce:
            bot.send_message(message.chat.id, getattr(ce, 'message', repr(ce)))
        else:
            try:
                r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}")
            except Exception(f"API fetch error from: https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}") as e:
                bot.send_message(message.chat.id, getattr(e, 'message', repr(e)))
            else:
                total_base = str(round(float(json.loads(r.content)[keys[base]]) * float(amount), 4))
                text = f"Price of {amount} {quote} in {base} is {total_base}"
                bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

import telebot

TOKEN = '5987705344:AAHz7m_HvFKv-72qDdXe-eZ8ogIFMc_uhy4'

from config import TOKEN, values, main_menu, help
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['menu'])
def main_menuu(message):
    bot.send_message(message.chat.id, main_menu)

@bot.message_handler(commands=['start'])
def startt(message):
    bot.send_message(message.chat.id, help + ' /menu')

@bot.message_handler(commands=['help'])
def helpp(message):
    bot.send_message(message.chat.id, help + ' /menu')

@bot.message_handler(commands=['values'])
def valuess(message):
    bot.send_message(message.chat.id, 'Валюты на выбор:')
    for i in values:
        bot.send_message(message.chat.id, i + ' ' + values[i] )
    bot.send_message(message.chat.id, '/menu')

@bot.message_handler(content_types=['text'])
def convert_result(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = val
        result = CryptoConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка со стороны пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f'{amount} {values[base]}({base}) в {values[quote]}({quote}) равно: {result}'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "/menu")

bot.polling()

values = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR'
}

main_menu = '''Команды Бота:
>>> /menu - Главное меню:
>>> /help - Помощь
>>> /values - Валюты на выбор'''

help = '''Вод данных производите в следующем формате:
<валюта которую конвертируем>пробел
<валюьа В которую конвертируем>пробел
<сумма конвертации>
'''
import requests
import json
from config import values


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'валюты совпадают, выберите разные: {base}-{quote}')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'Не удалось конвертировать {base}')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'Не удалось конвертировать {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось конвертировать {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        result = json.loads(r.content)[values[quote]]
        result *= amount

        return result
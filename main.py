import telebot
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

bot = telebot.TeleBot('6010273731:AAE9DkCdpt0SFC8xa79_R-rn1b4TTkXLke4');

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.message_handler(content_types=['text'])

    if message.text == '/help':
        with open('help_text.txt') as help_file:
            bot.send_message(message.from_user.id, help_file.read())

    else:
        try:
            symbol = message.text
            price = crypt(symbol)
            bot.send_message(message.from_user.id,f"Цена {symbol} в USD: {price}.")
            return symbol
        except:
            bot.send_message(message.from_user.id, "ошибка")


def crypt(symbol):
    url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
    parameters = {
        "amount": "1",
        'symbol':symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '1a4c7bb4-5a4b-453a-84a6-acc1f5c926c1',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url,params=parameters )
        data = json.loads(response.text)
        price = data['data'][0]['quote']['USD']['price']
        float(price)
        price = round(price, 2)
        return price

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


bot.polling(none_stop=True, interval=0)
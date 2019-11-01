import telebot
import requests
from bs4 import BeautifulSoup as bs
import lxml
from telebot import types

TOKEN = '1033546243:AAHEv2D1Ph-_CLFiin8dDau6r8umXft1GOk'
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.9 Safari/537.36'
           }
BASE_URL = 'https://minfin.com.ua/currency/'


def get_url():
    val = {}
    session = requests.Session()
    request = session.get(BASE_URL, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        tbody = soup.find('div', attrs={'class': 'mfm-tab-menu'}).find_all('a')
        for i in tbody[1:4]:
            val[i.text] = i['href']
        return val
    return 'ERROR'


def get_exchange(str):
    exchanger = {'bank': {}, 'market': {}}
    base_url = f'https://minfin.com.ua{get_url()[str]}'
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        span = soup.find_all('span', attrs={'class': 'mfm-posr'})
        exchanger['bank']['buy'] = span[0].text[:7]
        exchanger['bank']['cell'] = span[1].text[:7]
        exchanger['market']['buy'] = span[2].text[:7]
        exchanger['market']['cell'] = span[3].text[:7]
    return exchanger


bot = telebot.TeleBot(TOKEN)


def keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('$')
    itembtn2 = types.KeyboardButton('€')
    itembtn3 = types.KeyboardButton('RUB')
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Привет!!! Это простой инфо_бот,который всегда подскажет курс валют на даный момент)). Для начала нажми кнопку со значком интересуущей валюты",
        reply_markup=keyboard()
        )


@bot.message_handler(content_types=['text'])
def send_result(message):
    chat_id = message.chat.id
    if message.text == '$':
        dic = get_exchange("ДОЛЛАР")
        text = (
            f"На даный момент курс доллара: \n\t Нацбанк \n {(dic['bank']['buy'])}   куп \n {dic['bank']['cell']}   прод \n\t Черный рынок \n {dic['market']['buy']}   куп \n {dic['market']['cell']}   прод")
        bot.send_message(chat_id, text,)
    elif message.text == '€':
        dic = get_exchange("ЕВРО")
        text = (
            f"На даный момент курс евро: \n\t Нацбанк \n {(dic['bank']['buy'])}   куп \n {dic['bank']['cell']}   прод \n\t Черный рынок \n {dic['market']['buy']}   куп \n {dic['market']['cell']}   прод")
        bot.send_message(chat_id, text,)
    elif message.text == 'RUB':
        dic = get_exchange("РУБЛЬ")
        text = (
            f"На даный момент курс рубля: \n\t Нацбанк \n {(dic['bank']['buy'])}   куп \n {dic['bank']['cell']}   прод \n\t Черный рынок \n {dic['market']['buy']}   куп \n {dic['market']['cell']}   прод")
        bot.send_message(chat_id, text,)


if __name__ == '__main__':
    bot.polling()

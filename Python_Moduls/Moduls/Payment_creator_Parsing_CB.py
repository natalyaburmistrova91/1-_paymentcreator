import json
import requests
from bs4 import BeautifulSoup as bs
import datetime

NOW = datetime.datetime.today().date()
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        b = inputting_value.split(',')
        result = float('.'.join(b))
    return result


def payment_parsing_CB():

    CURRENCY_RATE_DICTIONARY = {}

    NOW_day = f'{NOW.day:02d}/{NOW.month:02d}/{NOW.year}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}

    link = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={NOW_day}'
    response = requests.get(link, headers=headers)
    soup = bs(response.text, 'html.parser')
    find_date = soup.find('valcurs')['date']

    print(f'Дата курса: {find_date}')

    for i in soup.findAll('valute', {}):

        # num_code = i.find('numcode').text
        nominal = i.find('nominal').text
        # name = i.find('name').text
        value = i.find('value').text
        charcode = i.find('charcode').text

        CURRENCY_RATE_DICTIONARY[charcode] = float(try_number(value))/float(nominal)

    return CURRENCY_RATE_DICTIONARY




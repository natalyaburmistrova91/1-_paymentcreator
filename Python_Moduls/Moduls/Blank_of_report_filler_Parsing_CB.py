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


def payment_parsing_CB(option):

    if option == 1:
        day = f'{NOW.day:02d}/{NOW.month:02d}/{NOW.year}'
    elif option == 2:
        day = f'{tomorrow.day:02d}/{tomorrow.month:02d}/{tomorrow.year}'
    else:
        day = option

    dict = {'RUB': 10000}


    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}

    link = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}'
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

        dict[charcode] = round(float(try_number(value))/float(nominal)*10000, 2)

    return find_date, dict




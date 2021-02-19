import xlrd
import datetime
from pymongo import MongoClient

NOW = datetime.datetime.today().date()


def try_number(inputting_value):
    try:
        result = int(inputting_value)
    except ValueError:
        b = inputting_value.split(',')
        result = float('.'.join(b))
    return result


def handle_country_rate_adding():

    client = MongoClient('localhost', 27017)
    db = client['CountryRatesInfo']
    country_rates = db.country_rates

    while True:

        name = input('Введите название страны на английском языке: ').upper()
        while True:
            md_answer = input('Эти курсы для MD? 1. Yes 2. No 3. Одинаковые ставки для всех LVL ')
            if md_answer == '1':
                md = ['Y']
                break
            elif md_answer == '2':
                md = ['N']
                break
            elif md_answer == '3':
                md = ['N', 'Y']
                break
            else:
                print('Вы ввели неверное значение. Повторите.')
        currency = input('Введите название валюты в формате "USD"/"EUR"/"KZT": ')
        hotel_rate = try_number(input('Введите ставку в валюте Отельную (без плана) : '))
        hotel_rate_with_plan = try_number(input('Введите ставку в валюте Отельную (с планом) : '))
        serviced_apartment_rate = try_number(input('Введите ставку в валюте Обслуживаемые апартаменты : '))
        unserviced_apartment_rate = try_number(input('Введите ставку в валюте Необслуживаемые апартаменты : '))

        answer = input(f'Проверьте, пожалуйста. \n'
                       f'Страна {name}, ставка для MD - {md} \n'
                       f'Валюта: {currency} \n'
                       f'Отельная ставка: {hotel_rate} \n'
                       f'Отельная ставка с планом: {hotel_rate_with_plan} \n'
                       f'Обслуживаемые апартаменты: {serviced_apartment_rate} \n'
                       f'Необслуживаемые апартаменты: {unserviced_apartment_rate} \n'
                       f'Все верно? Y/N ').upper()
        if answer == 'Y':
            for md_item in md:
                country_rates.insert_one({'Страна': name,
                                      'MD': md_item,
                                      'Валюта': currency,
                                      'Отельная ставка': hotel_rate,
                                      'Отельная ставка с планом': hotel_rate_with_plan,
                                      'Обслуживаемые апартаменты': serviced_apartment_rate,
                                      'Необслуживаемые апартаменты': unserviced_apartment_rate})
            print('Ставки были добавлены. ')
        else:
            print('Ставки не были добавлены.')
        if input('Продолжаем добавлять ставки? Y/N ').upper() == 'N':
            break




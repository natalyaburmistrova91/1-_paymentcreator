from pymongo import MongoClient
import datetime


def handle_country_rate_deleting():

    answer = input('Вы хотите удалить ставки определенной страны из базы? Y/N ').upper()

    if answer == 'Y':

        # открываем базу
        client = MongoClient('localhost', 27017)
        db = client['CountryRatesInfo']
        country_rates = db.country_rates

        while True:
            name = input('Введите название страны на английском: ').upper()
            country_info = country_rates.find_one({'Страна': name})
            if country_info is not None:
                if input(f'Сейчас в базе следующая информация: {country_info}. Удаляем? Y/N ').upper() == 'Y':
                    country_rates.delete_one({'Страна': name})
                    print(f'Ставки по стране {name} были удалены. ')
                else:
                    print(f'Ставки по стране {name} не были удалены. ')
            else:
                print('Такой страны нет базе данных.')
            if input('Продолжаем удалять ставки? Y/N ').upper() == 'N':
                break




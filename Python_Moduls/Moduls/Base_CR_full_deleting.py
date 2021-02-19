from pymongo import MongoClient


def total_delete_CR():
    client = MongoClient('localhost', 27017)
    db = client['CountryRatesInfo']
    country_rates = db.country_rates

    country_rates.delete_many({})

    print('Проверим есть ли записи после очистки. Они выведутся если есть. ')
    for country_rate in country_rates.find({}):
        print(country_rate)
    print('База очищена.')



if __name__ == '__mane__':
    total_delete()
    # check base
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    for employee in employees.find({}):
        print(employee)
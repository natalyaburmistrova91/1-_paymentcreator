import datetime
from pymongo import MongoClient
from Base_E_CC_first_fullfilling import first_download
from Base_E_full_deleting import total_delete_E
from Base_E_handle_bank_req_adding import handle_bank_adding
from Base_E_handle_bank_req_deleting import handle_bank_req_deleting
from Base_E_handle_employee_adding import handle_employee_adding
from Base_E_update_actual import update_actual
from Base_CR_handle_country_rate_adding import handle_country_rate_adding
from Base_CR_handle_country_rate_deleting import handle_country_rate_deleting
from Base_CR_full_deleting import total_delete_CR
from Base_E_update_MD_status import update_md_status
from Base_E_upload_enterprise_id import upload_enterprise_id
from Base_E_CC_reserve_copy_excel import reserve_copy


def base():

    NOW = datetime.datetime.today().date()

    while True:

        answer1 = input('С какой базой вы хотите поработать? \n1. База Employees \n2. База Country rates '
                       '\n3. Выход \nВаш выбор: ')

        if answer1 == '1':

            client = MongoClient('localhost', 27017)
            db = client['EmployeeInfo']
            employees = db.emloyees

            while True:
                answer = input('Что вы хотите сделать? \n1. Загрузить базу из СС \n2. Полностью очистить базу '
                               '\n3. Сделать резервную копию базу в Excel' 
                               '\n4. Проверить записи в базе \n5. Найти данные сотрудника по табельному номеру '
                               '\n6. Добавить банковские реквизиты вручную \n7. Удалить банковские реквизиты и внести комментарий '
                               '\n8. Вручную добавить сотрудника \n9. Актуализировать базу данных по файлу от Аксор '
                               '\n10. Добавить в базу Enterprise id сотрудников '
                               '\n11. Изменить статус MD у сотрудника \nВаш выбор: ')
                if answer == '1':
                    first_download(NOW)
                elif answer == '2':
                    if input('Вы уверены что хотите полностью очистить базу Employees? Y/N ').upper() == 'Y':
                        total_delete_E()
                elif answer == '3':
                    reserve_copy(NOW)
                elif answer == '4':
                    calc = 0
                    for employee in employees.find({}):
                        calc += 1
                        print(employee)
                    print(f'В базе {calc} сотрудников. ')
                elif answer == '5':
                    tab_number = int(input('Введите табельный номер: '))
                    print(employees.find_one({"Табельный номер": tab_number}))
                elif answer == '6':
                    handle_bank_adding()
                elif answer == '7':
                    handle_bank_req_deleting()
                elif answer == '8':
                    handle_employee_adding(NOW)
                elif answer == '9':
                    update_actual(NOW)
                elif answer == '10':
                    upload_enterprise_id()
                elif answer == '11':
                    update_md_status()
                else:
                    print('Вы ввели неверное значение! ')
                if input('Хотите выполнить другие действия с базой Employees? Y/N ').upper() == 'N':
                    break
        elif answer1 == '2':

            client = MongoClient('localhost', 27017)
            db = client['CountryRatesInfo']
            country_rates = db.country_rates

            while True:
                answer = input('Что вы хотите сделать? \n1. Внести новую страну \n2. Посмотреть, что уже занесено '
                               '\n3. Удалить страну по названию \n4. Полностью удалить базу \nВаш выбор: ')
                if answer == '1':
                    handle_country_rate_adding()
                elif answer == '2':
                    for country_rate in country_rates.find({}):
                        print(country_rate)
                elif answer == '3':
                    handle_country_rate_deleting()
                elif answer == '4':
                    if input('Вы уверены что хотите полностью очистить базу Country rate? Y/N ').upper() == 'Y':
                        total_delete_CR()
                else:
                    print('Вы ввели неверное значение! ')
                if input('Хотите выполнить другие действия с базой Country rates? Y/N ').upper() == 'N':
                    break
        elif answer1 == '3':
            break
        else:
            print('Вы ввели неверное значение! ')

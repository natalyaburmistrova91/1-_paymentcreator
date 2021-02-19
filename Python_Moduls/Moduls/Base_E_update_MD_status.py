import xlrd
import datetime
from pymongo import MongoClient


NOW = datetime.datetime.today().date()


def update_md_status():

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    while True:
        tab_number = int(input('Введите табельный номер сотрудника, которому хотите обновить статус MD: '))
        employee_info = employees.find_one({'Табельный номер': tab_number})
        if employee_info is not None:
            while True:
                md_status_answer = input(f'Это {employee_info["ФИО"]}. Сотрудник MD? Y/N ').upper()
                if md_status_answer == 'Y':
                    md_status = 'Y'
                    break
                elif md_status_answer == 'N':
                    md_status = 'N'
                    break
                else:
                    print('Вы ввели неверное значение. Повторите, пожалуйста. ')
            employees.update_one({'Табельный номер': tab_number},
                                         {'$set': {'MD': md_status}})
        # if not found
        else:
            print('Такого сотрудника нет в базе! ')
        answer = input('Продолжаем работать с изменением статуса MD? Y/N').upper()
        if answer == 'N':
            break




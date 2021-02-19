import xlrd
import datetime
from pymongo import MongoClient

NOW = datetime.datetime.today().date()

def handle_employee_adding(NOW):
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    while True:

        while True:
            tab_num = input('Введите табельный номер сотрудника: ')
            if len(tab_num) == 8:
                break
            else:
                print('Вы ввели неверное количество цифр. Повторите ввод. ')
        tab_number = int(tab_num)
        fio = input('Введите ФИО сотрудника: ')

        while True:
            bank_answer = int(input('Какой банк? 0 - ДРУГОЙ БАНК/1 - CitiBank '))
            if bank_answer == 0:
                bank = 'ДРУГОЙ БАНК'
                bank_req = input('Введите банковские реквизиты: ')
                break
            elif bank_answer == 1:
                bank = 'CitiBank'
                bank_req = input('Введите банковские реквизиты: ')
                bank_req_split = bank_req.split('#')
                if len(bank_req_split[0]) != 10:
                    print('Перепроверьте реквизиты. Банковский счет должен быть равен 10 символам')
                try:
                    int_bank = int(bank_req_split[0])
                except ValueError:
                    print('Перепроверьте реквизиты. В счете есть не только цифры.')
                break
            else:
                print('Вы ввели неверное значение, повторите.')

        while True:
            status_answer = int(input('Сотрудник резидент в банке? 0 - да/1 - нет '))
            if status_answer == 0:
                status = 'резидент'
                break
            elif status_answer == 1:
                status = 'Нерезидент'
                break
            else:
                print('Вы ввели неверное значение, повторите.')
        answer = input(f'Проверьте, пожалуйста. \n'
                       f'Сотрудник {fio}, табельный номер {tab_number} \n'
                       f'Банк: {bank} \n'
                       f'Реквизиты: {bank_req} \n'
                       f'Статус в банке: {status} \n'
                       f'Все верно? Y/N ').upper()
        if answer == 'Y':
            employees.insert_one({'Табельный номер': tab_number,
                                  'ФИО': fio,
                                  'Банк': bank,
                                  'Реквизиты': bank_req,
                                  'Статус': status,
                                  'Дата обновления': f'{NOW}'})  # f'{NOW}'
            print('Сотрудник был добавлен. ')
        else:
            print('Реквизиты не были добавлены.')
        if input('Продолжаем добавлять сотрудников? Y/N ').upper() == 'N':
            break




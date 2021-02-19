from pymongo import MongoClient
import datetime


def handle_bank_req_deleting():

    answer = input('Вам прислали изменения реквизитов и вы хотите удалить их из базы? Y/N ').upper()

    if answer == 'Y':

        # открываем базу
        client = MongoClient('localhost', 27017)
        db = client['EmployeeInfo']
        employees = db.emloyees

        while True:
            tab_number = int(input('Введите табельный номер сотрудника: '))
            employee = employees.find_one({'Табельный номер': tab_number})
            if employee is not None:
                if input(f'Это {employee["ФИО"]}. Продолжаем? Y/N ').upper() == 'Y':
                    while True:
                        bank_answer = input('Какой банк? 0 - ДРУГОЙ БАНК/1 - CitiBank ')
                        if bank_answer == '0':
                            bank = 'ДРУГОЙ БАНК'
                            break
                        elif bank_answer == '1':
                            bank = 'CitiBank'
                            break
                        else:
                            print('Вы ввели неверное значение, повторите.')
                    while True:
                        status_answer = input('Сотрудник резидент в банке? 0 - да/1 - нет ')
                        if status_answer == '0':
                            status = 'резидент'
                            break
                        elif status_answer == '1':
                            status = 'Нерезидент'
                            break
                        else:
                            print('Вы ввели неверное значение, повторите.')
                    comment = input('Введите комментарий в свободной форме: ')
                    answer = input(f'Проверьте, пожалуйста. \n '
                                   f'Сотрудник {employees.find_one({"Табельный номер": tab_number})["ФИО"]}, табельный номер: {tab_number} \n '
                                   f'Банк: {bank}  \n'
                                   f'Реквизиты: None  \n' 
                                   f'Статус в банке: {status} \n'
                                   f'Комментарий: {comment} \n'
                                   f'Все верно? Y/N ').upper()
                    if answer == 'Y':
                        employees.update_one({'Табельный номер': int(tab_number)},
                                             {'$set': {'Банк': bank, 'Реквизиты': 'None', 'Статус': status, 'Комментарий': comment}})
                        print('Реквизиты были удалены. ')
                    else:
                        print('Реквизиты не были добавлены.')
            else:
                print('Сотрудника нет в базе данных. Воспользуйтесь добавлением вручную или обновите по файлу Аксор.')
            if input('Продолжаем удалять реквизиты? Y/N ').upper() == 'N':
                break




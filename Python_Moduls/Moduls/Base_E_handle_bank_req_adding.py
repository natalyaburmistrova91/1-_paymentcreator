from pymongo import MongoClient


def handle_bank_adding():

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    answer = input('Вы хотите добавить банковские реквизиты? Y/N ').upper()
    flag = 0

    if answer == 'Y':
        while flag == 0:
            tab_number = int(input('Введите табельный номер сотрудника: '))
            employee_find = employees.find_one({'Табельный номер': tab_number})
            if employee_find is not None:
                answer2 = input(f"Это {employee_find['ФИО']}. Продолжаем? Y/N ").upper()
                if answer2 == 'Y':
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
                    answer3 = input(f'Проверьте, пожалуйста. \n'
                                    f'Сотрудник {employee_find["ФИО"]} \n'
                                    f'Банк: {bank}  \n'
                                    f'Реквизиты: {bank_req} \n'
                                    f'Статус в банке: {status}  \n'
                                    f'Все верно? Y/N ').upper()
                    if answer3 == 'Y':
                        employees.update_one({'Табельный номер': tab_number},
                                             {'$set': {'Банк': bank, 'Реквизиты': bank_req, 'Статус': status}})
                    else:
                        print('Реквизиты не были добавлены.')
                    flag = int(input('Продолжаем вносить реквизиты? 0 - да/1 - нет '))
            else:
                print('Такого сотрудника нет в базе данных.')
                flag = int(input('Продолжаем вносить реквизиты? 0 - да/1 - нет '))
    else:
        print('Окей, завершаем работу.')


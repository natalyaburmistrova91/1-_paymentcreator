import datetime
from pymongo import MongoClient
from Payment_creator_Parsing_CB import payment_parsing_CB


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        a = inputting_value.split(' ')
        b = float(''.join(a))
        c = b.split(',')
        result = float('.'.join(c))
    return result


def get_payments():
    currency_rate_dictionary = payment_parsing_CB()
    payment_type = int(input('Укажите тип выплаты: 1. аванс 2. возмещение 3. доплата: '))
    payment_date = input('Введите даты командировки: ')
    if payment_type == 1:
        bt_location = int(input('У сотрудника 1. заграничная командировка 2. командировка по России: ' ))
        bt_advance = int(input('Сотрудник хочет аванс 1. только на суточные 2. на суточные и отель: '))
        result = 0
        days_number = int(input('Количество дней: '))
        if bt_location == 1:
            per_diems_upper = int(input('У сотрудника суточные 1. свыше 2500 рублей в день 2. ниже 2500 рублей в день: '))
            if per_diems_upper == 1:
                result += int((days_number - 1) * 2500 + 700)
            else:
                daily_rate = int(input('Введите ставку суточных в стране: '))
                course_name = input('Введите название валюты в стране (например USD): ')
                result += int((days_number - 1) * daily_rate * currency_rate_dictionary.get(course_name) + 700)
        else:
            result += days_number * 700
        comment = 'N'
        if bt_advance == 2:
            if bt_location == 1:
                hotel_rate = try_number(input('Введите сумму в валюте за отель: '))
                course_name = input('Введите название валюты (например USD): ')
                result += int(hotel_rate * currency_rate_dictionary.get(course_name))
            else:
                hotel_rate = try_number(input('Введите сумму за отель: '))
                result += int(hotel_rate)
            comment = input('Введите комментарий - АО (если не будет - введите "N"): ').upper()
        payment_type_for_1c = 'Аванс'
        print(f'Авансовый платеж равен {result}.')
    elif payment_type == 3:
        result = try_number(input('Введите сумму к доплате: ' ))
        payment_type_for_1c = 'Доплата'
        comment = input('Введите комментарий (ВЖ / ВА / ВО)  (если не будет - введите "N"): ').upper()
    else:
        result = try_number(input('Введите сумму к возмещению: ' ))
        payment_type_for_1c = 'Возмещение'
        comment = input('Введите комментарий (ВЖ / ВА / ВО)  (если не будет - введите "N"): ').upper()
    if comment == 'Т':
        comment = 'N'
    return [result, payment_type_for_1c, payment_date, comment]


def add_tab_payment(tab_number):

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    employee_info = employees.find_one({'Табельный номер': tab_number})

    if employee_info is not None:
        print(f'Сотрудник {employee_info["ФИО"]}')
        if employee_info["Комментарий"] != 'None':
            print(f'Комментарий: {employee_info["Комментарий"]}')
        if employee_info["Банк"] != "None" and employee_info["Статус"] != "None" and employee_info["Реквизиты"] != 'None':
            get_payment = get_payments()
            return [tab_number, get_payment[0], get_payment[1], get_payment[2], get_payment[3]]
            # 1.tab_number, 2.amount of payment, 3.payment type (Advance or reimbursement) 4.dates of BT 5.comment
        else:
            print('У сотрудника не хватает реквизитов в базе данных для платежа. Перевод данному сотруднику не будет оформлен.')
            return None
    else:
        print(f'Сотрудника с табельным номером {tab_number} нет в базе!')
        return None

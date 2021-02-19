import datetime
from pymongo import MongoClient
import xlrd
from Payment_creator_Base_check_employee_1 import check_employee_1
from Payment_creator_Base_handle_payment_21 import add_tab_payment
from Payment_creator_Base_el_bank_statement_22 import electronic_bank_statement_creator
from Payment_creator_Base_payment_issue_23 import payment_creator, payment_creator_other


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        a = inputting_value.split(' ')
        result = float(''.join(a))
        b = result.split(',')
        result = float('.'.join(b))
    return result


def payment_creator_base():

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    NOW = datetime.datetime.today().date()

    while True:
        answer = input('Добро пожаловать в Payment Creator! Что вы хотите сделать: \n'
                       '1 - проверить сотрудников на наличие в базе\n'
                       '2 - создать платежные поручения\n'
                       '3 - выйти из программы: ')
        if answer == '1':
            check_employee_1()
        elif answer == '2':
            print("Приступим к выплате!")
            list_of_all_payment = []  # in this list should be lists of:
            # 1.tab_number, 2.amount of payment, 3.payment type (Advance or reimbursement) 4.dates of BT 5.comment
            handle_payment = input("Будут платежи не из списка 1С? Y/N ").upper()
            if handle_payment == 'Y':
                upload_employee = int(input('Выберите: 1. загрузить файл с табельными номерами 2. вводить вручную: '))
                if upload_employee != 2:
                    list_upload = []
                    f_1 = open("C:\python_working_files\list of tab numbers (handle payment).txt", 'r', encoding="utf-8")
                    for line in f_1:
                        list_upload.append(int(line.strip('\n')))
                    if len(list_upload) != 0:
                        for el in list_upload:
                            check_employee = add_tab_payment(el)
                            # Return None or 5 needed positions
                            if check_employee is not None:  # added to total list if not None
                                list_of_all_payment.append(check_employee)
                else:
                    while True:
                        tab_number = int(input('Введите табельный номер сотрудника или 0 (если закончили): '))
                        if tab_number == 0:
                            break
                        check_employee = add_tab_payment(tab_number)
                        if check_employee is not None:  # проверка на наличие в СС
                            list_of_all_payment.append(check_employee)
            one_c_payment = input("Будут платежи из 1С? Y/N ").upper()
            if one_c_payment == 'Y':
                one_c_payment_file = xlrd.open_workbook('C:\python_working_files\list_of_AR.xls', formatting_info=True)
                one_c_payment_sheet = one_c_payment_file.sheet_by_index(0)
                for row_num in range(1, one_c_payment_sheet.nrows):
                    row_line = one_c_payment_sheet.row_values(row_num)
                    employee_name = row_line[3].split()
                    employee_name_real = ' '.join(employee_name)
                    employee_info = employees.find_one({'ФИО': employee_name_real})
                    if employee_info is not None:
                        if employee_info["Банк"] != "None" \
                                and employee_info["Реквизиты"] != "None" \
                                and employee_info["Статус"] != "None":
                            reimb_1c = input(f'{employee_info["ФИО"]} возмещаем сумму {row_line[4]}. Верно? Y/N ').upper()
                            if reimb_1c == 'Y':
                                list_of_all_payment.append(
                                    [employee_info['Табельный номер'], float(row_line[4]), "Возмещение",
                                     row_line[9].split('#')[0],
                                     row_line[9].split('#')[2]])
                            else:
                                reimb_1c_sum = (try_number(input("Введите сумму к возмещению: ")))
                                list_of_all_payment.append(
                                    [employee_info['Табельный номер'], reimb_1c_sum, "Доплата", row_line[9].split('#')[0],
                                     row_line[9].split('#')[2]])
                        else:
                            print(f'У сотрудника {employee_info["ФИО"]} не хватает реквизитов в базе. '
                                  f'Выплата в Платеж не будет добавлена.')
                    else:
                        print('Сотрудника нет в базе! Выплата в Платеж не будет добавлена.')
            # Creating the list for 1C check bank statement
            list_of_all_payment_1c = []
            user_name = input('Введите имя пользователя (например N или D): ').upper()
            for el in list_of_all_payment:
                employee_info = employees.find_one({'Табельный номер': el[0]})
                list_of_all_payment_1c.append([el[0], employee_info['ФИО'], el[2], el[3], el[1], el[4]])
            f_4 = open(
                f'Z:/0_Helpful information/Info for Finance/Bank_statements/{user_name}_{NOW.day:02d}-{NOW.month:02d}-{NOW.year:02d}_bank_statement.txt',
                'w', encoding="utf-8")
            for e in list_of_all_payment_1c:
                f_4.write(f'{e[0]} {e[1]} {e[2]} {e[3]} {e[4]:.2f} {e[5]}\n')
            f_4.close()
            # Creating the list for 1c bank statement uploading
            electronic_bank_statement_creator(list_of_all_payment_1c, user_name)
            #  Deviding the list on employees with other bank and citi and counting total sum of payment
            list_of_all_payment_citi = []
            list_of_all_payment_other = []
            for el in list_of_all_payment:
                employee_info = employees.find_one({'Табельный номер': el[0]})
                if employee_info['Банк'] == 'CitiBank':
                    list_of_all_payment_citi.append([el[0], el[1], employee_info['Реквизиты'], employee_info['Статус']])
                else:
                    list_of_all_payment_other.append([el[0], el[1], employee_info['Реквизиты']])
                    if employee_info['Статус'] == 'Нерезидент':
                        print(f'Сотрудник {employee_info["Статус"]} - нерезидент. '
                              f'Не забудь загрузить в банк документы для валютного контроля')
            #  Deviding list on residents and non-residents for citi
            list_of_resident = []
            list_of_nonresident = []
            total_amount_resident = 0
            total_amount_nonresident = 0
            for i in list_of_all_payment_citi:
                if i[-1] == 'Резидент':
                    i.pop()
                    list_of_resident.append(i)
                    total_amount_resident += i[1] * 100
                else:
                    i.pop()
                    list_of_nonresident.append(i)
                    total_amount_nonresident += i[1] * 100
            if len(list_of_all_payment_other) != 0:
                print('Есть прочие банки!')
                payment_creator_other(list_of_all_payment_other)
            if len(list_of_resident) != 0:
                print('Делаем платеж для резидентов!')
                payment_creator(list_of_resident, total_amount_resident / 100)
            if len(list_of_nonresident) != 0:
                print('Делаем платеж для нерезидентов!')
                payment_creator(list_of_nonresident, total_amount_nonresident / 100, '{VO70205}')
            print('Платежи созданы.')

        else:
            break

import xlrd
import datetime

NOW = datetime.datetime.today()
CURRENCY_RATE_DICTIONARY = {
}
EMPLOYEE_DICTIONARY = {
}
EMPLOYEE_DICTIONARY_FROM_1C = {
}
EMPLOYEE_DICTIONARY_FROM_1C_reverse = {
}


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        b = inputting_value.split(',')
        result = float('.'.join(b))
    return result


def employee_dictionary_filler():
    employee_file = xlrd.open_workbook('Z:/0_Helpful information/Info for Finance/VENDORS/CC.xls', formatting_info=True)
    employee_sheet = employee_file.sheet_by_index(0)
    for row_num in range(1, employee_sheet.nrows):
        row_line = employee_sheet.row_values(row_num)
        EMPLOYEE_DICTIONARY[row_line[0]] = [row_line[1], row_line[3], row_line[4], row_line[5], row_line[6]]
        EMPLOYEE_DICTIONARY_FROM_1C[row_line[0]] = row_line[2]
        EMPLOYEE_DICTIONARY_FROM_1C_reverse[row_line[2]] = row_line[0]


def country_rate_dictionary_filler():
    courses_file = xlrd.open_workbook('Z:/0_Helpful information/Info for Finance/PIT/Иностранные формы/blank_of_report_filler/Courses.xls', formatting_info=True)
    courses_sheet = courses_file.sheet_by_index(0)
    date = courses_sheet.row_values(0)[1]
    print(f'ВНИМАНИЕ! КУРСЫ БУДУТ ИСПОЛЬЗОВАНЫ ОТ ДАТЫ: {date}')
    for row_num in range(2, courses_sheet.nrows):
        row_line = courses_sheet.row_values(row_num)
        CURRENCY_RATE_DICTIONARY[row_line[1]] = float(row_line[5])


def check_employee_avail():
    employee_none = []
    employee_avail = []
    handle_payment = input("Будут платежи не из выгруженного списка 1С? Y/N ").upper()
    while handle_payment == 'Y':
        tab_number = int(input('Введите табельный номер сотрудника (чтобы закончить, введите 0): '))
        if tab_number == 0:
            break
        empolyee_info = EMPLOYEE_DICTIONARY.get(tab_number)
        if empolyee_info == None:
            print(f'Сотрудника с {tab_number} нет в списке!')
            employee_none.append(tab_number)
        else:
            print(f'Сотрудник с {tab_number} есть в списке ({EMPLOYEE_DICTIONARY.get(tab_number)[0]}, {EMPLOYEE_DICTIONARY.get(tab_number)[1]})!')
            if EMPLOYEE_DICTIONARY.get(tab_number)[2] == 'None':
                print('Расчетный счет сотрудника в файле CC не задан!')
            employee_avail.append(tab_number)
    one_c_payment = input("Будут платежи из выгруженного файла 1С? Y/N ").upper()
    if one_c_payment == 'Y':
        one_c_payment_file = xlrd.open_workbook('list_of_AR.xls', formatting_info=True)
        one_c_payment_sheet = one_c_payment_file.sheet_by_index(0)
        for row_num in range(1, one_c_payment_sheet.nrows):
            row_line = one_c_payment_sheet.row_values(row_num)
            if EMPLOYEE_DICTIONARY_FROM_1C_reverse.get(row_line[3]) is None:
                print(f'Сотрудника {row_line[3]} нет в СС!')
            else:
                key_tab = EMPLOYEE_DICTIONARY_FROM_1C_reverse.get(row_line[3])
                if EMPLOYEE_DICTIONARY.get(key_tab)[2] == 'None':
                    print(f'Расчетный счет сотрудника {row_line[3]} в файле CC не задан!')
                else:
                    print(f'У {row_line[3]} все хорошо!')
    down_load_check = int(input('Введите 1. если хотите продолжить 2. завершить и выгрузить список табельных номеров в файл: '))
    if handle_payment == 'Y':
        f_1 = open("list of tab numbers (handle payment).txt", 'w', encoding="utf-8")
        for a in employee_avail:
            f_1.write(" ".join([str(a), '\n']))
        for n in employee_none:
            f_1.write(" ".join([str(n), '\n']))
    if down_load_check == 1:
        return 3
    elif down_load_check == 2:
        return 1


def get_payments():
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
                course_name = input('Введите название валюты в стране: ')
                result += int((days_number - 1) * daily_rate * CURRENCY_RATE_DICTIONARY.get(course_name) + 700)
        else:
            result += days_number * 700
        comment = 'N'
        if bt_advance == 2:
            if bt_location == 1:
                hotel_rate = try_number(input('Введите сумму в валюте за отель: '))
                course_name = input('Введите название валюты: ')
                result += int(hotel_rate * CURRENCY_RATE_DICTIONARY.get(course_name))
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
    if EMPLOYEE_DICTIONARY.get(tab_number) is not None:
        print(f'Сотрудник {EMPLOYEE_DICTIONARY.get(tab_number)[0]}, счет в {EMPLOYEE_DICTIONARY.get(tab_number)[1]}')
        if EMPLOYEE_DICTIONARY.get(tab_number)[4] != 'None':
            print(f'Комментарий: {EMPLOYEE_DICTIONARY.get(tab_number)[4]}')
        get_payment = get_payments()
        if EMPLOYEE_DICTIONARY.get(tab_number)[1] == 'ДРУГОЙ БАНК':
            if EMPLOYEE_DICTIONARY.get(tab_number)[2] == 'None':
                print(f'Счет сотрудника не найден! Записан в платеж не будет!')
        return [tab_number, get_payment[0], get_payment[1], get_payment[2], get_payment[3]]  #  возврат табельный номер, сумма, тип платежа, даты, комментарий
    else:
        print('Сотрудника нет в CC!')
        return None


def payment_creator(list_of_employees, total_amount, vo=''):
    num_of_payment = input('Введите номер платежа: ')
    year = NOW.year % 2000
    number_of_payment = f'{NOW.day:02d}{NOW.month:02d}{year:02d}{num_of_payment}'
    f_2 = open(f'{number_of_payment}_payment.txt', 'w', encoding="utf-8")
    f_2.write(f'0700986063#RUR#{NOW.day:02d}/{NOW.month:02d}/{year}#{number_of_payment}#{total_amount:.2f}\n')
    for e in list_of_employees:
        f_2.write(f'{e[0]}{e[1]:.2f}\n')
    f_2.close()
    f_3 = open(f'{number_of_payment}_admin_message.txt', 'w', encoding="utf-8")
    f_3.write(f'Payroll Consumer / Заработная плата физических лиц\n'
              f'\n'
              f'Распоряжение на перечисление денежных средств согласно реестру в соответствии с\n'
              f'Соглашением о перечислении сумм заработной платы с АО КБ "Ситибанк":\n'
              f'\n'
              f'Номер распоряжения: {number_of_payment}\n'
              f'Дата распоряжения: {NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'Сумма цифрами: {total_amount:.2f}\n'
              f'Номер счета плательщика: 700986063\n'
              f'Назначение платежа: {vo} Выплата сотрудникам командировочных средств в соответствии с реестром.\n'
              )
    f_3.close()


def payment_creator_other(list_of_all_payment_other):
    year = NOW.year % 2000
    date_of_file = f'{NOW.day:02d}{NOW.month:02d}{year:02d}'
    f_4 = open(f'{date_of_file}_other_banks_check.txt', 'w', encoding="utf-8")
    f_6 = open(f'{date_of_file}_other_banks_download.txt', 'w', encoding="utf-8")
    f_4.write(f'Номер в списке / ФИО /  Сумма / Банк / Резиденство / Комментарий\n')
    k = 1
    number = int(input('Введите стартовое значение для нумерации прочих платежей: '))
    for e in list_of_all_payment_other:
        f_4.write(f'{k}/ {e[0]} / {e[1]} / {e[2]:.2f} / {e[4]} / {e[5]}\n')
        if EMPLOYEE_DICTIONARY.get(e[0])[2] != 'None':
            bank_line_list = list(e[3])
            bank_line_list.insert(8, f'{NOW.year}{NOW.month:02d}{NOW.day:02d}')
            bank_line_list.insert(20, f'{e[2]:.2f}')
            bank_line_list.insert(45, f'{number:05d}')
            bank_line_actual = ''.join(bank_line_list)
            f_6.write(f'{bank_line_actual}\n')
            number += 1
        k += 1
    f_4.close()
    f_6.close()



def electronic_bank_statement_creator(list_of_all_payment_1c):
    f_5 = open(
        f'Z:/0_Helpful information/Info for Finance/Bank_statements/N_{NOW.day:02d}-{NOW.month:02d}-{NOW.year:02d}_bank_statement_el.txt',
        'w', encoding="ANSI")
    f_5.write(f'1CClientBankExchange\n'
              f'ВерсияФормата=1.02\n'
              f'Кодировка=Windows\n'
              f'Отправитель=CitiDirect\n'
              f'Получатель=1С:Предприятие\n'
              f'ДатаСоздания=10.01.2020\n'
              f'ВремяСоздания=10:29:51\n'
              f'ДатаНачала={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'ДатаКонца={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'РасчСчет=40702810100700986063\n'
              f'\n'
              f'СекцияРасчСчет\n'
              f'ДатаНачала={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'ДатаКонца={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'РасчСчет=40702810100700986063\n'
              f'НачальныйОстаток=0.00\n'
              f'ВсегоПоступило=0.00\n'
              f'ВсегоСписано=0.00\n'
              f'КонечныйОстаток=0.00\n'
              f'КонецРасчСчет\n'
              f'\n')
    for e in list_of_all_payment_1c:
        f_5.write(f'СекцияДокумент=Банковский ордер\n'
                  f'Номер={e[5]}\n'
                  f'Дата={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
                  f'Сумма={e[4]:.2f}\n'
                  f'ПлательщикСчет=40702810100700986063\n'
                  f'ДатаСписано={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
                  f'Плательщик1=\n'
                  f'ПлательщикРасчСчет=40702810100700986063\n'
                  f'ПлательщикБанк1=\n'
                  f'ПлательщикБанк2=\n'
                  f'ПлательщикБИК=\n'
                  f'ПолучательИНН={e[0]}\n'
                  f'Получатель1={e[1]}\n'
                  f'Получатель2=\n'
                  f'Получатель3=\n'
                  f'Получатель4=\n'
                  f'ПолучательБанк1=\n'
                  f'ПолучательБанк2=\n'
                  f'ПолучательБИК=\n'
                  f'ВидПлатежа=Электронно\n'
                  f'ВидОплаты=\n'
                  f'Код=\n'
                  f'СтатусСоставителя=\n'
                  f'ПлательщикКПП=\n'
                  f'ПолучательКПП=\n'
                  f'ПоказательКБК=\n'
                  f'ОКАТО=\n'
                  f'ПоказательОснования=\n'
                  f'ПоказательПериода=\n'
                  f'ПоказательНомера=\n'
                  f'ПоказательДаты=\n'
                  f'ПоказательТипа=\n'
                  f'Очередность=05\n'
                  f'НазначениеПлатежа={e[2]} {e[3]}\n'
                  f'\n'
                  f'КонецДокумента\n'
                  f'\n')
    f_5.write(f'КонецФайла\n')
    f_5.close()

#  Создаем словарь с курсами
country_rate_dictionary_filler()

#  Создаем словарь из файла CC
employee_dictionary_filler()

#  Проверка наличия табельного номера в словаре
cont_prog = int(input('Будем проверять наличие сотрудника в списке? (1. будем проверять 2. не будем проверять): '))
if cont_prog == 1:
    cont_prog = check_employee_avail()
#  Создаем платежку
if cont_prog != 1:
    upload_employee = 0
    print("Приступим к выплате!")
    list_of_all_payment = []
    handle_payment = input("Будут платежи не из списка 1С? Y/N ").upper()
    if handle_payment == 'Y':
        if cont_prog != 3:
            upload_employee = int(input('Выберите: 1. загрузить файл с табельными номерами 2. вводить вручную: '))
        # Создание списка сити при загрузке табельных номеров
        if upload_employee != 2:
            list_upload = []
            f_1 = open("list of tab numbers (handle payment).txt", 'r', encoding="utf-8")
            for line in f_1:
                list_upload.append(int(line.strip('\n')))
            if len(list_upload) != 0:
                for el in list_upload:
                    check_employee = add_tab_payment(el)  #  Возврат таб номер check_employee[0],сумма [1], тип платежа [2], даты [3], комментарий [4] (если нашел в СС)
                    if check_employee is not None:    #  проверка на наличие в СС
                        list_of_all_payment.append(check_employee)
        #  Создание списка сити при заведении их вручную
        else:
            while True:
                tab_number = int(input('Введите табельный номер сотрудника или 0 (если закончили): '))
                if tab_number == 0:
                    break
                check_employee = add_tab_payment(tab_number)  #  Возврат таб номер check_employee[0],сумма [1], тип платежа [2], даты [3], комментарий [4] (если нашел в СС)
                if check_employee is not None:  #  проверка на наличие в СС
                    list_of_all_payment.append(check_employee)
    one_c_payment = input("Будут платежи из 1С? Y/N ").upper()
    #  Создание списка из выгруженного 1С
    if one_c_payment == 'Y':
        one_c_payment_file = xlrd.open_workbook('list_of_AR.xls', formatting_info=True)
        one_c_payment_sheet = one_c_payment_file.sheet_by_index(0)
        for row_num in range(1, one_c_payment_sheet.nrows):
            row_line = one_c_payment_sheet.row_values(row_num)
            if EMPLOYEE_DICTIONARY_FROM_1C_reverse.get(row_line[3]) is None:
                print(f'Сотрудника {row_line[3]} нет в СС!')
            else:
                key_tab = EMPLOYEE_DICTIONARY_FROM_1C_reverse.get(row_line[3])
                if EMPLOYEE_DICTIONARY.get(key_tab)[2] == 'None':
                    print(f'Расчетный счет сотрудника {row_line[3]} в файле CC не задан!')
                else:
                    reimb_1c = input(f"{row_line[3]} возмещаем сумму {row_line[4]}. Верно? Y/N ").upper()
                    if reimb_1c == 'Y':
                        list_of_all_payment.append([int(key_tab), float(row_line[4]), "Возмещение", row_line[9].split('#')[0], row_line[9].split('#')[2]])
                    else:
                        reimb_1c_sum = (try_number(input("Введите сумму к возмещению: ")))
                        list_of_all_payment.append(
                            [int(key_tab), reimb_1c_sum, "Доплата", row_line[9].split('#')[0], row_line[9].split('#')[2]])
    # Делаем список для проведения в 1С
    list_of_all_payment_1c = []
    for el in list_of_all_payment:
        list_of_all_payment_1c.append([el[0], EMPLOYEE_DICTIONARY_FROM_1C.get(el[0]), el[2], el[3], el[1], el[4]])
    f_4 = open(f'Z:/0_Helpful information/Info for Finance/Bank_statements/N_{NOW.day:02d}-{NOW.month:02d}-{NOW.year:02d}_bank_statement.txt', 'w', encoding="utf-8")
    for e in list_of_all_payment_1c:
        f_4.write(f'{e[0]} {e[1]} {e[2]} {e[3]} {e[4]:.2f} {e[5]}\n')
    f_4.close()
    # Делаем список для проведения в 1С(электронно)
    electronic_bank_statement_creator(list_of_all_payment_1c)
    #  Разделяем список на другие банки и сити и считаем тотал сумму платежа
    list_of_all_payment_citi = []
    list_of_all_payment_other = []
    for el in list_of_all_payment:
        if EMPLOYEE_DICTIONARY.get(el[0])[1] == 'CitiBank':
            list_of_all_payment_citi.append([el[0], el[1], EMPLOYEE_DICTIONARY.get(el[0])[3]])
        else:
            list_of_all_payment_other.append([el[0], EMPLOYEE_DICTIONARY.get(el[0])[0], el[1], EMPLOYEE_DICTIONARY.get(el[0])[2], EMPLOYEE_DICTIONARY.get(el[0])[3], EMPLOYEE_DICTIONARY.get(el[0])[4]])
    #  Разделяем список на резиденты и нерезиденты
    list_of_resident = []
    list_of_nonresident = []
    total_amount_resident = 0
    total_amount_nonresident = 0
    for i in list_of_all_payment_citi:
        list_of_payment = [EMPLOYEE_DICTIONARY.get(i[0])[2], i[1]]
        if i[2] == 'Резидент':
            list_of_resident.append(list_of_payment)
            total_amount_resident += i[1] * 100
        else:
            list_of_nonresident.append(list_of_payment)
            total_amount_nonresident += i[1] * 100
    if len(list_of_all_payment_other) != 0:
        print('Есть прочие банки!')
        payment_creator_other(list_of_all_payment_other)
    if len(list_of_resident) != 0:
        print('Делаем платеж для резидентов!')
        payment_creator(list_of_resident, total_amount_resident/100)
    if len(list_of_nonresident) != 0:
        print('Делаем платеж для нерезидентов!')
        payment_creator(list_of_nonresident, total_amount_nonresident/100, '{VO70205}')
























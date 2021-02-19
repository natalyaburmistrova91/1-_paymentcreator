# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy

LIST_FROM_1C = []
MIXED_LISTS = []
EMAILS_LIST = []
EMPLOYEE_DICTIONARY_FROM_1C = {}
MAIL_DICTIONARY = {}
LIST_OF_EMPLOYEES = []
LIST_OF_EMAILS = []
UNEXPECTED_LIST = []


def employee_dictionary_filler_from1C():
    employee_file = xlrd.open_workbook('Z:/0_Helpful information/Info for Finance/VENDORS/CC.xls', formatting_info=True)
    employee_sheet = employee_file.sheet_by_index(0)
    for row_num in range(1, employee_sheet.nrows):
        row_line = employee_sheet.row_values(row_num)
        EMPLOYEE_DICTIONARY_FROM_1C[row_line[2]] = row_line[0]
        MAIL_DICTIONARY[row_line[0]] = row_line[7]


#  Спрашиваем хочет ли пользователь обновить список или составить письмо?
working_step = int(input('Что вы хотите сделать? 1. Если хотите обновить список 2. Если хотите отправить рассылку: '))
if working_step == 1:
    #  создаем список неподписанных из 1С
    file_from_1c = xlrd.open_workbook('ListOfAdvanceReports.xls', formatting_info=True)
    file_from_1c_sheet = file_from_1c.sheet_by_index(0)
    for row_num in range(1, file_from_1c_sheet.nrows):
        row_line = file_from_1c_sheet.row_values(row_num)
        if row_line[1] != '':
            if row_line[1] == 1:
                LIST_FROM_1C.append([row_line[5], row_line[3], row_line[4], row_line[2]])
            else:
                LIST_FROM_1C.append([row_line[5], row_line[3], row_line[4], 'подписано', row_line[2]])
    LIST_FROM_1C.sort()  # сортируем список
    #  Выгружаем список неподписанных из 1С за месяц
    f_1 = open("list_of_uns_month.txt", 'w', encoding="utf-8")
    for el in LIST_FROM_1C:
        f_1.write(f'{el[0]} {el[1]} {el[2]} {el[3]}\n')
    f_1.close()
    print('Список за месяц выгружен!')
    #  Спрашиваем хочет ли пользователь объединить 2 списка ( текущей и за месяц)
    mix_lists = input('Вы хотите объединить текущий список со списком за месяц? Y/N ').upper()
    if mix_lists == 'Y':
        f_2 = open("list_of_uns_month.txt", 'r', encoding="utf-8")
        for line in f_2:
            MIXED_LISTS.append(line)
        f_2.close()
        f_3 = open("current_list.txt", 'r', encoding="utf-8")
        for line in f_3:
            MIXED_LISTS.append(line)
        f_3.close()
        MIXED_LISTS.sort()
        f_4 = open("new_current_list.txt", 'w', encoding="utf-8")
        for el in MIXED_LISTS:
            f_4.write(f'{el}')
        f_4.close()
else:
    #  создаем словарь с сотрудниками
    employee_dictionary_filler_from1C()
    #  создаем словарь с почтами
    employee_mail_filler()
    print("Мы работаем с файлом current_list в текущей папке (не в резервной). Файл должен быть актуальным.")
    working_q = input('Он актуальный? Y/N ').upper()
    if working_q == 'N':
        print("Без актуализации смысла в этом нет - обнови и возвращайся!:)")
    else:
        f_5 = open("current_list.txt", 'r', encoding="utf-8")
        for line in f_5:
            c = line.split()
            if c[2].isalpha() == False:
                c_key = f'{c[0]} {c[1]}'
            else:
                c_key = f'{c[0]} {c[1]} {c[2]}'
            LIST_OF_EMPLOYEES.append(c_key)
        f_5.close()
        sorted_set_of_employees = sorted(list(set(LIST_OF_EMPLOYEES)))
        for i in sorted_set_of_employees:
            key_tab = EMPLOYEE_DICTIONARY_FROM_1C.get(i)
            if key_tab is None:
                UNEXPECTED_LIST.append(i)
            else:
                mail = MAIL_DICTIONARY.get(key_tab)
                LIST_OF_EMAILS.append(mail)
        f_6 = open("list_of_emails.txt", 'w', encoding="utf-8")
        if len(UNEXPECTED_LIST) != 0:
            f_6.write(f'Вот кого я не нашел в списке 1С:\n')
            for el in UNEXPECTED_LIST:
                f_6.write(f'{el}\n')
        if len(LIST_OF_EMAILS) != 0:
            f_6.write(f'Список тех, кого нашел:\n')
            for el in LIST_OF_EMAILS:
                f_6.write(f'{el}@accenture.com\n')
        f_6.close()

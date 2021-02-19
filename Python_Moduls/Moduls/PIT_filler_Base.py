# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
from pymongo import MongoClient


LIST_OF_FILE = []
LIST_OF_NONRES = {}


def set_style(align_horz, num_format_str=None):
    font = xlwt.Font()  # устанавливаем курсив
    font.name = 'Book Antiqua'
    font.height = 220
    align = xlwt.Alignment()
    align.horz = align_horz
    border = xlwt.Borders()
    border.bottom = xlwt.Borders.THIN
    border.left = xlwt.Borders.THIN
    border.right = xlwt.Borders.THIN
    border.top = xlwt.Borders.THIN
    style = xlwt.XFStyle()
    style.font = font
    style.alignment = align
    style.borders = border
    if num_format_str is not None:
        style.num_format_str = num_format_str
    return style


def pit_filler():

    answer = input('Убедитесь, что выгрузка с 20 счета из 1С расположена по адресу C:\python_working_files '
          '\n и называется PIT_filler_working_file формата xls (не XLSX!). Все верно? Y/N').upper()

    if answer == 'Y':

        #  устанавливаем стили
        style1 = set_style(xlwt.Alignment.HORZ_CENTER)
        style2 = set_style(xlwt.Alignment.HORZ_LEFT)
        style3 = set_style(xlwt.Alignment.HORZ_CENTER, '#,##0.00')

        #  Make connection to the base
        client = MongoClient('localhost', 27017)
        db = client['EmployeeInfo']
        employees = db.emloyees

        #  создаем словарь с нерезидентами
        f_1 = open("C:\python_working_files\list_of_tax_nonres.txt", 'r', encoding="utf-8")
        for line in f_1:
            c = line.split()
            LIST_OF_NONRES[int(c[0])] = [c[1], c[2]]
        #  открываем рабочий файл и делаем список для заполнения
        working_file = xlrd.open_workbook('C:\python_working_files\PIT_filler_working_file.xls', formatting_info=True)
        working_sheet = working_file.sheet_by_index(0)
        for row_num in range(10, working_sheet.nrows - 1):
            row_line = working_sheet.row_values(row_num)
            row_line_1 = row_line[1].split('\n')
            row_dates = row_line_1[1].split()[0]
            name = f'{" ".join(row_line[4].split())}'
            print(name)
            print(employees.find_one({'ФИО': name}))
            employees_info = employees.find_one({'ФИО': name})
            LIST_OF_FILE.append([row_line[0], employees_info['Табельный номер'], row_line[4], row_dates, row_line[6]])
        #  Заполняем новый файл информацией
        blank_of_PIT = xlrd.open_workbook(r'Z:\0_Helpful information\Info for Finance\Python_Moduls\Templates\blank_of_PIT_filler.xls', formatting_info=True)
        #  копируем файл для заполнения
        blank_PIT_filled = copy(blank_of_PIT)
        for i in range(len(LIST_OF_FILE)):
            blank_PIT_filled.get_sheet(0).write(i + 1, 0, LIST_OF_FILE[i][0], style1)  # дата АО
            blank_PIT_filled.get_sheet(0).write(i + 1, 1, LIST_OF_FILE[i][1], style1)  # таб номер
            blank_PIT_filled.get_sheet(0).write(i + 1, 2, LIST_OF_FILE[i][2], style2)  # ФИО
            blank_PIT_filled.get_sheet(0).write(i + 1, 3, LIST_OF_FILE[i][3], style1)  # даты
            blank_PIT_filled.get_sheet(0).write(i + 1, 4, LIST_OF_FILE[i][4], style3)  # сумма гросс
            if LIST_OF_NONRES.get(LIST_OF_FILE[i][1]) is not None:
                blank_PIT_filled.get_sheet(0).write(i + 1, 5, 'НЕрезидент', style1)  # статус
                blank_PIT_filled.get_sheet(0).write(i + 1, 6, 30, style1)  # ставка
            else:
                blank_PIT_filled.get_sheet(0).write(i + 1, 5, 'резидент', style1)  # статус
                blank_PIT_filled.get_sheet(0).write(i + 1, 6, 13, style1)  # ставка
        way = r'Z:\0_Helpful information\Info for Finance\PIT'
        blank_PIT_filled.save(f'{way}\{LIST_OF_FILE[0][0]}-{LIST_OF_FILE[len(LIST_OF_FILE) - 1][0]}.xls')
        print(r'Готово! Файл находится в папке Z:\0_Helpful information\Info for Finance\PIT ')

    else:
        print('Файл не был сформирован!')
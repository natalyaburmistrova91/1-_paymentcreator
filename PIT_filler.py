# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
EMPLOYEE_DICTIONARY_FROM_1C = {}
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


def employee_dictionary_filler_from1C():
    employee_file = xlrd.open_workbook('Z:/0_Helpful information/Info for Finance/VENDORS/CC.xls', formatting_info=True)
    employee_sheet = employee_file.sheet_by_index(0)
    for row_num in range(1, employee_sheet.nrows):
        row_line = employee_sheet.row_values(row_num)
        EMPLOYEE_DICTIONARY_FROM_1C[row_line[2]] = row_line[0]


#  устанавливаем стили
style1 = set_style(xlwt.Alignment.HORZ_CENTER)
style2 = set_style(xlwt.Alignment.HORZ_LEFT)
style3 = set_style(xlwt.Alignment.HORZ_CENTER, '#,##0.00')

#  создаем словарь с сотрудниками
employee_dictionary_filler_from1C()
#  создаем словарь с нерезидентами
f_1 = open("list_of_nonres.txt", 'r', encoding="utf-8")
for line in f_1:
    c = line.split()
    LIST_OF_NONRES[int(c[0])] = [c[1], c[2]]
#  открываем рабочий файл и делаем список для заполнения
working_file = xlrd.open_workbook('workingfile.xls', formatting_info=True)
working_sheet = working_file.sheet_by_index(0)
for row_num in range(10, working_sheet.nrows - 1):
    row_line = working_sheet.row_values(row_num)
    row_line_1 = row_line[1].split('\n')
    row_dates = row_line_1[1].split()[0]
    LIST_OF_FILE.append([row_line[0], EMPLOYEE_DICTIONARY_FROM_1C.get(row_line[4]), row_line[4], row_dates, row_line[6]])
#  Заполняем новый файл информацией
blank_of_PIT = xlrd.open_workbook('blank_of_PIT.xls', formatting_info=True)
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
blank_PIT_filled.save(f'{LIST_OF_FILE[0][0]}-{LIST_OF_FILE[len(LIST_OF_FILE) - 1][0]}.xls')
# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
import os
import datetime


def set_style(align_horz, font_type=None, num_format_str=None):
    font = xlwt.Font()  #
    font.name = 'Arial'
    font.height = 180
    font.bold = font_type
    align = xlwt.Alignment()
    align.horz = align_horz
    style = xlwt.XFStyle()
    style.font = font
    style.alignment = align
    if num_format_str is not None:
        style.num_format_str = num_format_str
    return style


style1 = set_style(xlwt.Alignment.HORZ_CENTER, 'Bold')
style2 = set_style(xlwt.Alignment.HORZ_LEFT)

NOW = datetime.datetime.today()
year = NOW.year
date_of_file = f'{NOW.day:02d}.{NOW.month:02d}.{year:04d}'


signature = int(input('Кто подписант сегодня?(1.Оля 2.Марина 3.Ира): '))
signature_name = ''
if signature == 1:
    signature_name = 'Круглова Ольга Александровна'
elif signature == 1:
    signature_name = 'Шевченко Марина Николаевна'
else:
    signature_name = 'Мамонова Ирина Сергеевна'

list_of_spr = os.listdir(path='Original')
for i in list_of_spr:
    spravka = xlrd.open_workbook(f'Original/{i}', formatting_info=True)
    spravka_last = spravka.sheet_by_index(0)
    coordinate_1 = 0
    coordinate_2 = 0
    for row_num in range(spravka_last.nrows):
        row_line = spravka_last.row_values(row_num)
        for row_line_num in range(len(row_line)):
            if row_line[row_line_num] == 'Круглова О. А.':
                coordinate_1 = row_num
                coordinate_2 = row_line_num
    new_spravka = copy(spravka)
    new_spravka.get_sheet(0).set_copies_num(2)
    new_spravka.get_sheet(0).set_header_margin(20)
    new_spravka.get_sheet(0).set_print_scaling(77)
    new_spravka.get_sheet(0).write(4, 28, '', style1)
    new_spravka.get_sheet(0).write(4, 30, date_of_file, style1)
    new_spravka.get_sheet(0).write(coordinate_1, coordinate_2, signature_name, style2)
    new_spravka.save(f'{i}_new.xls')

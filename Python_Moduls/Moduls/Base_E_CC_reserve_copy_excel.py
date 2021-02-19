import xlrd
import xlwt
from xlutils.copy import copy
import datetime
from pymongo import MongoClient

NOW = datetime.datetime.today().date()


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


def reserve_copy(NOW):

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    style2 = set_style(xlwt.Alignment.HORZ_LEFT)

    blank_of_CC = xlrd.open_workbook(
        r'Z:\0_Helpful information\Info for Finance\Python_Moduls\Templates\blank_of_CC.xls', formatting_info=True)
    blank_CC_filled = copy(blank_of_CC)

    i = 1
    for employee in employees.find({}):
        blank_CC_filled.get_sheet(0).write(i, 0, employee['Табельный номер'], style2)
        blank_CC_filled.get_sheet(0).write(i, 1, employee['ФИО'], style2)
        blank_CC_filled.get_sheet(0).write(i, 2, employee['Банк'], style2)
        blank_CC_filled.get_sheet(0).write(i, 3, employee['Реквизиты'], style2)
        blank_CC_filled.get_sheet(0).write(i, 4, employee['Статус'], style2)
        if employee.get('Комментарий') is not None:
            blank_CC_filled.get_sheet(0).write(i, 5, employee['Комментарий'], style2)
        else:
            blank_CC_filled.get_sheet(0).write(i, 5, 'None', style2)
        blank_CC_filled.get_sheet(0).write(i, 6, employee['Login в системе'], style2)
        i += 1

    way = r'Z:\0_Helpful information\Info for Finance\VENDORS'
    blank_CC_filled.save(f'{way}\CC_reserved_copy_{NOW}.xls')
    print(r'Готово! Файл находится в папке Z:\0_Helpful information\Info for Finance\VENDORS')


if __name__ == '__mane__':
    # check
    reserve_copy(NOW)

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    for employee in employees.find({}):
        print(employee)


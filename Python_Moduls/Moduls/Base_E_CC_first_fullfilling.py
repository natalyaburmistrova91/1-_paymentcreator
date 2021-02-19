import xlrd
import datetime
from pymongo import MongoClient

NOW = datetime.datetime.today().date()


def first_download(NOW):
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    employee_file = xlrd.open_workbook('Z:/0_Helpful information/Info for Finance/VENDORS/CC_download.xls', formatting_info=True)
    employee_sheet = employee_file.sheet_by_index(0)

    calc = 0

    for row_num in range(1, employee_sheet.nrows):

        row_line = employee_sheet.row_values(row_num)
        employees.insert_one({'Табельный номер': int(row_line[0]),
                              'ФИО': row_line[1],
                              'Банк': row_line[3],
                              'Реквизиты': row_line[4],
                              'Статус': row_line[5],
                              'Комментарий': row_line[6],
                              'Login в системе': row_line[7],
                              'MD': 'N',
                              'Дата обновления': f'30/09/2020'})  # f'{NOW}'
        calc += 1
    print(f'Добавлено {calc} сотрудников из СС')

if __name__ == '__mane__':
    # check
    first_download(NOW)

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    for employee in employees.find({}):
        print(employee)
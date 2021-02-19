import xlrd
import datetime
from pymongo import MongoClient


NOW = datetime.datetime.today().date()


def update_actual(NOW):
    print('Требования! Файл должен называться acsour, формат - xls, в папке C:\python_working_files. \n'
          'Убедитесь, пожалуйста, что в файле от Acsour содержится информация в таком порядке: \n'
          '1-ая строка - шапка, 1-ый стобец - табельный номер, 2-ой столбец - ФИО сотрудника')
    answer = input('Все верно? Y/N ').upper()

    if answer == 'Y':

        # открываем базу
        client = MongoClient('localhost', 27017)
        db = client['EmployeeInfo']
        employees = db.emloyees

        # открываем файл Аксор
        employee_file = xlrd.open_workbook(r'C:\python_working_files\acsour.xls', formatting_info=True)
        employee_sheet = employee_file.sheet_by_index(0)

        # построчно по открытому файлу проверяем наличие сотрудника в базе по табельному номеру
        # если сотрудник есть - обновляем ФИО (вдруг что-то поменялось) и уведомляем пользователя и дату обновления ставим новую
        # если сотрудника нет - добавляем новый табельный, фио и ставим дату
        # ФИО вставляем красивое (отделенное и сепарируем под пробелом)
        for row_num in range(1, employee_sheet.nrows):

            row_line = employee_sheet.row_values(row_num)
            fio = ' '.join(row_line[1].split())
            if employees.find_one({'Табельный номер': int(row_line[0])}) is not None:
                # если нашелся
                employees.update_one({'Табельный номер': int(row_line[0])},
                                     {'$set': {'ФИО': fio, 'Дата обновления': f'{NOW}'}})
                # если не нашелся
            else:
                employees.insert_one({'Табельный номер': int(row_line[0]),
                                      'ФИО': fio,
                                      'Банк': 'None',
                                      'Реквизиты': 'None',
                                      'Статус': 'None',
                                      'MD': 'N',
                                      'Дата обновления': f'{NOW}',
                                      'Login в системе': 'None'}
                                     )
                print(f'Был добавлен {fio}')
        answer2 = input('Хотите узнать кого не нашли в списке Аксор? Y/N ').upper()
        if answer2 == 'Y':
            for employee in employees.find({'Дата обновления': {'$ne': f'{NOW}'}}):
                print(employee['ФИО'])
            answer3 = input('Удаляем? Y/N ').upper()
            if answer3 == 'Y':
                employees.delete_many({'Дата обновления': {'$ne': f'{NOW}'}})
                print('База обновлена!')
            else:
                print('Хорошо, мы ничего не удаляли!')
        else:
            print('Хорошо, но в базе могут остаться сотрудники, которые уже не работают в нашей компании.')
    else:
        print('База не обновлена.')




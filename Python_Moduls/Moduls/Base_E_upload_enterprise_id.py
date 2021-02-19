import xlrd
import datetime
from pymongo import MongoClient


def upload_enterprise_id():
    print('Требования! Файл должен называться Personal_Number_Enterprise_ID, формат - xls, в папке C:\python_working_files. \n'
          'Убедитесь, пожалуйста, что в файле содержится информация в таком порядке: \n'
          '1-ая строка - шапка, 1-ый стобец - табельный номер, 2-ой столбец - Enterprise id')
    answer = input('Все верно? Y/N ').upper()

    if answer == 'Y':

        # открываем базу
        client = MongoClient('localhost', 27017)
        db = client['EmployeeInfo']
        employees = db.emloyees

        # открываем файл Аксор
        enterprise_id_file = xlrd.open_workbook(r'C:\python_working_files\Personal_Number_Enterprise_ID.xls', formatting_info=True)
        enterprise_id_sheet = enterprise_id_file.sheet_by_index(0)

        # построчно по открытому файлу проверяем наличие сотрудника в базе по табельному номеру
        # если сотрудник есть - обновляем enterprise id (вдруг что-то поменялось) и уведомляем пользователя
        # если сотрудника нет - пишем "табельный номер" такого сотрудника нет в базе данных

        counting = 1

        for row_num in range(1, enterprise_id_sheet.nrows):



            row_line = enterprise_id_sheet.row_values(row_num)
            enterprise_id = row_line[1]
            if employees.find_one({'Табельный номер': int(row_line[0])}) is not None:
                # если нашелся
                employees.update_one({'Табельный номер': int(row_line[0])},
                                     {'$set': {'Login в системе': enterprise_id}})
                counting += 1
                # если не нашелся
            else:
                print(f'Сотрудника с табельным номером {row_line[0]} нет в базе данных')
        print(f'Обновили enterprise id у {counting} сотрудников ')
    else:
        print('База не обновлена.')




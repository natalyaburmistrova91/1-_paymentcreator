# Библиотеки
import xlrd
import random


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        b = inputting_value.split(',')
        result = float('.'.join(b))
    return result


LIST_DATA = []
RESULTS = []

# answer = input('Убедитесь, что файл data.xls лежит в текущей директории. Все верно? y/n ').upper()
answer = 'Y'
if answer == 'Y':
    data_file = xlrd.open_workbook('data.xls', formatting_info=True)
    data_sheet = data_file.sheet_by_index(0)
    for row_num in range(1, data_sheet.nrows):
        row_line = data_sheet.row_values(row_num)
        LIST_DATA.append(try_number(row_line[1]))
        if row_num == 1:
            target = try_number(row_line[2])
            tries_number = int(row_line[3])
    data_index = [i for i in range(len(LIST_DATA))]
    for i in range(tries_number):
        random.shuffle(data_index)
        less_finding_sum = 0
        more_finding_sum = 0
        index_in_data_index = 0
        while more_finding_sum <= target:
            less_finding_sum = more_finding_sum
            more_finding_sum += LIST_DATA[data_index[index_in_data_index]]
            index_in_data_index += 1
            if more_finding_sum >= target:
                RESULTS.append([abs(target - less_finding_sum), less_finding_sum, sorted(data_index[:index_in_data_index-1])])
                RESULTS.append([abs(target - more_finding_sum), more_finding_sum, sorted(data_index[:index_in_data_index])])
    print(sorted(RESULTS)[0])


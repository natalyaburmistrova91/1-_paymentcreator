import datetime


NOW = datetime.datetime.today().date()


def payment_creator(list_of_employees, total_amount, vo=''):
    num_of_payment = input('Введите номер платежа: ')
    year = NOW.year % 2000
    number_of_payment = f'{NOW.day:02d}{NOW.month:02d}{year:02d}{num_of_payment}'
    f_2 = open(f'C:\import\{number_of_payment}_payment.txt', 'w', encoding="utf-8")
    f_2.write(f'0700986063#RUR#{NOW.day:02d}/{NOW.month:02d}/{year}#{number_of_payment}#{total_amount:.2f}\n')
    for e in list_of_employees:
        f_2.write(f'{e[2]}{e[1]:.2f}\n')
    f_2.close()
    f_3 = open(f'C:\import\{number_of_payment}_admin_message.txt', 'w', encoding="utf-8")
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
    f_6 = open(f'C:\import\{date_of_file}_other_banks_download.txt', 'w', encoding="utf-8")
    number = int(input('Введите стартовое значение для нумерации прочих платежей: '))
    for e in list_of_all_payment_other:
        bank_line_list = list(e[2])
        bank_line_list.insert(8, f'{NOW.year}{NOW.month:02d}{NOW.day:02d}')
        bank_line_list.insert(20, f'{e[1]:.2f}')
        bank_line_list.insert(45, f'{number:05d}')
        bank_line_actual = ''.join(bank_line_list)
        f_6.write(f'{bank_line_actual}\n')
        number += 1
    f_6.close()
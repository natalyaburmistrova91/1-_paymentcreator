import datetime


NOW = datetime.datetime.today().date()


def electronic_bank_statement_creator(list_of_all_payment_1c, user_name):
    f_5 = open(
        f'Z:/0_Helpful information/Info for Finance/Bank_statements/{user_name}_{NOW.day:02d}-{NOW.month:02d}-{NOW.year:02d}_bank_statement_el.txt',
        'w', encoding="ANSI")
    f_5.write(f'1CClientBankExchange\n'
              f'ВерсияФормата=1.02\n'
              f'Кодировка=Windows\n'
              f'Отправитель=CitiDirect\n'
              f'Получатель=1С:Предприятие\n'
              f'ДатаСоздания=10.01.2020\n'
              f'ВремяСоздания=10:29:51\n'
              f'ДатаНачала={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'ДатаКонца={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'РасчСчет=40702810100700986063\n'
              f'\n'
              f'СекцияРасчСчет\n'
              f'ДатаНачала={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'ДатаКонца={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
              f'РасчСчет=40702810100700986063\n'
              f'НачальныйОстаток=0.00\n'
              f'ВсегоПоступило=0.00\n'
              f'ВсегоСписано=0.00\n'
              f'КонечныйОстаток=0.00\n'
              f'КонецРасчСчет\n'
              f'\n')
    for e in list_of_all_payment_1c:
        f_5.write(f'СекцияДокумент=Банковский ордер\n'
                  f'Номер={e[5]}\n'
                  f'Дата={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
                  f'Сумма={e[4]:.2f}\n'
                  f'ПлательщикСчет=40702810100700986063\n'
                  f'ДатаСписано={NOW.day:02d}.{NOW.month:02d}.{NOW.year}\n'
                  f'Плательщик1=\n'
                  f'ПлательщикРасчСчет=40702810100700986063\n'
                  f'ПлательщикБанк1=\n'
                  f'ПлательщикБанк2=\n'
                  f'ПлательщикБИК=\n'
                  f'ПолучательИНН={e[0]}\n'
                  f'Получатель1={e[1]}\n'
                  f'Получатель2=\n'
                  f'Получатель3=\n'
                  f'Получатель4=\n'
                  f'ПолучательБанк1=\n'
                  f'ПолучательБанк2=\n'
                  f'ПолучательБИК=\n'
                  f'ВидПлатежа=Электронно\n'
                  f'ВидОплаты=\n'
                  f'Код=\n'
                  f'СтатусСоставителя=\n'
                  f'ПлательщикКПП=\n'
                  f'ПолучательКПП=\n'
                  f'ПоказательКБК=\n'
                  f'ОКАТО=\n'
                  f'ПоказательОснования=\n'
                  f'ПоказательПериода=\n'
                  f'ПоказательНомера=\n'
                  f'ПоказательДаты=\n'
                  f'ПоказательТипа=\n'
                  f'Очередность=05\n'
                  f'НазначениеПлатежа={e[2]} {e[3]}\n'
                  f'\n'
                  f'КонецДокумента\n'
                  f'\n')
    f_5.write(f'КонецФайла\n')
    f_5.close()
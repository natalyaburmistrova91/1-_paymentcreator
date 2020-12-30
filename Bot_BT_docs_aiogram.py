from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN


Dict = {}
first_action = ['Узнать список \U0001F4DD', 'Закончить диалог \U0001F3C3']
officies = ['Москва', 'Тверь', 'Ростов-на-Дону', 'Закончить диалог \U0001F3C3']
contries = ['Россия \U0001F1F7', 'Зарубеж \U0001F310', 'Россия \U0001F1F7 + Зарубеж \U0001F310',
            'Закончить диалог \U0001F3C3']
transports = ['1. Самолёт \U00002708', '2. Авто (личный/общественный/такси)', '3. Поезд \U0001F684',
             '4. Самолёт \U00002708 + авто (личный/общественный/такси)',
             '5. Поезд \U0001F684 + авто (личный/общественный/такси)', 'Закончить диалог \U0001F3C3']
boarding_pass_status = ['Да, есть \U0001F6C2', 'Нет или не все \U0001FA82', 'Закончить диалог \U0001F3C3']
boarding_pass_status_for_1 = ['Да, есть \U0001F6C2', 'Нет \U0001FA82', 'Закончить диалог \U0001F3C3']
boarding_pass_statuses = ['Да, есть \U0001F6C2', 'Нет или не все \U0001FA82', 'Нет \U0001FA82', 'Закончить диалог \U0001F3C3']
flight_statuses = ['Да, хочу дополнительный день/дни', 'Нет, раннего вылета/позднего прилета не было', 'Закончить диалог \U0001F3C3']
ticker_purcase_status = ['Да, самостоятельно \U0001F4B8', 'Нет', 'Закончить диалог \U0001F3C3']
hotel_status = ['Да, в отеле \U0001F3E8', 'Нет \U0001F3E1', 'Закончить диалог \U0001F3C3']
time_statuses = ['Вариант 1 \U0001F556', 'Вариант 2 \U0001F550', 'Нет раннего выезда, позднего приезда',
               'Закончить диалог \U0001F3C3']
hotel_docs = ['Ориг. счет и чек \U0001F34E', 'Копия счета и ориг. выписка из банка \U0001F34F',
              'Ориг. подтв. прож-ия из отеля \U0001F351', 'Справка от CWT \U0001F352', 'Закончить диалог \U0001F3C3']
trasport_statuses = ['Да, одинаковый', 'Нет, разный', 'Закончить диалог \U0001F3C3']


def text_print(dict_text_durty):
    dict_text = list(set(dict_text_durty))
    str_dict = f' - {dict_text[0]}'
    if len(dict_text) > 1:
        for i in range(1, len(dict_text)):
            str_dict += f',\n - {dict_text[i]}'
    return str_dict


def myte_print(dict_text):
    keys = dict_text.keys()
    text = ''
    number = 1
    for key in keys:
        docs_list_pure = list(set(dict_text[key]))
        docs = f'{docs_list_pure[0]}'
        if len(docs_list_pure) > 1:
            for i in range(1, len(docs_list_pure)):
                docs += f', {docs_list_pure[i]}'
        text += f' {number}) {key}\n приложить: {docs}\n'
        number += 1
    text += f'P.S. \n* - если расходы были'
    return text



bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class DocsStep(StatesGroup):
    waiting_for_office = State()
    waiting_for_country = State()
    waiting_for_transport = State()
    waiting_for_transport_spec = State()
    waiting_for_boarding_passes = State()
    waiting_for_train_ticket = State()
    waiting_for_air_payment = State()
    waiting_for_air_time = State()
    waiting_for_hotel = State()
    waiting_for_hotel_docs = State()
    waiting_for_flight_status = State()
    other_state = State()
    waiting_for_transport_change = State()


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
    Dict[message.from_user.id] = {'документы': [], 'тип расходов': {}, 'офис': []}
    keyboard_1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for action in first_action:
        keyboard_1.add(types.KeyboardButton(action))
    question = f"Добрый день \U0001F305\nя помогу вам узнать список документов по командировке , " \
               f"которые нужно сдать в финансовый отдел, а также какие расходы нужно отразить в MyTE и что " \
               f"приложить к ним. \n\nБудет не более 9 вопросов \U00002753." \
               f"\n\nЕсли вы ошиблись в выборе - закончите, пожалуйста, диалог и начните заново." \
               f"\n\nP.S. Если вы не видите варианты ответов под диалоговым окном - закройте клавиатуру."
    await DocsStep.waiting_for_office.set()
    await message.answer(question, reply_markup=keyboard_1)


@dp.message_handler(state=DocsStep.waiting_for_office)
async def get_office(message: types.Message, state: FSMContext):
    if message.text not in first_action:
        await message.reply('Пожалуйста, выберете действие из списка под клавиатурой.')
        return
    await state.update_data(start_choice=message.text)
    if message.text == "Узнать список \U0001F4DD":
        keyboard_1_1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for office in officies:
            keyboard_1_1.add(types.KeyboardButton(office))
        question_1 = f"К какому офису вы относитесь?"
        await message.answer(question_1, reply_markup=keyboard_1_1)
        await DocsStep.waiting_for_country.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_country)
async def get_country(message: types.Message, state: FSMContext):
    await state.update_data(office=message.text)
    if message.text not in officies:
        await message.reply('Пожалуйста, выберете офис из списка клавиатуры.')
        return
    if message.text == "Москва" or message.text == 'Тверь' or message.text == 'Ростов-на-Дону':
        if message.text == "Москва":
            Dict[message.from_user.id]['офис'] = ['Москва', 'Москвы', '23:20', '00:40']
        elif message.text == 'Тверь':
            Dict[message.from_user.id]['офис'] = ['Тверь', 'Москвы', '22:00', '02:00']
        elif message.text == 'Ростов-на-Дону':
            Dict[message.from_user.id]['офис'] = ['Ростов-на-Дону', 'Ростова-на-Дону', '23:20', '00:40']
        keyboard_2 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        for country in contries:
            keyboard_2.add(types.KeyboardButton(country))
        question_2 = f"\n\nВы были в командировке:"
        await message.answer(question_2, reply_markup=keyboard_2)
        await DocsStep.waiting_for_transport.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_transport)
async def get_transport(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    if message.text not in contries:
        await message.reply('Пожалуйста, выберете страны из списка под клавиатурой.')
        return
    if message.text == "Зарубеж \U0001F310" or message.text == 'Россия \U0001F1F7 + Зарубеж \U0001F310' or \
            message.text == "Россия \U0001F1F7":
        if message.text == "Россия \U0001F1F7":
            Dict[message.from_user.id]['документы'].append('копия подписанного приказа/-ов на командировку')
            if Dict[message.from_user.id]['тип расходов'].get('суточные') is None:
                Dict[message.from_user.id]['тип расходов']['суточные'] = []
            Dict[message.from_user.id]['тип расходов']['суточные'].append('скан подписанного приказа/ов на командировку')
        elif message.text == "Зарубеж \U0001F310" or message.text == 'Россия \U0001F1F7 + Зарубеж \U0001F310':
            Dict[message.from_user.id]['документы'].append('копия подписанного приказа/-ов на командировку, '
                                                           '\n -цветной скан заграничного паспорта (виза + 4 штампа '
                                                           '(2 российских + 2 зарубежных))')
            if Dict[message.from_user.id]['тип расходов'].get('суточные') is None:
                Dict[message.from_user.id]['тип расходов']['суточные'] = []
            Dict[message.from_user.id]['тип расходов']['суточные'].append('скан подписанного приказа/-ов на командировку, '
                                                           'цветной скан заграничного паспорта (виза + 4 штампа '
                                                           '(2 российских + 2 зарубежных))')

        keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for trasport_status in trasport_statuses:
            keyboard_3.add(types.KeyboardButton(trasport_status))
        question_3_1 = f"\n\U00002757ВНИМАНИЕ!\U00002757\nЕсли у вас были расходы, понесенные в валюте, вы можете " \
                       f"предоставить/приложить в MyTE выписку из банка с эквивалентом в рублях и получить возмещение " \
                       f"в рублях\n\n"
        question_3_2 = f"До места командирования и обратно вы использовали одинаковый вид траспорта?"
        if message.text == "Зарубеж \U0001F310" or message.text == 'Россия \U0001F1F7 + Зарубеж \U0001F310':
            await message.answer(question_3_1+question_3_2, reply_markup=keyboard_3)
        else:
            await message.answer(question_3_2, reply_markup=keyboard_3)
        await DocsStep.waiting_for_transport_change.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_transport_change)
async def get_transport(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    if message.text not in trasport_statuses:
        await message.reply('Пожалуйста, выберете транспорт из списка под клавиатурой.')
    if message.text == "Да, одинаковый":
        Dict[message.from_user.id]['транспорт'] = 0
        keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for transport in transports:
            keyboard_3.add(types.KeyboardButton(transport))
        question_3 = f"До места командирования и обратно вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                     f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                     f"отличается от города в приказе."
        await message.answer(question_3, reply_markup=keyboard_3)
        await DocsStep.waiting_for_transport_spec.set()
    elif message.text == "Нет, разный":
        Dict[message.from_user.id]['транспорт'] = 1
        keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for transport in transports:
            keyboard_3.add(types.KeyboardButton(transport))
        question_3 = f"До места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                     f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                     f"отличается от города в приказе."
        await message.answer(question_3, reply_markup=keyboard_3)
        await DocsStep.waiting_for_transport_spec.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_transport_spec)
async def get_transport_spec(message: types.Message, state: FSMContext):
    await state.update_data(transport=message.text)
    if message.text not in transports:
        await message.reply('Пожалуйста, выберете транспорт из списка под клавиатурой.')
        return
    if message.text == "1. Самолёт \U00002708" or message.text == '4. Самолёт \U00002708 + авто (личный/общественный/такси)':
        if message.text == '4. Самолёт \U00002708 + авто (личный/общественный/такси)':
            Dict[message.from_user.id]['документы'].append(
                'служебная записка о проезде на авто (форму запросить у финансового отдела)')
            Dict[message.from_user.id]['тип расходов']['суточные'].append(
                'служебная записка о проезде на авто (форму запросить у финансового отдела)')
        keyboard_4 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
            for status_bp_1 in boarding_pass_status_for_1:
                keyboard_4.add(types.KeyboardButton(status_bp_1))
        else:
            for status_bp in boarding_pass_status:
                keyboard_4.add(types.KeyboardButton(status_bp))
        question_4 = f"Необходимо предоставить оригинальные посадочные талоны \U0001F3AB.\nОни у вас есть? "
        if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
            question_4 = f"Необходимо предоставить оригинальный посадочный талон \U0001F3AB.\nОн у вас есть? "
        await message.answer(question_4, reply_markup=keyboard_4)
        await DocsStep.waiting_for_boarding_passes.set()
    elif message.text == '3. Поезд \U0001F684' or message.text == '5. Поезд \U0001F684 + авто (личный/общественный/такси)':
        if message.text == '5. Поезд \U0001F684 + авто (личный/общественный/такси)':
            Dict[message.from_user.id]['документы'].append(
                'служебная записка о проезде на авто (форму запросить у финансового отдела)')
            Dict[message.from_user.id]['тип расходов']['суточные'].append(
                'служебная записка о проезде на авто (форму запросить у финансового отдела)')
        keyboard_11 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        for purcase_status in ticker_purcase_status:
            keyboard_11.add(types.KeyboardButton(purcase_status))
        question_11 = f"ЖД билеты куплены самостоятельно?\n(самостоятельная покупка не желательна по политикам компании)"
        if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
            question_11 = f"ЖД билет куплен самостоятельно?\n(самостоятельная покупка не желательна по политикам компании)"
        await message.answer(question_11, reply_markup=keyboard_11)
        await DocsStep.waiting_for_train_ticket.set()
    elif message.text == '2. Авто (личный/общественный/такси)':
        Dict[message.from_user.id]['документы'].append(
            'служебная записка о проезде на авто (форму запросить у финансового отдела)')
        Dict[message.from_user.id]['тип расходов']['суточные'].append(
            'служебная записка о проезде на авто (форму запросить у финансового отдела)')
        if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
            question_12 = f"\n\nВы проживали в отеле? \U0001F3F0"
            keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
            for hotel_payment in hotel_status:
                keyboard_12.add(types.KeyboardButton(hotel_payment))
            await message.answer(question_12, reply_markup=keyboard_12)
            await DocsStep.waiting_for_hotel.set()
        else:
            Dict[message.from_user.id]['транспорт'] += 1
            keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for transport in transports:
                keyboard_3.add(types.KeyboardButton(transport))
            question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                     f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                     f"отличается от города в приказе."
            await message.answer(question_3, reply_markup=keyboard_3)
            await DocsStep.waiting_for_transport_spec.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_boarding_passes)
async def get_boarding_passes(message: types.Message, state: FSMContext):
    await state.update_data(boarding_pass_status=message.text)
    if message.text not in boarding_pass_statuses:
        await message.reply('Пожалуйста, выберете вариант наличия посадочных из списка под клавиатурой.')
        return
    if message.text == 'Да, есть \U0001F6C2' or message.text == 'Нет или не все \U0001FA82' or message.text == 'Нет \U0001FA82':
        if message.text == 'Да, есть \U0001F6C2':
            if Dict[message.from_user.id]['транспорт'] == 1:
                Dict[message.from_user.id]['документы'].append('оригинал посадочного талона (туда)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                        'посадочный талон(туда)')
            elif Dict[message.from_user.id]['транспорт'] == 2:
                Dict[message.from_user.id]['документы'].append('оригинал посадочного талона (обратно)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                            'посадочный талон(обратно)')
            else:
                Dict[message.from_user.id]['документы'].append('оригиналы посадочных талонов')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                            'посадочные талоны')
        elif message.text == 'Нет или не все \U0001FA82' or message.text == 'Нет \U0001FA82':
            if Dict[message.from_user.id]['транспорт'] == 1:
                Dict[message.from_user.id]['документы'].append('оригинальная справка от авиаперевозчика (вместо '
                                                                           'посадочного талона) (туда)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                                'справка от авиаперевозчика (вместо посадочного талона)(туда)')
            elif Dict[message.from_user.id]['транспорт'] == 2:
                Dict[message.from_user.id]['документы'].append('оригинальная справка от авиаперевозчика (вместо '
                                                                           'посадочного талона) (обратно)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                                'справка от авиаперевозчика (вместо посадочного талона)(обратно)')
            else:
                Dict[message.from_user.id]['документы'].append('оригинальная справка от авиаперевозчика (вместо '
                                                                           'посадочных талонов)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                                'справка от авиаперевозчика (вместо посадочных талонов)')
        keyboard_5 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        for purcase_status in ticker_purcase_status:
            keyboard_5.add(types.KeyboardButton(purcase_status))
        question_5 = f"Авиабилеты куплены самостоятельно?\n(самостоятельная покупка не желательна по политикам компании)"
        if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
            question_5 = f"Авиабилет куплен самостоятельно?\n(самостоятельная покупка не желательна по политикам компании)"
        await message.answer(question_5, reply_markup=keyboard_5)
        await DocsStep.waiting_for_air_payment.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_air_payment)
async def get_air_payment(message: types.Message, state: FSMContext):
    await state.update_data(air_payment=message.text)
    if message.text not in ticker_purcase_status:
        await message.reply('Пожалуйста, выберете вариант из списка под клавиатурой.')
        return
    if message.text == 'Да, самостоятельно \U0001F4B8' or message.text == 'Нет':
        keyboard_6 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        for flight_status in flight_statuses:
            keyboard_6.add(types.KeyboardButton(flight_status))
        question_6_1 = f"\U00002757ВНИМАНИЕ!\U00002757  \nПри самостоятельной покупке жд или авиабилетов сотрудники " \
                       f"финансового отдела будут обязаны уведомить об этом Travel отдел."
        question_6_2 = f'\n\nУ Вас был ранний выезд/приезд в/из аэропорта и вы хотели бы дополнительный день суточных?'

        if message.text == 'Да, самостоятельно \U0001F4B8':
            if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
                if Dict[message.from_user.id]['транспорт'] == 1:
                    Dict[message.from_user.id]['документы'].append('маршрутная квитанция электронного авиабилета (туда), '
                                                                   '\n -оригинальная выписка из банка на покупку авиабилета (туда)')
                else:
                    Dict[message.from_user.id]['документы'].append('маршрутная квитанция электронного авиабилета (обратно), '
                                                                   '\n -оригинальная выписка из банка на покупку авиабилета (обратно)')
                if Dict[message.from_user.id]['тип расходов'].get('расход на авиабилет') is None:
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'] = []
                if Dict[message.from_user.id]['транспорт'] == 1:
                    Dict[message.from_user.id]['тип расходов']['суточные'].append(
                        'электронный билет на самолёт (туда)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append('маршрутная квитанция электронного'
                                                                                             ' авиабилета (туда)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                        'выписка из банка на покупку авиабилета (туда)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                        'посадочный талон (туда)')
                else:
                    Dict[message.from_user.id]['тип расходов']['суточные'].append(
                        'электронный билет на самолёт (обратно)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append('маршрутная квитанция электронного'
                                                                                             ' авиабилета (обратно)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                        'выписка из банка на покупку авиабилета (обратно)')
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                        'посадочный талон (обратно)')
            else:
                Dict[message.from_user.id]['документы'].append('маршрутная квитанция электронных авиабилетов, '
                                                               '\n -оригинальная выписка из банка на покупку авиабилетов')
                if Dict[message.from_user.id]['тип расходов'].get('расход на авиабилет') is None:
                    Dict[message.from_user.id]['тип расходов']['расход на авиабилет'] = []
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронные билеты на самолёт')
                Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                    'маршрутная квитанция электронных'
                    ' авиабилетов')
                Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                    'выписка из банка на покупку авиабилетов')
                Dict[message.from_user.id]['тип расходов']['расход на авиабилет'].append(
                    'посадочные талоны')
            await message.answer(question_6_1 + question_6_2, reply_markup=keyboard_6)
            await DocsStep.waiting_for_flight_status.set()
        elif message.text == 'Нет':
            if Dict[message.from_user.id]['транспорт'] == 1 or Dict[message.from_user.id]['транспорт'] == 2:
                if Dict[message.from_user.id]['транспорт'] == 1:
                    Dict[message.from_user.id]['документы'].append('электронный билет CWT (туда)')
                    Dict[message.from_user.id]['тип расходов']['суточные'].append(
                        'электронный билет CWT (туда)')
                else:
                    Dict[message.from_user.id]['документы'].append('электронный билет CWT (обратно)')
                    Dict[message.from_user.id]['тип расходов']['суточные'].append(
                        'электронный билет CWT (обратно)')
            else:
                Dict[message.from_user.id]['документы'].append('электронные билеты CWT')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронные билеты CWT')
            await message.answer(question_6_2, reply_markup=keyboard_6)
            await DocsStep.waiting_for_flight_status.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_flight_status)
async def get_flight_time_payment(message: types.Message, state: FSMContext):
    if message.text not in flight_statuses:
        await message.reply('Пожалуйста, выберете вариант по раннему вылету/позднему прилету из списка под клавиатурой.')
        return
    if message.text == 'Да, хочу дополнительный день/дни':
        question_22 = f"\n\nВыберите ваш вариант : \n\nВариант 1. \U0001F556 \nУ вас по билетам вылет из аэропорта " \
                       f"{Dict[message.from_user.id]['офис'][1]} ранее {Dict[message.from_user.id]['офис'][3]}/ " \
                       f"прилет позднее {Dict[message.from_user.id]['офис'][2]}\nВариант 2. \U0001F550 \nУ вас ранний" \
                       f" приезд в аэропорт/позднее возвращение домой, но по билетам вылет из аэропорта " \
                       f"{Dict[message.from_user.id]['офис'][1]} позднее {Dict[message.from_user.id]['офис'][3]}/ " \
                       f"прилет ранее {Dict[message.from_user.id]['офис'][2]}, но вы хотели бы дополнительный день " \
                       f"суточных \n3. Ничего из вышеперечисленного \U0001F31E \n4. Закончить диалог \U0001F3C3"
        keyboard_22 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
        for time_status in time_statuses:
            keyboard_22.add(types.KeyboardButton(time_status))
        await message.answer(question_22, reply_markup=keyboard_22)
        await DocsStep.waiting_for_air_time.set()
    elif message.text == 'Нет, раннего вылета/позднего прилета не было':
        if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
            question_12 = f"\n\nВы проживали в отеле? \U0001F3F0"
            keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
            for hotel_payment in hotel_status:
                keyboard_12.add(types.KeyboardButton(hotel_payment))
            await message.answer(question_12, reply_markup=keyboard_12)
            await DocsStep.waiting_for_hotel.set()
        else:
            Dict[message.from_user.id]['транспорт'] += 1
            keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for transport in transports:
                keyboard_3.add(types.KeyboardButton(transport))
            question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                         f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                         f"отличается от города в приказе."
            await message.answer(question_3, reply_markup=keyboard_3)
            await DocsStep.waiting_for_transport_spec.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_air_time)
async def get_air_time(message: types.Message, state: FSMContext):
    await state.update_data(air_time=message.text)
    if message.text not in time_statuses:
        await message.reply('Пожалуйста, выберете вариант по выезду/приезду из аэропорта из списка под клавиатурой.')
        return
    if message.text == 'Вариант 1 \U0001F556' or message.text == 'Вариант 2 \U0001F550' or message.text == \
            'Нет раннего выезда, позднего приезда':
        question_7_1 = f"\U00002757ВНИМАНИЕ!\U00002757 \nПри составлении приказа на командировку учитывается время до " \
                       f"аэропорта и из аэропорта \U0001F3C1. \nПриказ должен быть оформлен на даты, включая день " \
                       f"выезда/приезда домой. \U0001F4C6 \nМожно сделать приказ на изменение/продление."
        question_7_2 = f"\U00002757ВНИМАНИЕ!\U00002757 \nСроки приказа на командировку должны включать этот " \
                       f"дополнительный день, а также у вас должно быть подтверждение раннего выезда/позднего приезда " \
                       f"(квитанция на такси, в которой видно дату и время \U0001F004)."
        question_7_3 = f"\n\nВы проживали в отеле? \U0001F3F0"

        if message.text == 'Вариант 1 \U0001F556':

            if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
                keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
                for hotel_payment in hotel_status:
                    keyboard_12.add(types.KeyboardButton(hotel_payment))
                await message.answer(question_7_1 + question_7_3, reply_markup=keyboard_12)
                await DocsStep.waiting_for_hotel.set()
            else:
                Dict[message.from_user.id]['транспорт'] += 1
                keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                for transport in transports:
                    keyboard_3.add(types.KeyboardButton(transport))
                question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                             f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                             f"отличается от города в приказе."
                await message.answer(question_3, reply_markup=keyboard_3)
                await DocsStep.waiting_for_transport_spec.set()
        elif message.text == 'Вариант 2 \U0001F550':
            if Dict[message.from_user.id]['транспорт'] == 0:
                Dict[message.from_user.id]['документы'].append(
                    'заявление на ранний выезд/поздний приезд из аэропорта (форму '
                    'запросить у сотрудника финансового отдела), \n - подтверждение '
                    'раннего выезда/позднего приезда (квитанция на такси)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'заявление на ранний выезд/поздний приезд из аэропорта (форму '
                    'запросить у сотрудника финансового отдела)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'подтверждение раннего выезда/позднего приезда (квитанция на такси)')
            elif Dict[message.from_user.id]['транспорт'] == 1:
                Dict[message.from_user.id]['документы'].append(
                    'заявление на ранний выезд в аэропорт (форму '
                    'запросить у сотрудника финансового отдела), \n - подтверждение '
                    'раннего выезда в аэропорт (квитанция на такси)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'заявление на ранний выезд в аэропорт (форму '
                    'запросить у сотрудника финансового отдела)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'подтверждение раннего выезда в аэропорт (квитанция на такси)')
            else:
                Dict[message.from_user.id]['документы'].append(
                    'заявление на поздний приезд из аэропорта (форму '
                    'запросить у сотрудника финансового отдела), \n - подтверждение '
                    'позднего приезда из аэропорта (квитанция на такси)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'заявление на поздний приезд из аэропорта (форму '
                    'запросить у сотрудника финансового отдела)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'подтверждение позднего приезда из аэропорта (квитанция на такси)')

            if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
                keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
                for hotel_payment in hotel_status:
                    keyboard_12.add(types.KeyboardButton(hotel_payment))
                await message.answer(question_7_2 + question_7_3, reply_markup=keyboard_12)
                await DocsStep.waiting_for_hotel.set()
            else:
                Dict[message.from_user.id]['транспорт'] += 1
                keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                for transport in transports:
                    keyboard_3.add(types.KeyboardButton(transport))
                question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                             f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                             f"отличается от города в приказе."
                await message.answer(question_3, reply_markup=keyboard_3)
                await DocsStep.waiting_for_transport_spec.set()

        elif message.text == 'Нет раннего выезда, позднего приезда':
            if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
                keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
                for hotel_payment in hotel_status:
                    keyboard_12.add(types.KeyboardButton(hotel_payment))
                await message.answer(question_7_3, reply_markup=keyboard_12)
                await DocsStep.waiting_for_hotel.set()
            else:
                Dict[message.from_user.id]['транспорт'] += 1
                keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                for transport in transports:
                    keyboard_3.add(types.KeyboardButton(transport))
                question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                             f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                             f"отличается от города в приказе."
                await message.answer(question_3, reply_markup=keyboard_3)
                await DocsStep.waiting_for_transport_spec.set()
        elif message.text == "Закончить диалог \U0001F3C3":
            await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
            if message.from_user.id in Dict:
                del Dict[message.from_user.id]
            await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_train_ticket)
async def get_boarding_passes(message: types.Message, state: FSMContext):
    await state.update_data(ticket_payment=message.text)
    if message.text not in ticker_purcase_status:
        await message.reply('Пожалуйста, выберете вариант из списка под клавиатурой.')
        return
    if message.text == 'Да, самостоятельно \U0001F4B8' or message.text == 'Нет':
        if message.text == 'Да, самостоятельно \U0001F4B8':
            if Dict[message.from_user.id]['тип расходов'].get('расход на жд') is None:
                Dict[message.from_user.id]['тип расходов']['расход на жд'] = []
            if Dict[message.from_user.id]['транспорт'] == 0:

                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронные жд билеты/оригинальные жд билеты')
                Dict[message.from_user.id]['документы'].append('электронные жд билеты/оригинальные жд билеты'
                                                               '\n- оригинальная выписка из банка на покупку жд билетов')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append('электронные жд билеты/'
                                                                                  'оригинальные жд билеты')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append(
                    'выписка из банка на покупку жд билетов')
            elif Dict[message.from_user.id]['транспорт'] == 1:
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронный жд билет/оригинальный жд билет (туда)')
                Dict[message.from_user.id]['документы'].append('электронный жд билет/оригинальный жд билет (туда)'
                                                               '\n- оригинальная выписка из банка на покупку жд билета (туда)')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append('электронный жд билет/'
                                                                                  'оригинальный жд билет (туда)')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append(
                    'выписка из банка на покупку жд билета (туда)')
            else:
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронный жд билет/оригинальный жд билет (обратно)')
                Dict[message.from_user.id]['документы'].append('электронный жд билет/оригинальный жд билет (обратно)'
                                                               '\n- оригинальная выписка из банка на покупку жд билета (обратно)')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append('электронный жд билет/'
                                                                                  'оригинальный жд билет (обратно)')
                Dict[message.from_user.id]['тип расходов']['расход на жд'].append(
                    'выписка из банка на покупку жд билета (обратно)')
        elif message.text == 'Нет':
            if Dict[message.from_user.id]['транспорт'] == 0:
                Dict[message.from_user.id]['документы'].append('электронные жд билеты/оригинальные жд билеты')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронные жд билеты/оригинальные жд билеты')
            elif Dict[message.from_user.id]['транспорт'] == 1:
                Dict[message.from_user.id]['документы'].append('электронный жд билет/оригинальный жд билет (туда)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append(
                    'электронный жд билет/оригинальный жд билет (туда)')
            else:
                Dict[message.from_user.id]['документы'].append('электронный жд билет/оригинальный жд билет (обратно)')
                Dict[message.from_user.id]['тип расходов']['суточные'].append('электронный жд билет/оригинальный жд билет (обратно)')
        question_11_1 = f"\n\nВы проживали в отеле? \U0001F3F0"
        question_11_2 = f"\U00002757ВНИМАНИЕ!\U00002757  \nПри самостоятельной покупке жд или авиабилетов сотрудники " \
                        f"финансового отдела будут обязаны уведомить об этом Travel отдел."
        if Dict[message.from_user.id]['транспорт'] == 0 or Dict[message.from_user.id]['транспорт'] == 2:
            keyboard_12 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # клавиатура
            for hotel_payment in hotel_status:
                keyboard_12.add(types.KeyboardButton(hotel_payment))
            if message.text == 'Да, самостоятельно \U0001F4B8':
                await message.answer(question_11_2 + question_11_1, reply_markup=keyboard_12)
            else:
                await message.answer(question_11_1, reply_markup=keyboard_12)
            await DocsStep.waiting_for_hotel.set()
        else:
            Dict[message.from_user.id]['транспорт'] += 1
            keyboard_3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for transport in transports:
                keyboard_3.add(types.KeyboardButton(transport))
            question_3 = f"Из места командирования вы добирались на: \n\n\U00002757ВНИМАНИЕ!\U00002757 " \
                         f"\nПункты 4 и 5 вы выбираете только если в билетах на поезд/самолет город назначения " \
                         f"отличается от города в приказе."
            if message.text == 'Да, самостоятельно \U0001F4B8':
                await message.answer(question_11_2 + question_3, reply_markup=keyboard_3)
            else:
                await message.answer(question_3, reply_markup=keyboard_3)
            await DocsStep.waiting_for_transport_spec.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_hotel)
async def get_hotel(message: types.Message, state: FSMContext):
    await state.update_data(step=message.text)
    if message.text not in hotel_status:
        await message.reply('Пожалуйста, выберете вариант из списка под клавиатурой.')
        return
    if message.text == 'Да, в отеле \U0001F3E8':
        keyboard_8 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)# клавиатура
        for hotel_doc in hotel_docs:
            keyboard_8.add(types.KeyboardButton(hotel_doc))
        question_8 = f"Последний вопрос \U00002705 и он про отель. Выберите 1 из 4 вариантов (1,2 - при " \
                     f"самостоятельной оплате). У меня есть:"
        await message.answer(question_8, reply_markup=keyboard_8)
        await DocsStep.waiting_for_hotel_docs.set()
    elif message.text == 'Нет \U0001F3E1':
        Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'] = []
        Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'].append('квитанция/чек'
                                                                                                    '/выписка из банка, '
                                                                                                    'маршрут')
        Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'] = []
        Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'].append('подтверждение '
                                                                                                    'оплаты и '
                                                                                                    'детализация')
        await message.answer(f"Список документов, который нужно предоставить в финансовый отдел "
                                               f"\U0001F463:\n\n{text_print(Dict[message.from_user.id]['документы'])}"
                                               f"\n\n\U00002757Внимание!\U00002757 \n\nНе забудь:"
                                               f"\n\n1. Самостоятельно сделать сканы всех документов до передачи в "
                                               f"финансовый отдел (для отражения расходов в MyTE) \U0001F4F8"
                                               f"\n2. Сдать оригинал приказа/-ов и согласие на вылет (если было) в HR "
                                               f"\U0001F64C"
                                               f"\n3. Отразить в MyTE следующие расходы: "
                                               f"\n{myte_print(Dict[message.from_user.id]['тип расходов'])}"
                                               f"\n\n Чтобы повторить, напиши /start \U0001F447")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(state=DocsStep.waiting_for_hotel_docs)
async def get_hotel_docs(message: types.Message, state: FSMContext):
    await state.update_data(hotel_docs=message.text)
    if message.text not in hotel_docs:
        await message.reply('Пожалуйста, выберете вариант из списка под клавиатурой.')
        return
    if message.text == 'Ориг. счет и чек \U0001F34E' \
            or message.text == 'Копия счета и ориг. выписка из банка \U0001F34F' \
            or message.text == 'Ориг. подтв. прож-ия из отеля \U0001F351' \
            or message.text == 'Справка от CWT \U0001F352':
        if message.text == 'Ориг. счет и чек \U0001F34E':
            Dict[message.from_user.id]['документы'].append('оригинальные счет и чек из отеля')
            Dict[message.from_user.id]['тип расходов']['суточные'].append('счет и чек из отеля')
            Dict[message.from_user.id]['тип расходов']['расход на отель'] = []
            Dict[message.from_user.id]['тип расходов']['расход на отель'].append('счет и чек из отеля')
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'] = []
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'].append('квитанция/чек'
                                                                                                        '/выписка из '
                                                                                                        'банка, маршрут')
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'] = []
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'].append('подтверждение '
                                                                                                        'оплаты и '
                                                                                                        'детализация')
        elif message.text == 'Копия счета и ориг. выписка из банка \U0001F34F':
            Dict[message.from_user.id]['документы'].append(
                'копия счета и выписка из оригинальная выписка из банка за отель')
            Dict[message.from_user.id]['тип расходов']['суточные'].append('счет из отеля')
            Dict[message.from_user.id]['тип расходов']['расход на отель'] = []
            Dict[message.from_user.id]['тип расходов']['расход на отель'].append('счет из отеля и выписку из банка '
                                                                                 'на оплату')
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'] = []
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'].append('квитанция/чек'
                                                                                                        '/выписка из '
                                                                                                        'банка, маршрут')
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'] = []
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'].append('подтверждение '
                                                                                                        'оплаты и '
                                                                                                        'детализация')
        elif message.text == 'Ориг. подтв. прож-ия из отеля \U0001F351':
            Dict[message.from_user.id]['документы'].append('оригинальная справка из отеля')
            Dict[message.from_user.id]['тип расходов']['суточные'].append('справка из отеля')
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'] = []
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'].append('квитанция/чек'
                                                                                                        '/выписка из '
                                                                                                        'банка, маршрут')
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'] = []
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'].append('подтверждение '
                                                                                                        'оплаты и '
                                                                                                        'детализация')
        elif message.text == 'Справка от CWT \U0001F352':
            Dict[message.from_user.id]['документы'].append('справка, подтверждающая проживание в отеле, от CWT')
            Dict[message.from_user.id]['тип расходов']['суточные'].append('справка на проживание от CWT')
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'] = []
            Dict[message.from_user.id]['тип расходов']['* расходы на такси/каршеринг'].append('квитанция/чек'
                                                                                                        '/выписка из '
                                                                                                        'банка, маршрут')
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'] = []
            Dict[message.from_user.id]['тип расходов']['* прочие согласованные расходы'].append('подтверждение '
                                                                                                        'оплаты и '
                                                                                                        'детализация')
        await message.answer(f"Список документов, который нужно предоставить в финансовый отдел "
                                               f"\U0001F463:\n\n{text_print(Dict[message.from_user.id]['документы'])}"
                                               f"\n\n\U00002757Внимание!\U00002757 \n\nНе забудь:"
                                               f"\n\n1. Сделать сканы/фото всех документов до передачи в "
                                               f"финансовый отдел (для их загрузки в MyTE) \U0001F4F8"
                                               f"\n2. Сдать оригинал приказа/-ов и согласие на вылет (если было) в HR \U0001F64C"
                                               f"\n3. Отразить в MyTE следующие расходы: "
                                               f"\n{myte_print(Dict[message.from_user.id]['тип расходов'])}"
                                               f"\n\n Чтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()
    elif message.text == "Закончить диалог \U0001F3C3":
        await message.answer(f"Хорошего дня! \U0001F44B \n\nЧтобы повторить, напишите /start")
        if message.from_user.id in Dict:
            del Dict[message.from_user.id]
        await DocsStep.other_state.set()


@dp.message_handler(commands=['help'], state="*")
async def process_help_command(message: types.Message):
    await message.answer("Этот бот поможет вам узнать список документов на командировку. "
                         "\nДля начала разговора напишите /start")


@dp.message_handler(state="*")
async def other_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Для начала разговора напишите /start')


if __name__ == '__main__':
    executor.start_polling(dp)


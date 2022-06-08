import logging
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton as IKButton
from aiogram.types import InlineKeyboardMarkup as IKMarkup

from handlers.users.menu import show_menu

from keyboards.inline.menu_keybord import cbd_admin

from loader import dp

from utils.db.db_menu import add_button, gen_level, get_stage1


# Создаем класс и присваиваем к переменным функцию состояния
class FSMBtn(StatesGroup):
    btn_type = State()
    btn_header = State()
    btn_text = State()


# Создаем клавиатуру для типа кнопки
btn_type_kb = IKMarkup(row_width=2).add(
    IKButton(text='Подкатегория', callback_data='cb_type_0'),
    IKButton(text='Ветвление с заголовком', callback_data='cb_type_2'),
    IKButton(text='Финальная кнопка', callback_data='cb_type_1'),
    IKButton(text='Отмена', callback_data='cancel'),
    )

# FIXME: создаем клавиатуру для отмены
cancel_kb = IKMarkup(row_width=1).add(
    IKButton(text='Отмена', callback_data='cancel'),
)


# Точка входа в конструктор через callback
@dp.callback_query_handler(cbd_admin.filter())
async def button_build_start(callback: types.CallbackQuery,
                             callback_data: dict, state: FSMContext):
    logging.info('button_build_start')
    logging.info('Prepared callback_data for button_build. callback_data = '
                 f'{callback_data}')
    async with state.proxy() as data:
        data['pre_level'] = callback_data['pre_level']
        data['level'] = callback_data['level']
    await callback.answer()  # отвечаем на нажатие "добавить кнопку" ничем
    await FSMBtn.btn_type.set()
    await callback.message.answer('Выберете тип кнопки',
                                  reply_markup=btn_type_kb)


# Выход из FSM
@dp.callback_query_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.answer('Button creation cancelled')
    await show_menu(callback.message)  # вывод меню на экран


# Считывает тип кнопки и записывает в словарь
@dp.callback_query_handler(Text(startswith='cb_type_'), state=FSMBtn.btn_type)
async def button_type_set(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['btn_type'] = int(callback.data.split('_')[-1])
        data['rez_id'] = gen_level()
        if data['btn_type'] == 0:
            data['btn_text'] = None
    await FSMBtn.next()
    await callback.message.answer('Введите заголовок кнопки',
                                  reply_markup=cancel_kb)


# Считывает текст кнопки и записывает в словарь
@dp.message_handler(state=FSMBtn.btn_header)
async def button_header_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_header'] = text_filter(message.text, header=True)
    if data['btn_header'] is None:
        logging.error(f'{message.from_user.id} too long header')
        await message.answer('Достигнут лимит в 17 символов, '
                             'повторите ввод',
                             reply_markup=cancel_kb)
        return
    if data['btn_type'] == 0:
        async with state.proxy() as data:
            # Вызывает функцию добавления кнопки, передает составленный словарь
            add_button(data['pre_level'], data['level'], data['btn_type'],
                       data['rez_id'], data['btn_header'], data['btn_text'])
            await message.reply('Кнопка успешно добавлена')
        await state.finish()  # успешное завершение состояния
        logging.info(f'{message.from_user.id} added button '
                     f'"{data["btn_header"]}"')
        # Вывод меню на экран
        await show_menu(message,
                        test_pre_level=data['pre_level'],
                        current_level=data['level'],
                        next_level=data['level'])
    else:
        await FSMBtn.next()
        await message.answer('Введите содержимое кнопки',
                             reply_markup=cancel_kb)


# Считывает содержимое кнопки и записывает в словарь
@dp.message_handler(state=FSMBtn.btn_text)
async def button_text_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_text'] = text_filter(message.text)
    if data['btn_text'] is None:
        logging.error(f'{message.from_user.id} too long text')
        await message.answer('Достигнут лимит в 4096 символов, '
                             'повторите ввод',
                             reply_markup=cancel_kb)
        return
    async with state.proxy() as data:
        # Вызывает функцию добавления кнопки, передает составленный словарь
        add_button(data['pre_level'], data['level'], data['btn_type'],
                   data['rez_id'], data['btn_header'], data['btn_text'])
        await message.reply('Кнопка успешно добавлена')
    await state.finish()  # успешное завершение состояния
    logging.info(f'{message.from_user.id} added button '
                 f'"{data["btn_header"]}"')
    # Вывод меню на экран
    await show_menu(message,
                    test_pre_level=data['pre_level'],
                    current_level=data['level'],
                    next_level=data['level'])


# Обработка пользовательского ввода
def text_filter(text, header=False):
    # обработка длины текста
    if header is True:
        if len(text) > 17:
            return None
    if len(text) >= 4096:
        return None
    # обработка запрещенных символов
    forbidden = r"""':"""
    for sym in forbidden:
        if sym in text:
            if sym == "'":
                text = text.replace(sym, '"')
            if header is True:
                if sym == ":":
                    text = text.replace(sym, ' ')
    # обработка ссылок в тексте
    links = re.findall(r'http\S+', text)
    if links:
        for link in links:
            text = text.replace(link, f'<a href="{link}">*link*</a>')
    return text

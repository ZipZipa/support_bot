from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton as IKButton
from aiogram.types import InlineKeyboardMarkup as IKMarkup

from loader import dp

from utils.db.db_menu import add_button, gen_level


# Создаем класс и присваиваем к переменным функцию состояния
class FSMBtn(StatesGroup):
    btn_type = State()
    btn_text = State()


# Создаем клавиатуру для типа кнопки
btn_type_kb = IKMarkup(row_width=2).add(
    IKButton(text='Подкатегория', callback_data='cb_type_1'),
    IKButton(text='Ветвление с заголовком', callback_data='cb_type_2'),
    IKButton(text='Финальная кнопка', callback_data='cb_type_0'),
    IKButton(text='Отмена', callback_data='cancel'),
    )

# FIXME: создаем клавиатуру для отмены
cancel_kb = IKMarkup(row_width=1).add(
    IKButton(text='Отмена', callback_data='cancel'),
)


# Точка входа в конструктор кнопки
# на данном этапе реализована через команду /add.
#
# Ниже попробую переделать ее для callback_data, но нет возможности
# протестировать, т. к. в моей ветке не работает кнопка "новая кнопка"
@dp.message_handler(commands='add', state=None)
async def button_build_start(message: types.Message):
    # TODO: проверка на админа
    await FSMBtn.btn_type.set()
    await message.answer('Выберете тип кнопки', reply_markup=btn_type_kb)
    # await message.reply('Введите тип кнопки (0, 1, 2)')


# # TODO: Точка входа в конструктор через callback
# # Реагирует на текстовую коллбекдату 'add_button'
# @dp.callback_query_handler(text='add_button')
# async def button_build_start(callback: types.CallbackQuery):
#     # TODO: проверка на админа
#     await FSMBtn.btn_type.set()
#     await callback.message.answer('Выберете тип кнопки', reply_markup=btn_type_kb)


# TODO: переделать в инлайн
# Выход из FSM
@dp.callback_query_handler(Text(equals='cancel', ignore_case=True), state="*")
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    # await callback.message.answer('test', reply_markup='')
    await callback.answer('Button creation cancelled')


# # Выход из FSM - текст версия
# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('add_button cancelled')


# TODO: повесить инлайн-кнопки
# Считываем тип кнопки и записываем в словарь
@dp.callback_query_handler(Text(startswith='cb_type_'), state=FSMBtn.btn_type)
async def button_type_set(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['btn_type'] = int(callback.data.split('_')[-1])
        if data['btn_type'] == 0:
            data['rez_id'] = 1
        else:
            data['rez_id'] = gen_level()
    await FSMBtn.next()
    print(btn_type_kb)
    print(type(btn_type_kb))
    # FIXME: клавиатура для отмены выводится новым принтом
    await callback.message.answer('Введите текст для вывода', reply_markup=cancel_kb)


# Считываем тип кнопки и записываем в словарь - текст версия
# @dp.message_handler(state=FSMBtn.btn_type)
# async def button_type_set(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['btn_type'] = int(message.text)
#         if data['btn_type'] == 0:
#             data['rez_id'] = 1
#         elif data['btn_type'] == 1:
#             data['rez_id'] = gen_level()
#         elif data['btn_type'] == 2:
#             data['rez_id'] = gen_level()
#     await FSMBtn.next()
#     await message.reply('Введите текст для вывода')


# Считываем текст кнопки и записываем в словарь
@dp.message_handler(state=FSMBtn.btn_text)
async def button_text_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_text'] = message.text
    async with state.proxy() as data:
        await message.reply(data)
        # add_button(data['btn_text'], )  # На этом этапе вызываем функцию и передаем в неё наш словарь
    await state.finish()  # успешное завершение состояния


# можно передавать функции через регистрацию, но у нас работает и без этого
# def register_handlers_button_builder(dp: Dispatcher):
#     dp.register_message_handler(button_build_start, commands='add', state=None)
#     dp.register_message_handler(button_type_set, state=FSMBtn.btn_type)
#     dp.register_message_handler(button_text_set, state=FSMBtn.btn_text)

import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from data.config import ADMINS

from keyboards.inline.menu_keybord import categories_keyboard, menu_cd

from loader import dp

from utils.db.db_menu import all_menu, get_stage1

from cgitb import text


# async def get_message(message: types.Message):
#    await message.answer("Сообщение с <u>HTML-разметкой</u>")


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    current_level = 0
    if str(message.from_user.id) in ADMINS:  # проверка на админа
        sql = ('SELECT * FROM main_pages WHERE level = 0 '
               + 'and visebiliti in (0, 1);')
    else:
        sql = ('SELECT * FROM main_pages WHERE level = 0 '
               + 'and visebiliti = 1')
    logging.info(f'Function show_menu, current_level = {current_level}')
    await list_categories(message, current_level, sql, '0')


# Та самая функция, которая отдает категории.
# Она может принимать как CallbackQuery, так и Message.
# Помимо этого, мы в нее можем отправить и другие параметры:
# category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message],
                          current_level, sql, rez, **kwargs):
    logging.info(f'Function list_categories. rez=  {rez}')

    # Клавиатуру формируем с помощью следующей функции
    markup = await categories_keyboard(current_level, sql)
    logging.info('Keyboard recived')

    # Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        logging.info('Если Message - отправляем новое сообщение')
        await message.answer("Главное меню", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        logging.info('Если CallbackQuery - изменяем это сообщение')
        call = message
        await call.message.edit_reply_markup(markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """
    logging.info('Function navigate. Handle pressing')
    user_id = str(call.from_user.id)
    if callback_data["rez"] == "1":
        # вставить id резулльтата
        sql = f'SELECT text FROM rez_pages WHERE index_r = {callback_data["rez_page_id"] };'
        date = get_stage1(sql)
        await call.message.edit_text(f"{date[0][0]} ")
        sql = f'SELECT * FROM main_pages WHERE level = 0;'
        # await list_categories(call, int(callback_data["level"]), sql, callback_data["level"])
    elif callback_data["rez"] == "2":
        sql = f'SELECT text FROM rez_pages WHERE index_r = {callback_data["rez_page_id"]};'
        date = get_stage1(sql)
        sql = f'SELECT * FROM main_pages WHERE level = {callback_data["level"]};'
        await call.message.edit_text(f"{callback_data['state']}:\n{date[0][0]}")
        await list_categories(call, int(callback_data["level"]), sql, callback_data["level"])

    else:
        sql = f'SELECT * FROM main_pages WHERE level = {callback_data["level"]};'
        await list_categories(call, int(callback_data["level"]), sql, callback_data["rez"])
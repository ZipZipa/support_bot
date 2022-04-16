from cgitb import text
import logging
from typing import Union
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram import types
from loader import dp
from keyboards.inline.menu_keybord import menu_cd, categories_keyboard
from utils.db.db_menu import get_stage1


#async def get_message(message: types.Message):
#    await message.answer("Сообщение с <u>HTML-разметкой</u>")


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    current_level = 0
    sql = "SELECT * FROM main_pages WHERE level = 0;"
    logging.info(f'Function show_menu, current_level = {current_level}')
    await list_categories(message, current_level, sql, '0')


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message],
                          current_level, sql, rez, **kwargs):   
    logging.info(f'Function list_categories. rez=  {rez}')
    
    # Клавиатуру формируем с помощью следующей функции
    markup = await categories_keyboard(current_level, sql)
    logging.info(f'Keyboard recived')

    # Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        logging.info(f'Если Message - отправляем новое сообщение')
        await message.answer("Главное меню", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        logging.info(f'Если CallbackQuery - изменяем это сообщение')
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


    if callback_data["rez"] == "1":
        # вставить id резулльтата
        sql = f'SELECT text FROM rez_pages WHERE index_r = {callback_data["rez_page_id"] };'
        date = get_stage1(sql)
        await call.message.edit_text(f"{callback_data['state']}:\n {date[0][0]}  \n\n /menu")
    else:
        sql = f'SELECT * FROM main_pages WHERE level = {callback_data["level"]};'
        await list_categories(call, int(callback_data["level"]), sql, callback_data["rez"])

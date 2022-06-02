import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from handlers.users.to_main import back_to_main_kb

from keyboards.inline.menu_keybord import categories_keyboard, menu_cd

from loader import dp

from utils.db.db_menu import get_stage1


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    user_id = str(message.from_user.id)
    current_level = 0
    test_pre_level = 0
    next_level = 0
    sql = "SELECT * FROM main_pages WHERE level = 0;"
    logging.debug(f'Function show_menu, current_level = {current_level}')
    await list_categories(message, current_level, sql, '0',
                          user_id, test_pre_level, next_level)


# Та самая функция, которая отдает категории.
# Она может принимать как CallbackQuery, так и Message.
# Помимо этого, мы в нее можем отправить и другие параметры:
# category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message],
                          current_level, sql, button_rezult, user_id,
                          test_pre_level, next_level, **kwargs):

    logging.info(f'Function list_categories. button_rezult= {button_rezult} '
                 f'current_level= {current_level} '
                 f'test_pre_level= {test_pre_level}')

    # Клавиатуру формируем с помощью следующей функции
    markup = await categories_keyboard(current_level, sql, user_id,
                                       test_pre_level, next_level)
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

    # Параметр call: Тип объекта CallbackQuery, который прилетает в хендлер
    # Параметр callback_data: Словарь с данными,
    # которые хранятся в нажатой кнопке

    user_id = str(call.from_user.id)
    logging.info('Function navigate. Handle pressing')

    if callback_data["button_rezult"] == "1":
        # вставить id резулльтата
        # TODO:
        sql = ('SELECT text FROM rez_pages WHERE index_r = '
               f'{callback_data["next_level"]};')
        date = get_stage1(sql)
        await call.message.edit_text(f'{date[0][0]}')
        # await call.message.answer('Вернуться в /menu')
        await call.message.answer('Выберете действие',
                                  reply_markup=back_to_main_kb)

    elif callback_data["button_rezult"] == "2":
        sql = ('SELECT text FROM rez_pages WHERE index_r = '
               f'{callback_data["next_level"]};')
        date = get_stage1(sql)
        sql = ('SELECT * FROM main_pages WHERE level = '
               f'{callback_data["next_level"]};')
        await call.message.edit_text(f"{callback_data['button_name']}"
                                     f":\n{date[0][0]}")
        await list_categories(call, int(callback_data["next_level"]), sql,
                              callback_data["next_level"], user_id,
                              callback_data["test_pre_level"],
                              callback_data["next_level"])

    else:
        sql = ('SELECT * FROM main_pages WHERE level = '
               f'{callback_data["next_level"]};')
        await list_categories(call, int(callback_data["next_level"]), sql,
                              callback_data["button_rezult"], user_id,
                              callback_data["test_pre_level"],
                              callback_data["next_level"])

import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db.db_menu import get_stage1

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "state", "index",
                       "rez", "pre_level", "rez_page_id")

# callback_admin = CallbackData("is_admin_button", "lol")

# def make_callback_admin(is_admin_button="1"):
#     return callback_admin.new(is_admin_button=is_admin_button)

# С помощью этой функции будем формировать коллбек дату для каждого
# элемента меню,в зависимости от переданных параметров.
# Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, state="0", rez="0", index="0",
                       pre_level="0", rez_page_id="0"):
    return menu_cd.new(level=level, state=state, rez=rez, index=index,
                       pre_level=pre_level, rez_page_id=rez_page_id)

# Создаем функцию, которая отдает
# клавиатуру с доступными stage
async def categories_keyboard(current_level, sql, check_admin):
    markup = InlineKeyboardMarkup(row_width=2)
    logging.info('Function categories_keyboard')
    categories = get_stage1(sql)

    logging.info('Categories recived')
    for category in categories:
        # Текст на кнопке

        # Сформируем колбек дату, которая будет на кнопке.
        callback_data = make_callback_data(
            level=category[4],
            state=category[1],
            rez=category[2],
            index=category[-1],
            pre_level=category[7],
            rez_page_id=category[5])
        logging.info('Prepared callback_data for button. callback_data = '
                     + f'{callback_data}')

        # Вставляем кнопку в клавиатуру
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=callback_data))

    # Создаем Кнопку "Назад", в которой прописываем колбек дату
    if current_level != 0:
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=category[7])),
        )

    # if check_admin:
    #     a = make_callback_admin(is_admin_button="0")
    #     markup.row(
    #         InlineKeyboardButton(
    #             text="Добавить кнопку", 
    #             callback_data=a),
    #     )

    logging.info('Return markup')
    return markup

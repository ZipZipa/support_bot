import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from handlers.users.admin import check_admin

from utils.db.db_menu import get_stage1


# Создаем CallbackData-объекты, которые будут нужны
# для работы с менюшкой и вызова создания кнопки
menu_cd = CallbackData("menu", "next_level", "button_name",
                       "button_rezult", "test_pre_level")

cbd_admin = CallbackData("add_btn", "pre_level", "level")


def make_callback_data(next_level, button_name="0", button_rezult="0",
                       test_pre_level="0"):
    '''
    С помощью этой функции будем формировать коллбек дату для каждого
    элемента меню,в зависимости от переданных параметров.
    '''
    logging.info('make_callback_data. Формируем callback')
    return menu_cd.new(next_level=next_level, button_name=button_name,
                       button_rezult=button_rezult,
                       test_pre_level=test_pre_level)


def make_new_button_data(pre_level="0", level="0"):
    return cbd_admin.new(pre_level=pre_level, level=level)


async def categories_keyboard(current_level, sql, user_id,
                              test_pre_level, next_level):
    '''
    Создаем функцию, которая отдает клавиатуру с доступными категориями выбора
    '''
    markup = InlineKeyboardMarkup(row_width=2)
    logging.info('Function categories_keyboard')
    categories = get_stage1(sql)

    logging.info('Categories recived')
    for category in categories:
        # 0 - _id
        # 1 - title
        # 2 - last
        # 3 - level
        # 4 - next_level
        # 6 - visebiliti
        # 7 - previous_level

        # Сформируем колбек дату, которая будет на кнопке.
        callback_data = make_callback_data(
            button_name=category[1],        # Название кнопки
            button_rezult=category[2],      # Проверка на тип кнопки:
                                            # 0-переход к следующей кнопке
                                            # 1-финальный вывод
                                            # 2-вывод текса и переход дальше
            test_pre_level=category[3],     # Текущий уровень
            next_level=category[4],         # Следующий уровень
            )

        logging.info('Подготовленная callback_data для кнопки. '
                     f'callback_data = {callback_data}')

        # Вставляем кнопку в клавиатуру
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=callback_data))

    # Создаем Кнопку "Назад"
    if current_level != 0:
        try:
            markup.row(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=make_callback_data(category[7])),
            )
        except UnboundLocalError:
            markup.row(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=make_callback_data(test_pre_level)),
            )

    # Создаем кнопку "Добавить кнопку" для админа
    if check_admin(user_id):
        markup.row(
            InlineKeyboardButton(
                text="Добавить кнопку",
                callback_data=make_new_button_data(pre_level=test_pre_level,
                                                   level=next_level)),
        )

    logging.info('Return markup')
    return markup

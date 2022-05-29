from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from handlers.users.admin import check_admin
from utils.db.db_menu import get_stage1
import logging

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой и вызова создания кнопки
menu_cd = CallbackData("menu", "next_level", "button_name", "button_rezult", "rez_page_id", "test_pre_level")

cbd_admin = CallbackData("add_btn", "pre_level", "level")


# С помощью этой функции будем формировать коллбек дату для каждого
# элемента меню,в зависимости от переданных параметров.
def make_callback_data(next_level, button_name="0", button_rezult="0", rez_page_id="0", test_pre_level="0"):
    return menu_cd.new(next_level=next_level, button_name=button_name, button_rezult=button_rezult, rez_page_id=rez_page_id, test_pre_level=test_pre_level)

def make_new_button_data(pre_level="0", level="0"):
    return cbd_admin.new(pre_level=pre_level, level=level)


# Создаем функцию, которая отдает клавиатуру с доступными категориями выбора
async def categories_keyboard(current_level, sql, user_id, test_pre_level, next_level):
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
        # 5 - rez_page_id
        # 6 - visebiliti
        # 7 - previous_level

        # Сформируем колбек дату, которая будет на кнопке.
        callback_data = make_callback_data(
            button_name=category[1],        # Название кнопки
            button_rezult=category[2],      # Проверка на тип кнопки 0-переход к следующей кнопке 1-финальный вывод 2-вывод текса и переход дальше 
            test_pre_level=category[3],     # Текущий уровень
            next_level=category[4],         # Следующий уровень
            rez_page_id=category[5]         # id текста в таблице rez_page         
            )

        logging.info(f'Prepared callback_data for button. callback_data = {callback_data}')

        # Вставляем кнопку в клавиатуру
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=callback_data))

    # Создаем Кнопку "Назад"
    if current_level != 0:
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

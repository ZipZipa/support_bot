from aiogram import types
from aiogram.types import InlineKeyboardButton as IKButton
from aiogram.types import InlineKeyboardMarkup as IKMarkup

import handlers.users.menu as usr_menu

import keyboards.inline.menu_keybord as inline_mk

from loader import dp


# Создаем клавиатуру для финального вывода
back_to_main_kb = IKMarkup(row_width=2).add(
    IKButton(text='В меню', callback_data='to_main_menu'),
    IKButton(text='Назад', callback_data='go_back'),
    )


# Реагирует на текстовую коллбекдату 'to_main_menu'
@dp.callback_query_handler(text='to_main_menu')
async def to_main_menu(callback: types.CallbackQuery):
    await callback.answer()
    await usr_menu.show_menu(callback.message)


# FIXME: кнопка назад не работает
# Реагирует на текстовую коллбекдату 'go_back'
@dp.callback_query_handler(text='go_back')
async def go_back(callback: types.CallbackQuery):
    await callback.answer('callback recieved')
    # await callback.message.answer('test', reply_markup=usr_menu.s)
    await usr_menu.show_menu(inline_mk.categories_keyboard(inline_mk.menu_cd))

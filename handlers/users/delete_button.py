import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton as IKButton
from aiogram.types import InlineKeyboardMarkup as IKMarkup

from handlers.users.menu import show_menu

from keyboards.inline.menu_keybord import cbd_delete

from loader import dp

from utils.db.db_menu import add_button, gen_level, get_stage1

# @dp.callback_query_handler(cbd_delete.filter())
@dp.callback_query_handler(Text(startswith='delete_dict'))
async def del_button_start(callback: types.CallbackQuery):
                           #callback_data: dict):
    print('callback revieced')
    logging.info(f"callback recieved {callback}")
    await callback.answer('Callback recieved')
    await callback.message.reply('Callback revieced')

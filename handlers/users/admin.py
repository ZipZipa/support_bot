import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS

from loader import dp

from collections import UserString

from utils.db.db_menu import all_users, draw_tree


@dp.message_handler(Command("admin"))
async def admin(message: types.Message):
    logging.info('Admin start')
    user_id = str(message.from_user.id)
    if check_admin(user_id):
        logging.info('Users list')
        await message.reply('Нарекаю тебя АДМИНИСТРАТОР: '
                            + f'{message.from_user.full_name}!')
        all_usr = all_users()
        await message.answer('\n'.join(str(value) for value in all_usr))
        all_menu = menu3()
        await message.answer(all_menu)
    else:
        logging.info(f'Кто-то нас раскрыл... {message.from_user.id}')
        await message.reply(f'{message.from_user.full_name}, '
                            + 'Вы не являетесь администратором бота!')


def check_admin(user_id):
    return user_id in ADMINS
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from data.config import ADMINS

from loader import dp

from collections import UserString

from utils.db.db_menu import all_users, draw_tree
from utils.db.db_menu import Tree, get_stage1
from typing import Union

def check_admin(user_id):
    sql = f'SELECT {user_id} FROM users WHERE is_admin = "true"'
    list_admins = get_stage1(sql)
    for admin in list_admins:
        return admin in list_admins

def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
            InlineKeyboardButton(text="Инструкция администратора", url="https://telegra.ph/privet-06-14-20"),
            InlineKeyboardButton(text="Вывести список пользователей", callback_data="user_list"),
            InlineKeyboardButton(text="Показать структуру проекта", callback_data="project_tree"),
            InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")
        ]

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return (keyboard)

@dp.message_handler(Command("admin"))
async def admin_buttons(message: Message):
    logging.info('Admin start')

    if check_admin(str(message.from_user.id)):
        await message.answer('Нарекаю тебя АДМИНИСТРАТОР', reply_markup=get_keyboard())

    else:
        logging.info(f'Кто-то нас раскрыл... {message.from_user.id}')
        await message.reply(f'{message.from_user.full_name}, '
                            + 'Вы не являетесь администратором бота! '
                            + f'Отправьте свой id {message.from_user.id} администратору для получения прав')

@dp.callback_query_handler(text="user_list")
async def show_users(call: CallbackQuery):
    await call.message.edit_text('\n'.join(str(value) for value in all_users()))
    await call.answer()

@dp.callback_query_handler(text="project_tree")
async def project_tree(call: CallbackQuery):
    await call.message.edit_text(Tree.output(0))
    await call.answer()

@dp.callback_query_handler(text="add_admin")
async def add_admin(call: CallbackQuery):
    pass
    #sql = f'UPDATE users SET is_admin = true WHERE user_id = "{str(call.from_user.id)}"
    #get_stage1(sql)

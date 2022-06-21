import logging
from venv import create

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from data.config import ADMINS

from loader import dp

from collections import UserString

from utils.db.db_menu import all_users, create_tree, draw_tree
from utils.db.db_menu import Tree, get_stage1
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

def check_admin(user_id):
    sql = 'SELECT user_id FROM users WHERE is_admin = true'
    list_admins = get_stage1(sql)
    for admin in list_admins:
        if user_id == str(admin[0]):
            a=True
            break
        else:
            a=False
    return a

def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
            InlineKeyboardButton(text="Инструкция администратора", url="https://telegra.ph/privet-06-14-20"),
            InlineKeyboardButton(text="Вывести список пользователей", callback_data="user_list"),
            InlineKeyboardButton(text="Показать структуру проекта", callback_data="project_tree"),
            InlineKeyboardButton(text="Редактировать администраторов", callback_data="change_admin")
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
                            + 'Отправьте свой id администратору для получения прав')
        await message.reply (message.from_user.id)

@dp.callback_query_handler(text="user_list")
async def show_users(call: CallbackQuery):
    await call.message.edit_text('\n'.join(str(value) for value in all_users()))
    await call.answer()

@dp.callback_query_handler(text="project_tree")
async def project_tree(call: CallbackQuery):
    await call.message.edit_text(draw_tree(create_tree()))
    await call.answer()


@dp.callback_query_handler(text="change_admin")
async def add_admin_start(call: CallbackQuery):
    buttons_change = [
            InlineKeyboardButton(text="Добавить админа", callback_data="add_admin"),
            InlineKeyboardButton(text="Удалить админа", callback_data="remove_admin"),
        ]

    await call.message.answer('Что сделать с администратором?', reply_markup=InlineKeyboardMarkup(row_width=1).add(*buttons_change))

    
class change_admin(StatesGroup):
    waiting_add_id = State()
    waiting_remove_id = State()

@dp.callback_query_handler(text="add_admin", state ="*")
async def add_admin(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Введите id")
    await change_admin.waiting_add_id.set()

@dp.callback_query_handler(text="remove_admin", state ="*")
async def remove_admin(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Введите id")
    await change_admin.waiting_remove_id.set()

@dp.message_handler(state=change_admin.waiting_add_id) 
async def food_chosen(message: Message, state: FSMContext):
    sql = f'UPDATE users SET is_admin = true WHERE user_id = {str(message.text)}'
    get_stage1(sql)
    await dp.bot.send_message(str(message.text), '''Вас добавили в админы''')
    await message.answer('Админ добавлен!')
    await state.finish()

@dp.message_handler(state=change_admin.waiting_remove_id) 
async def food_chosen(message: Message, state: FSMContext):
    sql = f'UPDATE users SET is_admin = false WHERE user_id = {str(message.text)}'
    get_stage1(sql)
    await dp.bot.send_message(str(message.text), '''Вас удалили из админов''')
    await message.answer('Админ удален!')
    await state.finish()


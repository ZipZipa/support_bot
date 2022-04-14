from collections import UserString
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db.db_menu import add_user

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    usr_id = message.from_user.id
    usr_full_name = message.from_user.full_name
    add_user(usr_id, usr_full_name)
    await message.answer(f'''Здравствуйте, {usr_full_name}!

Я бот поддержки ДОПС.
Я смогу вам подсказать интересующую информацию или показать куда обратиться.

В некоторых случаях, я Вам буду отправлять прямые ссылки на Confluence или Jira.
✅Что бы их открыть на Вашем мобильном устройстве, Вы можете скачать браузер
 "Web" >> в приложении "Hub" >> в разделе "Персональный офис".

Для начала работы выберете или введите команду: /menu
''')

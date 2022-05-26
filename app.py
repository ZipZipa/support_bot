from aiogram import executor

from loader import dp

import handlers

from utils.db.db_menu import menu3, add_question

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

import handlers


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    print(menu3())
    #add_question(100,"test",0)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

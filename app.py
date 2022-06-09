from aiogram import executor
from handlers.users import button_builder
from handlers.users import delete_button

from loader import dp

import handlers

from utils.db.db_menu import draw_tree, create_tree

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)
    print(draw_tree(create_tree()))

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

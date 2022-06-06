from aiogram import executor
from handlers.users import button_builder

from loader import dp

import handlers
#get_subscribers for test
from utils.db.db_menu import menu3, get_subscribers
from utils.subscribers import send_to_subscribers, subscribe_to_group, unsubscribe_from_group, unsubscribe_from_groups

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)
    # print("Testing group test")
    # await send_to_subscribers(dispatcher, 'test', 'test')
    #
    # print("Testing group kest")
    # await send_to_subscribers(dispatcher, 'kest', 'kest')
    # await subscribe_to_group(173472441, 'kest')
    await unsubscribe_from_group(173472441, 'kest')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

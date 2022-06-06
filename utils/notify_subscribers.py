import logging

from aiogram import Dispatcher

from utils.db.db_menu import get_subscribers

async def send_To_Subscribers(dp: Dispatcher, group):
    for users in get_subscribers(group):
        try:
            await dp.bot.send_message(users[0], 'Testing message')
        except Exception as err:
            logging.exception(err)

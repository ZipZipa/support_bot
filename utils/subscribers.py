import logging

from aiogram import Dispatcher

from utils.db.db_menu import get_subscribers

async def send_To_Subscribers(dp: Dispatcher, group):
    for users in get_subscribers(group):
        try:
            if users == 'None':
                return
            await dp.bot.send_message(users[0], 'Testing message')
        except Exception as err:
            logging.exception(err)

async def subscribe_To_Groupe(user,groupName):
    #Подписка узера на группу
    print(None)

async def unsubscribe_From_Groupe(user,group):
    # Отписка узера от группы
    print(None)

async def unsubscribe_From_Groupe(user):
    # Отписка узера от всех групп
    print(None)


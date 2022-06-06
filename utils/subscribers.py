import logging

from aiogram import Dispatcher

from utils.db.db_menu import get_subscribers, subscribeTo, unsubscribeFrom


async def send_to_subscribers(dp: Dispatcher, group, text):
    for users in get_subscribers(group):
        try:
            if users == 'None':
                return
            await dp.bot.send_message(users[0], text)
            logging.info(f'[send_to_subscribers] Отправлено сообщение подписчикам группы: "{group}"')
        except Exception as err:
            logging.exception(err)


async def subscribe_to_group(user, groupName):
    logging.info(f'[subscribe_to_group] Пользователь "{user}" подписывается на группу: "{groupName}"')
    subscribeTo(user, groupName)


async def unsubscribe_from_group(user, group):
    # Отписка узера от группы
    unsubscribeFrom(user, group)


async def unsubscribe_from_groups(user):
    # Отписка узера от всех групп
    unsubscribeFromGroups(user)

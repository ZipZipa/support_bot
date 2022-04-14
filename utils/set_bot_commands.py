from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начать общение"),
            types.BotCommand("menu", "Меню"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("subscribe", "Подписаться на рассылку")
        ]
    )

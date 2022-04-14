from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/manu - Главное меню для начала работы",
            "/start - О бо мне",
            "/help - Получить справку")

    await message.answer("\n".join(text))

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'''Здравствуйте, {message.from_user.full_name}!

Я бот поддержки ДОПС.
Я смогу вам подсказать интересующую информацию или показать куда обратиться.
В некоторых случаях, я Вам буду отправлять прямые ссылкина Confluence или Jira.
✅Что бы их открыть на Вашем мобильном устройстве, Вы можете скачать браузер
 "Web" >> в приложении "Hub" >> в разделе "Персональный офис".
По какому проекту у Вас вопрос?
/menu
''')

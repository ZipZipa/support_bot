import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton as IKButton
from aiogram.types import InlineKeyboardMarkup as IKMarkup

from handlers.users.menu import show_menu
from handlers.users.button_builder import cancel_kb

from keyboards.inline.menu_keybord import cbd_delete

from loader import dp

from utils.db.db_menu import get_stage1, delete_button


class FSMDelete(StatesGroup):
    pick_button = State()
    confirm_delete = State()


@dp.callback_query_handler(cbd_delete.filter())
async def del_button_start(callback: types.CallbackQuery,
                           callback_data: dict):
    await callback.answer()
    sql = ('SELECT _id, title FROM main_pages WHERE level = '
           f'{callback_data["current_level"]}')
    buttons = get_stage1(sql)
    logging.info(f"Current delete buttons: {buttons}")
    del_markup = IKMarkup(row_width=2)
    for button in buttons:
        # 0 - _id
        # 1 - title
        del_markup.insert(
            IKButton(
                callback_data=f'delete_{button[0]}',
                text=button[1],
            ),
        )
    # Вставляем кнопку отмены
    del_markup.row(
        IKButton(
            text='Отмена',
            callback_data='cancel',
        ),
    )
    await FSMDelete.pick_button.set()
    await callback.message.answer('Внимание! Вход в режим удаления.\n'
                                  'Выберете кнопку, которую ходите удалить.',
                                  reply_markup=del_markup)


# Хендлер нажатия на кнопку удаления
@dp.callback_query_handler(Text(startswith='delete_'),
                           state=FSMDelete.pick_button)
async def pick_deletion(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['remove_id'] = int(callback.data.split('_')[-1])
    await FSMDelete.next()
    await callback.message.answer('Чтобы удалить выбранную кнопку '
                                  'и все содержимое, введите '
                                  '"подтверждаю".',
                                  reply_markup=cancel_kb)


@dp.message_handler(state=FSMDelete.confirm_delete)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == "подтверждаю":
        async with state.proxy() as data:
            delete_button(data['remove_id'])
        await message.answer('Кнопка удалена!')
        await state.finish()
        await show_menu(message)
    else:
        await message.answer('Удаление не подтверждено, '
                             'для возврата нажмите "отмена".',
                             reply_markup=cancel_kb)
        return

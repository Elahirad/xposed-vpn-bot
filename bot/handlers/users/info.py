from aiogram.types import Message

from bot.states import UserStates
from loader import dp, _
from models import User


@dp.message_handler(i18n_text='My Information ℹ️', state=UserStates.main_page)
@dp.message_handler(commands=['user_info'], state='*')
async def _show_info(message: Message, user: User):
    text = _('Name'), _('Username'), _('Balance'), _('Tomans')
    await message.answer(f"{text[0]}: {user.name}\n{text[1]}: @{user.username}\n{text[2]}: {user.balance} {text[3]}")

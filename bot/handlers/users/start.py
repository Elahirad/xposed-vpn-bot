from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import Message

from bot.commands import get_admin_commands, get_default_commands
from bot.commands import set_admin_commands
from bot.keyboards.inline import get_language_inline_markup
from bot.states import UserStates
from loader import dp, _
from models import User


@dp.message_handler(CommandStart(), state='*')
async def _start(message: Message, user: User, state: FSMContext):
    if user.is_admin:
        await set_admin_commands(user.id, user.language)

    text = _('Hi {full_name}!\n'
             'Choose your language').format(full_name=user.name)

    await message.answer(text, reply_markup=get_language_inline_markup())

    await UserStates.main_page.set()


@dp.message_handler(i18n_text='Help 🆘', state=UserStates.main_page)
@dp.message_handler(CommandHelp(), state='*')
async def _help(message: Message, user: User):
    commands = get_admin_commands(user.language) if user.is_admin else get_default_commands(user.language)

    text = _('Help 🆘') + '\n\n'
    for command in commands:
        text += f'{command.description} - {command.command}\n'

    await message.answer(text)

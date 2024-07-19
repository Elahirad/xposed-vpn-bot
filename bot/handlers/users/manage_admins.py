from aiogram import types
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message

from bot.keyboards.default import get_manage_admins_markup, get_default_markup, get_back_markup
from bot.keyboards.inline import get_admin_delete_markup
from bot.states import UserStates
from loader import dp, _
from models import User
from services.users import get_admins, find_user, make_admin, remove_admin


@dp.message_handler(i18n_text='Manage Admins ⚙️', state=UserStates.main_page, is_admin=True)
@dp.message_handler(commands=['manage_admins'], state='*', is_admin=True)
async def _manage_admins(message: Message):
    text = _('Ok! What do you want to do ?')
    await message.answer(text, reply_markup=get_manage_admins_markup())
    await UserStates.manage_admins.set()


@dp.message_handler(state=UserStates.manage_admins, is_admin=True)
async def _handle_manage_admins(message: Message, user: User):
    if message.text == 'Back 🔙':
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == 'Add Admin ➕':
        await message.answer(
            _('Enter the username or numeric id of the user you want to make admin.\nNote: Make sure the user contacted the bot.'),
            reply_markup=get_back_markup())
        await UserStates.add_admin.set()
        return
    if message.text == 'Show and Delete Admins ❌':
        for admin in get_admins():
            text = _('Numeric ID: {numeric_id}\nName: {name}\nUsername: {username}').format(numeric_id=admin.id,
                                                                                            name=admin.name,
                                                                                            username=admin.username)
            await message.answer(text, reply_markup=get_admin_delete_markup(admin.id))


@dp.message_handler(state=UserStates.add_admin, is_admin=True)
async def _handle_add_admin(message: Message, user: User):
    if message.text == 'Back 🔙':
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_admins_markup())
        await UserStates.manage_admins.set()
        return
    user_to_be_admin = find_user(message.text)
    if not user_to_be_admin:
        await message.answer(
            _('There is no user with this username or numeric id.\nMake sure the user has contacted the bot'))
        return

    try:
        make_admin(user_to_be_admin)
        await message.answer(_("This user now have admin privileges."), reply_markup=get_manage_admins_markup())
        await UserStates.manage_admins.set()
    except:
        await message.answer(_("An error occurred."))


@dp.callback_query_handler(Regexp(r'^remove_admin_(\d+)$'), state='*', is_admin=True)
async def _remove_admin(callback_query: types.CallbackQuery, regexp: Regexp):
    admin_id = regexp.group(1)
    try:
        user = find_user(admin_id)
        remove_admin(user)
        await callback_query.answer(_("Admin removed."))
        await callback_query.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        await callback_query.answer(_("An error occurred."))

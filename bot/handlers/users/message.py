from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import ChatNotFound

from bot.keyboards.default import get_default_markup, get_back_markup
from bot.keyboards.inline import get_reply_markup
from bot.states import UserStates
from loader import dp, _, bot
from models import User
from services.users import get_users


@dp.message_handler(commands=['broadcast'], state='*', is_admin=True)
async def _broadcast_message(message: Message, user: User):
    try:
        msg = message.text.split(maxsplit=1)[1]
        users = get_users()
        for user in users:
            await bot.send_message(user.id, msg)
        await message.reply(_("Broadcast message sent."))
    except:
        await message.reply(_("Broadcast message failed.\nCommand usage: /broadcast [message]"))


@dp.message_handler(commands=["private_message"], state='*', is_admin=True)
async def send_private_message(message: Message, user: User):
    try:
        user_id, msg = int(message.text.split()[1]), ' '.join(message.text.split()[2:])
        await bot.send_message(user_id, _("Message from Admin ({name}):\n{msg}").format(name=user.name, msg=msg),
                               reply_markup=get_reply_markup(user.id))
        await message.reply(_("Private message sent to user {user_id}.").format(user_id=user_id))
    except ChatNotFound:
        await message.reply(_("User not found."))
    except:
        await message.reply(_("Private message failed.\nCommand usage: /private_message [numeric_id] [message]"))


@dp.callback_query_handler(lambda c: c.data.startswith('reply_'), state='*')
async def process_callback_reply(callback_query: CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split('_')[1])
    await state.update_data(user_id=user_id)
    await bot.send_message(callback_query.from_user.id, "Please send your reply:", reply_markup=get_back_markup())
    await UserStates.message_reply.set()


@dp.message_handler(state=UserStates.message_reply)
async def _message_reply(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer('OK! You cancelled reply.', reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    state_data = await state.get_data()
    user_id = int(state_data['user_id'])
    try:
        sender = _('Admin ({name})').format(name=user.name) if user.is_admin else f"{user.name} ({user.id})"
        await bot.send_message(chat_id=user_id,
                               text=_('Message from {sender}:\n{msg}').format(sender=sender, msg=message.text),
                               reply_markup=get_reply_markup(user.id))
        await message.reply(_('Message sent successfully.'), reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
    except Exception as e:
        print(e)
        await message.reply(_("Failed to send message to user {user_id}.").format(user_id=user_id))

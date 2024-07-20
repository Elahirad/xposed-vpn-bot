from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_reply_markup(user_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Reply 💬'), callback_data=f'reply_{user_id}'))

    return markup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_admin_delete_markup(user_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Remove 🗑️'), callback_data=f'remove_admin_{user_id}'))

    return markup

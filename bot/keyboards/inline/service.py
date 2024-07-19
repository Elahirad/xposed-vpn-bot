from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_service_inline_markup(service_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Prolong 🕐'), callback_data=f'prolong_service_{service_id}'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data=f'remove_service_{service_id}'))

    return markup

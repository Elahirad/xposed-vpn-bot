from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_receipt_inline_markup(receipt_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Approve ✅'), callback_data=f'receipt_approve_{receipt_id}'))
    markup.add(InlineKeyboardButton(_('Reject ❌'), callback_data=f'receipt_reject_{receipt_id}'))

    return markup

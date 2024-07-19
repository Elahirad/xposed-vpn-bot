from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_product_inline_markup(product_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Edit Name ✏️'), callback_data=f'product_edit_name_{product_id}'))
    markup.add(InlineKeyboardButton(_('Edit Server ✏️'), callback_data=f'product_edit_server_{product_id}'))
    markup.add(InlineKeyboardButton(_('Edit Package Days ✏️'), callback_data=f'product_edit_days_{product_id}'))
    markup.add(InlineKeyboardButton(_('Edit GB Limit ✏️'), callback_data=f'product_edit_gb_limit_{product_id}'))
    markup.add(InlineKeyboardButton(_('Edit Price ✏️'), callback_data=f'product_edit_price_{product_id}'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data=f'remove_product_{product_id}'))

    return markup

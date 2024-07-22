from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_card_markup(card_id, is_active):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Disable ⛔') if is_active else _('Activate ✅'),
                                    callback_data=f'disable_card_{card_id}' if is_active else f'activate_card_{card_id}'))

    return markup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_language_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('🇮🇷 پارسی', callback_data='lang_fa'))
    markup.add(InlineKeyboardButton('🇺🇸 English', callback_data='lang_en'))

    return markup

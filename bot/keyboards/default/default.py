from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _


def get_default_markup(user):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(_('Help 🆘'), _('Settings 🛠'))
    markup.add(_('My Information ℹ️'), _('Increase Balance💵'))

    if user.is_admin:
        markup.add(_('Export users 📁'))
        markup.add(_('Manage receipts 🧾'))
        markup.add(_('Manage Admins ⚙️'))

    if len(markup.keyboard) < 1:
        return ReplyKeyboardRemove()

    return markup


def get_manage_admins_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(_('Add Admin ➕'), _('Show and Delete Admins ❌'))
    markup.add(_('Back 🔙'))

    return markup


def get_back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(_('Back 🔙'))

    return markup

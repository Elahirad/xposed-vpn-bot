from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _
from services.products import get_products
from services.servers import get_servers


def get_default_markup(user):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Get a Test Service 🧪'))
    markup.add(_('My Information ℹ️'), _('Increase Balance💵'))
    markup.add(_('Buy a Service 🛒'), _('My Services 📜'))
    markup.add(_('Help 🆘'), _('Settings 🛠'))

    if user.is_admin:
        markup.add(_('Export users 📁'), _('Manage receipts 🧾'))
        markup.add(_('Manage Servers 🖥️'), _('Manage Products 🛍️'))
        markup.add(_('Manage Admins ⚙️'))

    if len(markup.keyboard) < 1:
        return ReplyKeyboardRemove()

    return markup


def get_manage_admins_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Add Admin ➕'), _('Show and Delete Admins ❌'))
    markup.add(_('Back 🔙'))

    return markup


def get_manage_servers_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Add Server ➕'), _('Edit Servers ✏️'))
    markup.add(_('Back 🔙'))

    return markup


def get_manage_products_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Add Product ➕'), _('Edit Products ✏️'))
    markup.add(_('Back 🔙'))

    return markup


def get_order_confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Confirm ✅'))
    markup.add(_('Back 🔙'))

    return markup


def get_back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    markup.add(_('Back 🔙'))

    return markup


def get_servers_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    for server in get_servers():
        markup.add(server.name)
    markup.add(_('Back 🔙'))

    return markup


def get_products_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    for product in get_products():
        markup.add(product.name)
    markup.add(_('Back 🔙'))

    return markup

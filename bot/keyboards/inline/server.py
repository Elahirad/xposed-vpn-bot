from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_server_inline_markup(server_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Edit Name ✏️'), callback_data=f'server_edit_name_{server_id}'))
    markup.add(InlineKeyboardButton(_('Edit URL ✏️'), callback_data=f'server_edit_url_{server_id}'))
    markup.add(InlineKeyboardButton(_('Edit Proxy Path ✏️'), callback_data=f'server_edit_proxy_path_{server_id}'))
    markup.add(InlineKeyboardButton(_('Edit Users Path ✏️'), callback_data=f'server_edit_users_path_{server_id}'))
    markup.add(InlineKeyboardButton(_('Edit Admin UUID ✏️'), callback_data=f'server_edit_admin_uuid_{server_id}'))
    markup.add(InlineKeyboardButton(_('Delete 🗑️'), callback_data=f'remove_server_{server_id}'))

    return markup

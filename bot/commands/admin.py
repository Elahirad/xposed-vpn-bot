from aiogram.types import BotCommandScopeChat, BotCommand

from loader import _, bot
from .default import get_default_commands


def get_admin_commands(lang: str = 'en') -> list[BotCommand]:
    commands = get_default_commands(lang)

    commands.extend([
        BotCommand('/broadcast', _('Send broadcast message.')),
        BotCommand('/private_message', _('Send private message.')),
        BotCommand('/manage_cards', _('Manage cards.')),
        BotCommand('/add_card', _('Add cards.')),
        BotCommand('/manage_receipts', _('Manage unresolved receipts')),
        BotCommand('/manage_admins', _('Manage admins')),
        BotCommand('/manage_servers', _('Manage servers')),
        BotCommand('/manage_products', _('Manage products')),
        BotCommand('/export_users', _('Export users to csv', locale=lang)),
    ])

    return commands


async def set_admin_commands(user_id: int, commands_lang: str):
    await bot.set_my_commands(get_admin_commands(commands_lang), scope=BotCommandScopeChat(user_id))

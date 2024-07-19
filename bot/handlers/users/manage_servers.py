from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message

from bot.keyboards.default import get_manage_servers_markup, get_default_markup, get_back_markup
from bot.keyboards.inline import get_server_inline_markup
from bot.states import UserStates
from loader import dp, _, bot
from models import User
from services.servers import get_servers, add_server, delete_server, update_server_name, update_server_url, \
    update_server_admin_uuid, \
    update_server_proxy_path, update_server_users_path


@dp.message_handler(i18n_text='Manage Servers 🖥️', state=UserStates.main_page, is_admin=True)
@dp.message_handler(commands=['manage_servers'], state='*', is_admin=True)
async def _manage_servers(message: Message):
    text = _('Ok! What do you want to do ?')
    await message.answer(text, reply_markup=get_manage_servers_markup())
    await UserStates.ManageServers.main.set()


@dp.message_handler(state=UserStates.ManageServers.main, is_admin=True)
async def _handle_manage_servers(message: Message, user: User):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == _('Add Server ➕'):
        await message.answer(
            _('OK! Now send the Name of the server.'),
            reply_markup=get_back_markup())
        await UserStates.ManageServers.get_name.set()
        return
    if message.text == _('Edit Servers ✏️'):
        servers = get_servers()

        if not len(servers):
            await message.answer(_('There is no server in the database.'))
            return

        for server in servers:
            text = _(
                'Name: {name}\nURL: {url}\nProxy Path: {proxy_path}\nUsers Path: {users_path}\nAdmin UUID: {admin_uuid}').format(
                name=server.name, url=server.url,
                proxy_path=server.proxy_path,
                users_path=server.users_path,
                admin_uuid=server.admin_uuid)
            await message.answer(text, reply_markup=get_server_inline_markup(server))


@dp.message_handler(state=UserStates.ManageServers.get_name, is_admin=True)
async def _get_name(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    await state.update_data(name=message.text)
    await message.answer(_('OK! Now send the URL of the server.'), reply_markup=get_back_markup())
    await UserStates.ManageServers.get_url.set()


@dp.message_handler(state=UserStates.ManageServers.get_url, is_admin=True)
async def _get_url(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the Name of the server.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageServers.get_name.set()
        return
    await state.update_data(url=message.text)
    await message.answer(_('OK! Now send the Proxy Path of the server.'), reply_markup=get_back_markup())
    await UserStates.ManageServers.get_proxy_path.set()


@dp.message_handler(state=UserStates.ManageServers.get_proxy_path, is_admin=True)
async def _get_proxy_path(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the URL of the server.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageServers.get_url.set()
        return
    await state.update_data(proxy_path=message.text)
    await message.answer(_('OK! Now send the Users Path of the server.'), reply_markup=get_back_markup())
    await UserStates.ManageServers.get_users_path.set()


@dp.message_handler(state=UserStates.ManageServers.get_users_path, is_admin=True)
async def _get_users_path(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the Proxy Path of the server.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageServers.get_proxy_path.set()
        return
    await state.update_data(users_path=message.text)
    await message.answer(_('OK! Now send the Admin UUID of the server.'), reply_markup=get_back_markup())
    await UserStates.ManageServers.get_admin_uuid.set()


@dp.message_handler(state=UserStates.ManageServers.get_admin_uuid, is_admin=True)
async def _get_admin_uuid(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the Users Path of the server.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageServers.get_users_path.set()
        return
    state_data = await state.get_data()
    try:
        add_server(state_data['name'], state_data['url'], state_data['proxy_path'], state_data['users_path'],
                   message.text)
        await message.answer(_('Server added.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^remove_server_(\d+)$'), state='*', is_admin=True)
async def _remove_server(callback_query: types.CallbackQuery, regexp: Regexp):
    server_id = regexp.group(1)
    try:
        delete_server(server_id)
        await callback_query.answer(_("Server removed."))
        await callback_query.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        await callback_query.answer(_("An error occurred."))


@dp.callback_query_handler(Regexp(r'^server_edit_name_(\d+)$'), state='*', is_admin=True)
async def _update_server_name(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    server_id = int(regexp.group(1))
    await state.update_data(server_id=server_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new URL for this server."))
    await UserStates.ManageServers.edit_name.set()


@dp.message_handler(state=UserStates.ManageServers.edit_name, is_admin=True)
async def _update_name(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    state_data = await state.get_data()
    try:
        update_server_name(state_data['server_id'], message.text)
        await message.answer(_('Server updated.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^server_edit_url_(\d+)$'), state='*', is_admin=True)
async def _update_server_url(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    server_id = int(regexp.group(1))
    await state.update_data(server_id=server_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new URL for this server."))
    await UserStates.ManageServers.edit_url.set()


@dp.message_handler(state=UserStates.ManageServers.edit_url, is_admin=True)
async def _update_url(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    state_data = await state.get_data()
    try:
        update_server_url(state_data['server_id'], message.text)
        await message.answer(_('Server updated.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^server_edit_proxy_path_(\d+)$'), state='*', is_admin=True)
async def _update_server_proxy_path(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    server_id = int(regexp.group(1))
    await state.update_data(server_id=server_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new Proxy Path for this server."))
    await UserStates.ManageServers.edit_proxy_path.set()


@dp.message_handler(state=UserStates.ManageServers.edit_proxy_path, is_admin=True)
async def _update_proxy_path(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    state_data = await state.get_data()
    try:
        update_server_proxy_path(state_data['server_id'], message.text)
        await message.answer(_('Server updated.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^server_edit_users_path_(\d+)$'), state='*', is_admin=True)
async def _update_server_users_path(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    server_id = int(regexp.group(1))
    await state.update_data(server_id=server_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new Users Path for this server."))
    await UserStates.ManageServers.edit_user_path.set()


@dp.message_handler(state=UserStates.ManageServers.edit_user_path, is_admin=True)
async def _update_users_path(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    state_data = await state.get_data()
    try:
        update_server_users_path(state_data['server_id'], message.text)
        await message.answer(_('Server updated.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^server_edit_admin_uuid_(\d+)$'), state='*', is_admin=True)
async def _update_server_admin_uuid(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    server_id = int(regexp.group(1))
    await state.update_data(server_id=server_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new Admin UUID for this server."))
    await UserStates.ManageServers.edit_admin_uuid.set()


@dp.message_handler(state=UserStates.ManageServers.edit_admin_uuid, is_admin=True)
async def _update_admin_uuid(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
        return
    state_data = await state.get_data()
    try:
        update_server_admin_uuid(state_data['server_id'], message.text)
        await message.answer(_('Server updated.'), reply_markup=get_manage_servers_markup())
        await UserStates.ManageServers.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))

from aiogram.types import Message
from aiogram.dispatcher.filters import Regexp
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.states import UserStates
from bot.keyboards.inline import get_service_inline_markup
from bot.keyboards.default import get_order_confirm_markup, get_default_markup
from loader import dp, _, bot
from models import User
from services.service import get_user_services, get_service, remove_service
from services.users import decrease_balance
from services.hiddify import HiddifyInterface

import datetime

@dp.message_handler(i18n_text='My Services 📜', state=UserStates.main_page)
@dp.message_handler(commands=['my_services'], state='*')
async def _my_services(message: Message, user: User):
    services = get_user_services(user.id)
    

    if not len(services):
        await message.answer(_('You have no servers.'))
        return

    for service in services:
        remaining_days = service['package_days'] - (datetime.datetime.now() - datetime.datetime.strptime(service['start_date'], "%Y-%m-%d")).days
        
        text = _('Name: {name}\nDays remaining: {days}\nUsage(GB): {usage}\nLimit: {limit}')\
            .format(name=service['name'], 
                    days=remaining_days, 
                    usage=service['current_usage_GB'], 
                    limit=service['usage_limit_GB']
                    )
        await message.answer(text, reply_markup=get_service_inline_markup(service['raw_id']))


@dp.callback_query_handler(Regexp(r'^prolong_service_(\d+)$'), state='*', is_admin=True)
async def _prolong_service_handler(callback_query: types.CallbackQuery, regexp: Regexp, user: User, state: FSMContext):
    service_id = int(regexp.group(1))
    await state.update_data(service_id=service_id)
    await bot.send_message(chat_id=user.id, text=_('By prolonging your remaining days and usage will be reset.\nPress Confirm✅ to finalize prolonging'), reply_markup=get_order_confirm_markup())
    await UserStates.MyServices.prolong_confirm.set()


@dp.message_handler(state=UserStates.MyServices.prolong_confirm)
async def _prolong_service(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == _('Confirm ✅'):
        state_data = await state.get_data()
        service = get_service(state_data['service_id'])
        interface = HiddifyInterface(service.server.url, service.server.proxy_path, service.server.users_path, service.server.admin_uuid)
        interface.prolong_service(service.uuid)
        decrease_balance(service.user.id, service.product.price)
        await message.answer(
            _('Service prolong success.'),
            reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return


@dp.callback_query_handler(Regexp(r'^remove_service_(\d+)$'), state='*', is_admin=True)
async def _remove_service_handler(callback_query: types.CallbackQuery, regexp: Regexp, user: User, state: FSMContext):
    service_id = int(regexp.group(1))
    await state.update_data(service_id=service_id)
    await bot.send_message(chat_id=user.id, text=_('By deleting a service you will lose all of your remaining days and traffic.\nPress Confirm✅ to finalize deleting'), reply_markup=get_order_confirm_markup())
    await UserStates.MyServices.remove_confirm.set()

@dp.message_handler(state=UserStates.MyServices.remove_confirm, is_admin=True)
async def _remove_service_handler(message:Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == _('Confirm ✅'):
        await bot.send_message(chat_id=user.id, text=_('By deleting a service your paid balance will not be refunded.\nPress Confirm✅ to finalize deleting'), reply_markup=get_order_confirm_markup())
        await UserStates.MyServices.remove_second_confirm.set()

@dp.message_handler(state=UserStates.MyServices.remove_second_confirm)
async def _remove_service(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == _('Confirm ✅'):
        state_data = await state.get_data()
        service = get_service(state_data['service_id'])
        interface = HiddifyInterface(service.server.url, service.server.proxy_path, service.server.users_path, service.server.admin_uuid)
        interface.delete_service(service.uuid)
        remove_service(service.id)
        await message.answer(
            _('Service deletion success.'),
            reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
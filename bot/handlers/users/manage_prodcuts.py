from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message

from bot.keyboards.default import get_manage_products_markup, get_default_markup, get_back_markup, get_servers_markup
from bot.keyboards.inline import get_product_inline_markup
from bot.states import UserStates
from loader import dp, _, bot
from models import User
from services.products import get_products, add_product, delete_product, update_product_name, update_product_server, \
    update_product_days, update_product_gb_limit, update_product_price


@dp.message_handler(i18n_text='Manage Products 🛍️', state=UserStates.main_page, is_admin=True)
@dp.message_handler(commands=['manage_products'], state='*', is_admin=True)
async def _manage_products(message: Message):
    text = _('Ok! What do you want to do ?')
    await message.answer(text, reply_markup=get_manage_products_markup())
    await UserStates.ManageProducts.main.set()


@dp.message_handler(state=UserStates.ManageProducts.main, is_admin=True)
async def _handle_manage_products(message: Message, user: User):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    if message.text == _('Add Product ➕'):
        await message.answer(
            _('OK! Now send the Name of the product.'),
            reply_markup=get_back_markup())
        await UserStates.ManageProducts.get_name.set()
        return
    if message.text == _('Edit Products ✏️'):
        products = get_products()

        if not len(products):
            await message.answer(_('There is no product in the database.'))
            return
        for product in products:
            text = _('Name: {name}\nServer: {server}\nDays: {days}\nGB Limit: {gb_limit}\nPrice: {price}').format(
                name=product.name, server=product.server.name, days=product.days, gb_limit=product.gb_limit,
                price=product.price)
            await message.answer(text, reply_markup=get_product_inline_markup(product))


@dp.message_handler(state=UserStates.ManageProducts.get_name, is_admin=True)
async def _get_name(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    await state.update_data(name=message.text)
    await message.answer(_('OK! Now choose the server of this product.'), reply_markup=get_servers_markup())
    await UserStates.ManageProducts.get_server.set()


@dp.message_handler(state=UserStates.ManageProducts.get_server, is_admin=True)
async def _get_server(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the Name of the product.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageProducts.get_name.set()
        return
    await state.update_data(server=message.text)
    await message.answer(_('OK! Now send the days of the product.'), reply_markup=get_back_markup())
    await UserStates.ManageProducts.get_days.set()


@dp.message_handler(state=UserStates.ManageProducts.get_days, is_admin=True)
async def _get_days(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now choose the server of this product.'),
                             reply_markup=get_servers_markup())
        await UserStates.ManageProducts.get_server.set()
        return
    await state.update_data(days=message.text)
    await message.answer(_('OK! Now send the GB Limit of the product.'), reply_markup=get_back_markup())
    await UserStates.ManageProducts.get_gb_limit.set()


@dp.message_handler(state=UserStates.ManageProducts.get_gb_limit, is_admin=True)
async def _get_gb_limit(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the days of the product.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageProducts.get_days.set()
        return
    await state.update_data(gb_limit=message.text)
    await message.answer(_('OK! Now send the Price of the product.'), reply_markup=get_back_markup())
    await UserStates.ManageProducts.get_price.set()


@dp.message_handler(state=UserStates.ManageProducts.get_price, is_admin=True)
async def _get_gb_limit(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now send the GB Limit of the product.'),
                             reply_markup=get_back_markup())
        await UserStates.ManageProducts.get_days.set()
        return
    state_data = await state.get_data()
    try:
        add_product(state_data['name'], state_data['server'], state_data['days'], state_data['gb_limit'], message.text)
        await message.answer(_('Product added!'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^remove_product_(\d+)$'), state='*', is_admin=True)
async def _remove_product(callback_query: types.CallbackQuery, regexp: Regexp):
    product_id = regexp.group(1)
    try:
        delete_product(product_id)
        await callback_query.answer(_("Product removed."))
        await callback_query.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        await callback_query.answer(_("An error occurred."))


@dp.callback_query_handler(Regexp(r'^product_edit_name_(\d+)$'), state='*', is_admin=True)
async def _update_product_name(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext, user: User):
    product_id = int(regexp.group(1))
    await state.update_data(product_id=product_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new Name for this product."))
    await UserStates.ManageProducts.edit_name.set()


@dp.message_handler(state=UserStates.ManageProducts.edit_name, is_admin=True)
async def _update_name(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    state_data = await state.get_data()
    try:
        update_product_name(state_data['product_id'], message.text)
        await message.answer(_('Product updated.'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^product_edit_server_(\d+)$'), state='*', is_admin=True)
async def _update_product_server(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext,
                                 user: User):
    product_id = int(regexp.group(1))
    await state.update_data(product_id=product_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Choose new Server for this product."),
                           reply_markup=get_servers_markup())
    await UserStates.ManageProducts.edit_server.set()


@dp.message_handler(state=UserStates.ManageProducts.edit_server, is_admin=True)
async def _update_server(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    state_data = await state.get_data()
    try:
        update_product_server(state_data['product_id'], message.text)
        await message.answer(_('Product updated.'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^product_edit_days_(\d+)$'), state='*', is_admin=True)
async def _update_product_days(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext,
                               user: User):
    product_id = int(regexp.group(1))
    await state.update_data(product_id=product_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new days for this product."))
    await UserStates.ManageProducts.edit_days.set()


@dp.message_handler(state=UserStates.ManageProducts.edit_days, is_admin=True)
async def _update_days(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    state_data = await state.get_data()
    try:
        update_product_days(state_data['product_id'], message.text)
        await message.answer(_('Product updated.'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^product_edit_gb_limit_(\d+)$'), state='*', is_admin=True)
async def _update_product_gb_limit(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext,
                                   user: User):
    product_id = int(regexp.group(1))
    await state.update_data(product_id=product_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new GB Limit for this product."))
    await UserStates.ManageProducts.edit_gb_limit.set()


@dp.message_handler(state=UserStates.ManageProducts.edit_gb_limit, is_admin=True)
async def _update_gb_limit(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    state_data = await state.get_data()
    try:
        update_product_gb_limit(state_data['product_id'], message.text)
        await message.answer(_('Product updated.'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))


@dp.callback_query_handler(Regexp(r'^product_edit_price_(\d+)$'), state='*', is_admin=True)
async def _update_product_gb_limit(callback_query: types.CallbackQuery, regexp: Regexp, state: FSMContext,
                                   user: User):
    product_id = int(regexp.group(1))
    await state.update_data(product_id=product_id)

    await bot.send_message(chat_id=user.id, text=_("OK! Send the new Price for this product."))
    await UserStates.ManageProducts.edit_price.set()


@dp.message_handler(state=UserStates.ManageProducts.edit_price, is_admin=True)
async def _update_gb_limit(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Ok! What do you want to do ?'),
                             reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
        return
    state_data = await state.get_data()
    try:
        update_product_price(state_data['product_id'], message.text)
        await message.answer(_('Product updated.'), reply_markup=get_manage_products_markup())
        await UserStates.ManageProducts.main.set()
    except Exception as e:
        print(e)
        await message.answer(_('An error occurred.'))
